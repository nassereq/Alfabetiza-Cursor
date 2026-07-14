"""03 — Carga Silver (tratamento + integração).

Padrão da aula: limpeza, tipagem, nulos, deduplicação e chaves normalizadas.
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipelines.config import BRONZE, LOGS, SILVER  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("silver")


def _latest_bronze(entidade: str) -> Path:
    base = BRONZE / entidade
    if not base.exists():
        raise FileNotFoundError(f"Bronze inexistente: {base}. Rode load_bronze.py")
    parts = sorted(base.glob("dt=*/part-*.parquet"))
    if not parts:
        raise FileNotFoundError(f"Sem parquet em {base}")
    return parts[-1]


def _read_bronze(entidade: str) -> pd.DataFrame:
    return pd.read_parquet(_latest_bronze(entidade))


def _to_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def transform_uf(df: pd.DataFrame) -> pd.DataFrame:
    out = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    out["id_uf"] = out["id_uf"].astype(str).str.zfill(2)
    out["sigla_uf"] = out["sigla_uf"].astype(str).str.upper().str.strip()
    out = out.drop_duplicates(["id_uf"])
    out["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    return out


def transform_municipio(df: pd.DataFrame) -> pd.DataFrame:
    out = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    out["id_municipio"] = out["id_municipio"].astype(str)
    out["id_uf"] = out["id_uf"].astype(str).str.zfill(2)
    out["sigla_uf"] = out["sigla_uf"].astype(str).str.upper().str.strip()
    out["nome_municipio"] = out["nome_municipio"].astype(str).str.strip()
    out = out.dropna(subset=["id_municipio", "id_uf"])
    out = out.drop_duplicates(["id_municipio"])
    out["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    return out


def transform_meta_brasil(df: pd.DataFrame) -> pd.DataFrame:
    out = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    out = _to_numeric(out, ["ano", "meta_pct", "ponto_corte"])
    out = out.dropna(subset=["ano", "meta_pct"])
    out = out.drop_duplicates(["ano"])
    out["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    return out


def transform_meta_uf(df: pd.DataFrame) -> pd.DataFrame:
    out = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    out = _to_numeric(out, ["ano", "meta_pct"])
    out["id_uf"] = out["id_uf"].astype(str).str.zfill(2)
    out["sigla_uf"] = out["sigla_uf"].astype(str).str.upper().str.strip()
    out = out.dropna(subset=["ano", "id_uf", "meta_pct"])
    out = out.drop_duplicates(["ano", "id_uf"])
    out["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    return out


def transform_meta_municipio(df: pd.DataFrame) -> pd.DataFrame:
    out = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    out = _to_numeric(out, ["ano", "meta_pct"])
    out["id_municipio"] = out["id_municipio"].astype(str)
    out["id_uf"] = out["id_uf"].astype(str).str.zfill(2)
    out = out.dropna(subset=["ano", "id_municipio", "meta_pct"])
    out = out.drop_duplicates(["ano", "id_municipio"])
    out["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    return out


def transform_indicador(df: pd.DataFrame) -> pd.DataFrame:
    out = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    out = _to_numeric(
        out,
        ["ano", "pct_alfabetizados", "ponto_corte", "n_avaliados", "serie", "rede", "media_portugues"],
    )
    out["id_municipio"] = out["id_municipio"].astype(str)
    out["id_uf"] = out["id_uf"].astype(str).str.zfill(2)
    out["sigla_uf"] = out["sigla_uf"].astype(str).str.upper().str.strip()
    out = out.dropna(subset=["ano", "id_municipio", "pct_alfabetizados"])
    out = out.drop_duplicates(["ano", "id_municipio"])
    out["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    return out


def transform_alunos(df: pd.DataFrame) -> pd.DataFrame:
    out = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    out = _to_numeric(out, ["id_aluno", "ano", "proficiencia_saeb", "alfabetizado"])
    out["id_municipio"] = out["id_municipio"].astype(str)
    out["id_uf"] = out["id_uf"].astype(str).str.zfill(2)
    out = out.dropna(subset=["id_aluno", "ano", "id_municipio"])
    out = out.drop_duplicates(["id_aluno", "ano"])
    out["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    return out


TRANSFORMERS = {
    "uf": transform_uf,
    "municipio": transform_municipio,
    "meta_brasil": transform_meta_brasil,
    "meta_uf": transform_meta_uf,
    "meta_municipio": transform_meta_municipio,
    "indicador_municipio": transform_indicador,
    "alunos": transform_alunos,
}


def write_silver(df: pd.DataFrame, name: str) -> Path:
    SILVER.mkdir(parents=True, exist_ok=True)
    path = SILVER / f"{name}.parquet"
    df.to_parquet(path, index=False)
    return path


def run() -> dict:
    LOGS.mkdir(parents=True, exist_ok=True)
    resultados = {}
    for entidade, fn in TRANSFORMERS.items():
        raw = _read_bronze(entidade)
        # incluir eventos streaming já mesclados na bronze de indicador, se houver
        if entidade == "indicador_municipio":
            events_root = BRONZE / "events_indicador"
            if events_root.exists():
                ev_parts = list(events_root.glob("dt=*/part-*.parquet"))
                if ev_parts:
                    ev = pd.concat([pd.read_parquet(p) for p in ev_parts], ignore_index=True)
                    # eventos sobrescrevem o mesmo município/ano (last-write-wins)
                    raw = pd.concat([raw, ev], ignore_index=True)
                    raw = raw.drop_duplicates(["ano", "id_municipio"], keep="last")
                    log.info("Mesclados %s eventos streaming na bronze de indicador", len(ev))

        treated = fn(raw)
        # garante FK indicador → município (descarta eventos de outra fonte)
        if entidade == "indicador_municipio":
            mun_ids = set(
                pd.read_parquet(SILVER / "municipio.parquet")["id_municipio"].astype(str)
            )
            before = len(treated)
            treated = treated[treated["id_municipio"].astype(str).isin(mun_ids)].copy()
            dropped = before - len(treated)
            if dropped:
                log.warning(
                    "Removidos %s indicadores sem município (ex.: eventos antigos)",
                    dropped,
                )
        path = write_silver(treated, entidade)
        resultados[entidade] = {"rows": len(treated), "path": str(path)}
        log.info("Silver %s: %s linhas", entidade, len(treated))

    # integração: indicador + meta município + nome
    ind = pd.read_parquet(SILVER / "indicador_municipio.parquet")
    meta = pd.read_parquet(SILVER / "meta_municipio.parquet")
    mun = pd.read_parquet(SILVER / "municipio.parquet")
    integrado = (
        ind.merge(
            meta[["ano", "id_municipio", "meta_pct"]],
            on=["ano", "id_municipio"],
            how="left",
            suffixes=("", "_meta"),
        )
        .merge(
            mun[["id_municipio", "nome_municipio"]],
            on="id_municipio",
            how="left",
            suffixes=("", "_dim"),
        )
    )
    if "nome_municipio_dim" in integrado.columns:
        integrado["nome_municipio"] = integrado["nome_municipio"].fillna(
            integrado["nome_municipio_dim"]
        )
        integrado = integrado.drop(columns=["nome_municipio_dim"])
    integrado["gap_meta_pct"] = integrado["pct_alfabetizados"] - integrado["meta_pct"]
    integrado["atingiu_meta"] = integrado["gap_meta_pct"] >= 0
    integrado["_data_processamento"] = datetime.now(timezone.utc).isoformat()
    path_int = write_silver(integrado, "indicador_meta_integrado")
    resultados["indicador_meta_integrado"] = {"rows": len(integrado), "path": str(path_int)}
    log.info("Silver integrado: %s linhas", len(integrado))

    report = {
        "layer": "silver",
        "ts": datetime.now(timezone.utc).isoformat(),
        "entidades": resultados,
    }
    (LOGS / "silver_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    run()
