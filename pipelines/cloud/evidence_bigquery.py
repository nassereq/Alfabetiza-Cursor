"""Evidência de execução em nuvem (GCP BigQuery).

Consulta o dataset público da Base dos Dados usando o billing project
do aluno e grava metadados do job (job_id, bytes, duração) em
reports/cloud_evidence/ — requisito do Estágio 8 do Tech Challenge.

Uso:
  python -m pipelines.cloud.evidence_bigquery
  set BD_BILLING_PROJECT_ID=seu-projeto   # opcional
"""
from __future__ import annotations

import argparse
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("cloud_evidence")

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "reports" / "cloud_evidence"
DEFAULT_PROJECT = os.environ.get("BD_BILLING_PROJECT_ID", "alfabetiza-fiap-t-challenge-2")

SQL = """
SELECT
  ano,
  COUNT(*) AS n_linhas,
  COUNT(DISTINCT id_municipio) AS n_municipios,
  ROUND(AVG(taxa_alfabetizacao), 2) AS taxa_media
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
WHERE CAST(serie AS INT64) = 2 AND CAST(rede AS INT64) = 5
GROUP BY ano
ORDER BY ano
"""


def _bq_client(project_id: str):
    """Usa as mesmas credenciais OAuth do pacote basedosdados (já validadas no Estágio 7)."""
    from google.cloud import bigquery

    try:
        from basedosdados.download.download import _credentials

        credentials = _credentials(from_file=False, reauth=False)
        return bigquery.Client(project=project_id, credentials=credentials)
    except Exception as exc:  # noqa: BLE001
        log.warning("Fallback ADC (basedosdados creds indisponíveis): %s", exc)
        return bigquery.Client(project=project_id)


def run(project_id: str) -> dict:
    from google.cloud import bigquery

    client = _bq_client(project_id)
    job_config = bigquery.QueryJobConfig(use_legacy_sql=False)
    started = datetime.now(timezone.utc)
    log.info("Submetendo query BigQuery (billing=%s)...", project_id)
    job = client.query(SQL, job_config=job_config)
    rows = [dict(r) for r in job.result()]
    finished = datetime.now(timezone.utc)

    stats = {
        "provider": "gcp",
        "service": "bigquery",
        "billing_project_id": project_id,
        "dataset": "basedosdados.br_inep_avaliacao_alfabetizacao",
        "table": "municipio",
        "job_id": job.job_id,
        "location": job.location,
        "state": job.state,
        # Timestamps do job no servidor (None se a API não preencher — sem misturar com cliente)
        "created": job.created.isoformat() if job.created else None,
        "started": job.started.isoformat() if job.started else None,
        "ended": job.ended.isoformat() if job.ended else None,
        # Relógio do cliente (round-trip local); não substituem started/ended do job
        "client_request_started": started.isoformat(),
        "client_request_finished": finished.isoformat(),
        "total_bytes_processed": job.total_bytes_processed,
        "total_bytes_billed": job.total_bytes_billed,
        "cache_hit": job.cache_hit,
        "latency_seconds": (finished - started).total_seconds(),
        "sql": SQL.strip(),
        "result_preview": rows,
        "evidence_ts": finished.isoformat(),
        "notes": (
            "Execução real em GCP BigQuery sobre dados públicos da Base dos Dados. "
            "O medalhão local (Parquet) consome o recorte exportado; "
            "em produção o mesmo SQL alimentaria GCS/Glue ou materialização Spec. "
            "Campos started/ended são do job no servidor; "
            "client_request_* e latency_seconds medem o round-trip local."
        ),
    }

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    out = EVIDENCE_DIR / "bigquery_job_evidence.json"
    out.write_text(json.dumps(stats, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    md = EVIDENCE_DIR / "EVIDENCIA_CLOUD.md"
    bytes_mb = (stats["total_bytes_processed"] or 0) / (1024 * 1024)
    md.write_text(
        "\n".join(
            [
                "# Evidência de execução em nuvem (GCP)",
                "",
                f"- **Projeto (billing):** `{project_id}`",
                f"- **Serviço:** BigQuery",
                f"- **Job ID:** `{stats['job_id']}`",
                f"- **Location:** `{stats['location']}`",
                f"- **Estado:** `{stats['state']}`",
                f"- **Bytes processados:** {stats['total_bytes_processed']} (~{bytes_mb:.3f} MB)",
                f"- **Cache hit:** {stats['cache_hit']}",
                f"- **Latência cliente:** {stats['latency_seconds']:.2f}s",
                f"- **Gerado em:** {stats['evidence_ts']}",
                "",
                "## Resultado (agregado)",
                "",
                "```json",
                json.dumps(rows, ensure_ascii=False, indent=2, default=str),
                "```",
                "",
                "## Como reproduzir",
                "",
                "```powershell",
                "python -m pipelines.cloud.evidence_bigquery",
                "```",
                "",
                "Arquivo JSON completo: `reports/cloud_evidence/bigquery_job_evidence.json`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    log.info("Evidência salva: %s (job_id=%s)", out, stats["job_id"])
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera evidência BigQuery (Estágio 8)")
    parser.add_argument("--project-id", default=DEFAULT_PROJECT)
    args = parser.parse_args()
    run(project_id=args.project_id)


if __name__ == "__main__":
    main()
