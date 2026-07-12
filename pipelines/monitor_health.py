"""Health check rápido pós-pipeline (observabilidade leve)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipelines.config import GOLD, LOGS, SILVER  # noqa: E402


def main() -> None:
    summary_path = LOGS / "pipeline_summary.json"
    quality_path = LOGS / "quality_report.json"
    issues = []

    if not summary_path.exists():
        issues.append("Falta pipeline_summary.json — rode pipelines/run_pipeline.py")
    else:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        print(f"latency_seconds={summary.get('latency_seconds')}")
        print(f"streaming={summary.get('streaming')}")
        print(f"gold_tables={len(summary.get('gold_tables', []))}")
        if summary.get("quality_passed") is False:
            issues.append("quality_passed=false")

    if quality_path.exists():
        q = json.loads(quality_path.read_text(encoding="utf-8"))
        fails = [c for c in q.get("checks", []) if not c.get("ok")]
        print(f"quality_checks_fail={len(fails)}")
        for f in fails:
            print("  FAIL", f)

    for table in [
        "indicador_alfabetizacao_municipio.parquet",
        "comparativo_meta_resultado_uf.parquet",
        "comparativo_meta_resultado_brasil.parquet",
        "evolucao_temporal_brasil.parquet",
    ]:
        if not (GOLD / table).exists():
            issues.append(f"Gold ausente: {table}")

    if not (SILVER / "indicador_meta_integrado.parquet").exists():
        issues.append("Silver integrado ausente")

    if issues:
        print("HEALTH: FAIL")
        for i in issues:
            print(" -", i)
        raise SystemExit(1)

    print("HEALTH: OK")


if __name__ == "__main__":
    main()
