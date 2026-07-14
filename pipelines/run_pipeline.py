"""Orquestra batch (+ streaming file-sink opcional) e qualidade."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipelines.batch import load_bronze, load_gold, load_silver  # noqa: E402
from pipelines.config import LOGS  # noqa: E402
from pipelines.reports import generate_summary  # noqa: E402
from pipelines.streaming import producer_eventos  # noqa: E402
from quality import validate  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("run_pipeline")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline medalhão Alfabetiza")
    parser.add_argument(
        "--fonte",
        default="sample",
        choices=["sample", "raw"],
        help="sample=dados sintéticos; raw=entidades em data/raw (Base dos Dados mapeada)",
    )
    parser.add_argument("--with-streaming", action="store_true", help="Gera eventos antes do Silver")
    parser.add_argument("--stream-n", type=int, default=10)
    args = parser.parse_args()

    LOGS.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)

    bronze = load_bronze.run(fonte=args.fonte)
    if args.with_streaming:
        events = producer_eventos.build_events(n=args.stream_n, fonte=args.fonte)
        sink = producer_eventos.write_file_sink(events)
        log.info("Streaming simulado: %s eventos → %s", len(events), sink)

    silver = load_silver.run()
    quality = validate.run()
    gold = load_gold.run()

    summary = {
        "started": started.isoformat(),
        "finished": datetime.now(timezone.utc).isoformat(),
        "latency_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "fonte": args.fonte,
        "bronze_entities": list(bronze.get("entidades", {}).keys()),
        "silver_entities": list(silver.get("entidades", {}).keys()),
        "gold_tables": list(gold.get("tabelas", {}).keys()),
        "quality_passed": quality.get("passed"),
        "streaming": bool(args.with_streaming),
    }
    path = LOGS / "pipeline_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    reports = generate_summary.run()
    summary["reports"] = {
        "executive_md": reports.get("executive_md"),
        "gold_preview_files": reports.get("gold_preview_files"),
    }
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Pipeline OK summary=%s | relatório=%s", path, reports.get("executive_md"))
    if not quality.get("passed"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
