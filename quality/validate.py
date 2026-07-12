"""Validações de qualidade (regras do enunciado)."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipelines.config import LOGS, SILVER  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("quality")


def _load(name: str) -> pd.DataFrame:
    path = SILVER / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def check_duplicates(df: pd.DataFrame, keys: list[str], label: str) -> dict:
    dup = int(df.duplicated(keys).sum())
    return {
        "check": "duplicidade",
        "table": label,
        "keys": keys,
        "duplicates": dup,
        "ok": dup == 0,
    }


def check_nulls(df: pd.DataFrame, cols: list[str], label: str) -> dict:
    nulls = {c: int(df[c].isna().sum()) for c in cols if c in df.columns}
    return {
        "check": "valores_ausentes",
        "table": label,
        "nulls": nulls,
        "ok": all(v == 0 for v in nulls.values()),
    }


def check_fk(
    child: pd.DataFrame,
    parent: pd.DataFrame,
    child_key: str,
    parent_key: str,
    label: str,
) -> dict:
    missing = ~child[child_key].isin(parent[parent_key])
    n = int(missing.sum())
    return {
        "check": "chave_relacionamento",
        "table": label,
        "child_key": child_key,
        "parent_key": parent_key,
        "orphans": n,
        "ok": n == 0,
    }


def check_consistency_meta_vs_indicador(ind: pd.DataFrame, meta: pd.DataFrame) -> dict:
    # anos do indicador devem existir em meta município
    anos_ind = set(ind["ano"].dropna().unique())
    anos_meta = set(meta["ano"].dropna().unique())
    only_ind = sorted(anos_ind - anos_meta)
    return {
        "check": "consistencia_entre_tabelas",
        "detail": "anos em indicador sem meta_municipio",
        "anos_sem_meta": [int(a) for a in only_ind],
        "ok": len(only_ind) == 0,
    }


def run() -> dict:
    LOGS.mkdir(parents=True, exist_ok=True)
    uf = _load("uf")
    mun = _load("municipio")
    meta_mun = _load("meta_municipio")
    ind = _load("indicador_municipio")
    alunos = _load("alunos")
    integrado = _load("indicador_meta_integrado")

    checks = [
        check_duplicates(uf, ["id_uf"], "uf"),
        check_duplicates(mun, ["id_municipio"], "municipio"),
        check_duplicates(meta_mun, ["ano", "id_municipio"], "meta_municipio"),
        check_duplicates(ind, ["ano", "id_municipio"], "indicador_municipio"),
        check_duplicates(alunos, ["id_aluno", "ano"], "alunos"),
        check_nulls(ind, ["ano", "id_municipio", "pct_alfabetizados"], "indicador_municipio"),
        check_nulls(mun, ["id_municipio", "id_uf", "sigla_uf"], "municipio"),
        check_fk(mun, uf, "id_uf", "id_uf", "municipio→uf"),
        check_fk(ind, mun, "id_municipio", "id_municipio", "indicador→municipio"),
        check_fk(alunos, mun, "id_municipio", "id_municipio", "alunos→municipio"),
        check_consistency_meta_vs_indicador(ind, meta_mun),
        check_nulls(integrado, ["meta_pct"], "indicador_meta_integrado"),
    ]

    report = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "passed": all(c["ok"] for c in checks),
        "checks": checks,
    }
    path = LOGS / "quality_report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Quality passed=%s → %s", report["passed"], path)
    for c in checks:
        status = "OK" if c["ok"] else "FAIL"
        log.info("[%s] %s %s", status, c["check"], c.get("table", c.get("detail", "")))
    return report


if __name__ == "__main__":
    result = run()
    raise SystemExit(0 if result["passed"] else 1)
