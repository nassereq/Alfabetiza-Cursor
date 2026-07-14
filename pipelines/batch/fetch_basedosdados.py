"""Baixa e mapeia tabelas da Base dos Dados (Indicador Criança Alfabetizada).

Dataset: br_inep_avaliacao_alfabetizacao
Tabelas leves: municipio, uf

Requer: pacote basedosdados + Project ID GCP com BigQuery habilitado.
Guia: https://basedosdados.org/docs/access_data_bq
"""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("fetch_bd")

DATASET = "br_inep_avaliacao_alfabetizacao"
TABLES = ("municipio", "uf")
DEFAULT_PROJECT = os.environ.get("BD_BILLING_PROJECT_ID", "alfabetiza-fiap-t-challenge-2")


def extract(out: Path, project_id: str) -> dict[str, Path]:
    import basedosdados as bd

    out.mkdir(parents=True, exist_ok=True)
    paths = {}
    for table in TABLES:
        log.info("Baixando %s.%s (billing=%s)...", DATASET, table, project_id)
        df = bd.read_table(DATASET, table, billing_project_id=project_id)
        path = out / f"bd_{table}.csv"
        df.to_csv(path, index=False)
        log.info("Salvo %s shape=%s", path.name, df.shape)
        paths[table] = path
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Base dos Dados → data/raw")
    parser.add_argument("--out", type=Path, default=Path("data/raw"))
    parser.add_argument("--project-id", default=DEFAULT_PROJECT)
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Só mapeia CSVs bd_*.csv já existentes",
    )
    parser.add_argument(
        "--skip-map",
        action="store_true",
        help="Só extrai brutos, sem gerar entidades da pipeline",
    )
    args = parser.parse_args()

    try:
        import basedosdados  # noqa: F401
    except ImportError:
        log.error("Pacote basedosdados não instalado. pip install basedosdados")
        raise SystemExit(1)

    if not args.skip_extract:
        extract(args.out, args.project_id)

    if not args.skip_map:
        from pipelines.batch.map_basedosdados import run as map_run

        manifest = map_run(raw_dir=args.out)
        log.info("Mapeamento OK: %s municípios, anos=%s", manifest["n_municipios"], manifest["anos"])


if __name__ == "__main__":
    main()
