"""02 — Carga Bronze (batch).

Padrão da aula Arquitetura de Big Data / Glue etl-bronze:
- preserva dado bruto
- adiciona metadados de ingestão (_data_ingestao, _fonte)
- grava Parquet particionável em data/bronze (local) ou S3 SOR (cloud)
"""
from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipelines.config import BRONZE, ENTIDADES, LOGS, RAW, SAMPLE  # noqa: E402
from pipelines.batch.generate_sample_data import build_samples  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("bronze")


def _ensure_samples() -> Path:
    if not (SAMPLE / "manifest.json").exists():
        log.info("Amostras ausentes — gerando...")
        build_samples()
    return SAMPLE


def load_entity(src_dir: Path, entidade: str) -> pd.DataFrame:
    csv_path = src_dir / f"{entidade}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")
    return pd.read_csv(csv_path, dtype=str)


def write_bronze(df: pd.DataFrame, entidade: str, fonte: str) -> Path:
    ts = datetime.now(timezone.utc)
    out = df.copy()
    out["_data_ingestao"] = ts.isoformat()
    out["_fonte"] = fonte
    out["_entidade"] = entidade
    out["_modo"] = "batch"

    dest_dir = BRONZE / entidade / f"dt={ts.strftime('%Y-%m-%d')}"
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / "part-000.parquet"
    out.to_parquet(path, index=False)
    return path


def run(fonte: str = "sample") -> dict:
    LOGS.mkdir(parents=True, exist_ok=True)
    src = _ensure_samples() if fonte == "sample" else RAW
    if fonte == "sample":
        # espelha raw para rastreabilidade
        RAW.mkdir(parents=True, exist_ok=True)
        for f in src.glob("*.csv"):
            shutil.copy2(f, RAW / f.name)
        shutil.copy2(src / "manifest.json", RAW / "manifest.json")

    resultados = {}
    for entidade in ENTIDADES:
        if not (src / f"{entidade}.csv").exists():
            log.warning("Pulando %s (CSV ausente)", entidade)
            continue
        df = load_entity(src, entidade)
        path = write_bronze(df, entidade, fonte=f"batch:{fonte}")
        resultados[entidade] = {"rows": len(df), "path": str(path)}
        log.info("Bronze %s: %s linhas → %s", entidade, len(df), path)

    report = {
        "layer": "bronze",
        "modo": "batch",
        "ts": datetime.now(timezone.utc).isoformat(),
        "entidades": resultados,
    }
    report_path = LOGS / "bronze_batch_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Relatório: %s", report_path)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga Bronze batch")
    parser.add_argument("--fonte", default="sample", choices=["sample", "raw"])
    args = parser.parse_args()
    run(fonte=args.fonte)


if __name__ == "__main__":
    main()
