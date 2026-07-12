"""04 — Carga Gold (camada analítica).

Produtos mínimos do enunciado:
1. Indicador por município
2. Comparação meta × resultado (Brasil / UF / município)
3. Evolução temporal
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

from pipelines.config import GOLD, LOGS, SILVER  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("gold")


def run() -> dict:
    LOGS.mkdir(parents=True, exist_ok=True)
    GOLD.mkdir(parents=True, exist_ok=True)

    integrado = pd.read_parquet(SILVER / "indicador_meta_integrado.parquet")
    meta_brasil = pd.read_parquet(SILVER / "meta_brasil.parquet")
    meta_uf = pd.read_parquet(SILVER / "meta_uf.parquet")

    # 1) Indicador por município (fato analítica)
    gold_mun = integrado[
        [
            "ano",
            "id_municipio",
            "id_uf",
            "sigla_uf",
            "nome_municipio",
            "pct_alfabetizados",
            "meta_pct",
            "gap_meta_pct",
            "atingiu_meta",
            "n_avaliados",
            "ponto_corte",
        ]
    ].copy()
    gold_mun["camada"] = "gold"
    p1 = GOLD / "indicador_alfabetizacao_municipio.parquet"
    gold_mun.to_parquet(p1, index=False)
    gold_mun.to_csv(GOLD / "indicador_alfabetizacao_municipio.csv", index=False)
    log.info("Gold município: %s linhas", len(gold_mun))

    # 2a) Comparação meta × resultado — município (já no gold_mun)
    # 2b) por UF
    gold_uf = (
        gold_mun.groupby(["ano", "id_uf", "sigla_uf"], as_index=False)
        .agg(
            pct_alfabetizados=("pct_alfabetizados", "mean"),
            meta_pct_media_mun=("meta_pct", "mean"),
            n_municipios=("id_municipio", "nunique"),
            n_atingiram_meta=("atingiu_meta", "sum"),
            n_avaliados=("n_avaliados", "sum"),
        )
    )
    gold_uf = gold_uf.merge(
        meta_uf[["ano", "id_uf", "meta_pct"]].rename(columns={"meta_pct": "meta_pct_uf"}),
        on=["ano", "id_uf"],
        how="left",
    )
    gold_uf["gap_meta_uf"] = gold_uf["pct_alfabetizados"] - gold_uf["meta_pct_uf"]
    gold_uf["pct_municipios_na_meta"] = (
        gold_uf["n_atingiram_meta"] / gold_uf["n_municipios"] * 100
    ).round(2)
    gold_uf["pct_alfabetizados"] = gold_uf["pct_alfabetizados"].round(2)
    p2 = GOLD / "comparativo_meta_resultado_uf.parquet"
    gold_uf.to_parquet(p2, index=False)
    gold_uf.to_csv(GOLD / "comparativo_meta_resultado_uf.csv", index=False)
    log.info("Gold UF: %s linhas", len(gold_uf))

    # 2c) Brasil
    gold_br = (
        gold_mun.groupby("ano", as_index=False)
        .agg(
            pct_alfabetizados=("pct_alfabetizados", "mean"),
            n_municipios=("id_municipio", "nunique"),
            n_atingiram_meta=("atingiu_meta", "sum"),
            n_avaliados=("n_avaliados", "sum"),
        )
    )
    gold_br = gold_br.merge(
        meta_brasil[["ano", "meta_pct"]].rename(columns={"meta_pct": "meta_pct_brasil"}),
        on="ano",
        how="left",
    )
    gold_br["gap_meta_brasil"] = gold_br["pct_alfabetizados"] - gold_br["meta_pct_brasil"]
    gold_br["pct_alfabetizados"] = gold_br["pct_alfabetizados"].round(2)
    p3 = GOLD / "comparativo_meta_resultado_brasil.parquet"
    gold_br.to_parquet(p3, index=False)
    gold_br.to_csv(GOLD / "comparativo_meta_resultado_brasil.csv", index=False)
    log.info("Gold Brasil: %s linhas", len(gold_br))

    # 3) Evolução temporal (município + UF + Brasil)
    evo_mun = gold_mun.sort_values(["id_municipio", "ano"]).copy()
    evo_mun["delta_pp_ano_anterior"] = evo_mun.groupby("id_municipio")[
        "pct_alfabetizados"
    ].diff()
    p4 = GOLD / "evolucao_temporal_municipio.parquet"
    evo_mun.to_parquet(p4, index=False)
    evo_mun.to_csv(GOLD / "evolucao_temporal_municipio.csv", index=False)

    evo_uf = gold_uf.sort_values(["id_uf", "ano"]).copy()
    evo_uf["delta_pp_ano_anterior"] = evo_uf.groupby("id_uf")["pct_alfabetizados"].diff()
    p5 = GOLD / "evolucao_temporal_uf.parquet"
    evo_uf.to_parquet(p5, index=False)
    evo_uf.to_csv(GOLD / "evolucao_temporal_uf.csv", index=False)

    evo_br = gold_br.sort_values("ano").copy()
    evo_br["delta_pp_ano_anterior"] = evo_br["pct_alfabetizados"].diff()
    p6 = GOLD / "evolucao_temporal_brasil.parquet"
    evo_br.to_parquet(p6, index=False)
    evo_br.to_csv(GOLD / "evolucao_temporal_brasil.csv", index=False)
    log.info("Gold evolução temporal gerada")

    report = {
        "layer": "gold",
        "ts": datetime.now(timezone.utc).isoformat(),
        "tabelas": {
            "indicador_alfabetizacao_municipio": str(p1),
            "comparativo_meta_resultado_uf": str(p2),
            "comparativo_meta_resultado_brasil": str(p3),
            "evolucao_temporal_municipio": str(p4),
            "evolucao_temporal_uf": str(p5),
            "evolucao_temporal_brasil": str(p6),
        },
    }
    (LOGS / "gold_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    run()
