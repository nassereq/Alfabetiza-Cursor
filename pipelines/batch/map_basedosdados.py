"""Mapeia CSVs brutos da Base dos Dados → entidades da pipeline.

Fonte: br_inep_avaliacao_alfabetizacao (municipio / uf)
Saída: data/raw/{uf,municipio,indicador_municipio,meta_*,alunos}.csv

Regras:
- serie = 2 (2º ano do EF — foco do Compromisso Nacional)
- rede = 5 (agregado mais completo na publicação BD; cobre ~5,5k municípios)
- taxa_alfabetizacao → pct_alfabetizados (Indicador Criança Alfabetizada)
- metas: trajetória didática até 100% em 2030 (as tabelas BD não trazem meta)
- alunos: microdados sintéticos alinhados à taxa real (tabela alunos fica para depois)
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from pipelines.config import PONTO_CORTE_ALFABETIZACAO, RAW

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("map_bd")

# Códigos IBGE de UF (mesma base do gerador de amostras)
UF_IBGE = [
    ("11", "RO"), ("12", "AC"), ("13", "AM"), ("14", "RR"), ("15", "PA"),
    ("16", "AP"), ("17", "TO"), ("21", "MA"), ("22", "PI"), ("23", "CE"),
    ("24", "RN"), ("25", "PB"), ("26", "PE"), ("27", "AL"), ("28", "SE"),
    ("29", "BA"), ("31", "MG"), ("32", "ES"), ("33", "RJ"), ("35", "SP"),
    ("41", "PR"), ("42", "SC"), ("43", "RS"), ("50", "MS"), ("51", "MT"),
    ("52", "GO"), ("53", "DF"),
]
SIGLA_TO_ID = {s: i for i, s in UF_IBGE}
ID_TO_SIGLA = {i: s for i, s in UF_IBGE}
NOME_UF = {s: s for _, s in UF_IBGE}

# Trajetória de meta nacional (Compromisso → 100% em 2030).
# Valores ilustrativos alinhados ao enunciado; não vêm das tabelas municipio/uf da BD.
METAS_NACIONAIS = {
    2023: 56.0,
    2024: 62.0,
    2025: 70.0,
    2026: 78.0,
    2027: 86.0,
    2028: 92.0,
    2029: 96.0,
    2030: 100.0,
}

SERIE_FOCO = 2
REDE_PADRAO = 5
RNG = np.random.default_rng(42)


def _filter_slice(df: pd.DataFrame) -> pd.DataFrame:
    out = df[(df["serie"] == SERIE_FOCO) & (df["rede"] == REDE_PADRAO)].copy()
    if out.empty:
        raise ValueError(
            f"Nenhuma linha com serie={SERIE_FOCO} e rede={REDE_PADRAO}. "
            "Ajuste filtros em map_basedosdados.py."
        )
    return out


def build_uf_dim(bd_uf: pd.DataFrame) -> pd.DataFrame:
    siglas = sorted(bd_uf["sigla_uf"].astype(str).str.upper().unique())
    rows = []
    for sigla in siglas:
        id_uf = SIGLA_TO_ID.get(sigla)
        if id_uf is None:
            log.warning("Sigla UF desconhecida ignorada: %s", sigla)
            continue
        rows.append({"id_uf": id_uf, "sigla_uf": sigla, "nome_uf": NOME_UF.get(sigla, sigla)})
    # garante UFs do IBGE mesmo se ausentes na fatia BD (ex.: DF/RR sem dado)
    for id_uf, sigla in UF_IBGE:
        if sigla not in {r["sigla_uf"] for r in rows}:
            rows.append({"id_uf": id_uf, "sigla_uf": sigla, "nome_uf": sigla})
    return pd.DataFrame(rows).drop_duplicates("id_uf").sort_values("id_uf")


def build_municipio_dim(bd_mun: pd.DataFrame) -> pd.DataFrame:
    m = bd_mun.copy()
    m["id_municipio"] = m["id_municipio"].astype(str).str.zfill(7)
    m["id_uf"] = m["id_municipio"].str[:2]
    m["sigla_uf"] = m["id_uf"].map(ID_TO_SIGLA)
    m = m.dropna(subset=["sigla_uf"])
    dim = (
        m.groupby("id_municipio", as_index=False)
        .agg(id_uf=("id_uf", "first"), sigla_uf=("sigla_uf", "first"))
    )
    dim["nome_municipio"] = "Mun_" + dim["id_municipio"]
    return dim[["id_municipio", "id_uf", "sigla_uf", "nome_municipio"]]


def build_indicador(bd_mun: pd.DataFrame, mun_dim: pd.DataFrame) -> pd.DataFrame:
    ind = bd_mun.copy()
    ind["id_municipio"] = ind["id_municipio"].astype(str).str.zfill(7)
    ind = ind.merge(mun_dim, on="id_municipio", how="inner")
    ind["pct_alfabetizados"] = pd.to_numeric(ind["taxa_alfabetizacao"], errors="coerce")
    ind["ponto_corte"] = PONTO_CORTE_ALFABETIZACAO
    ind["n_avaliados"] = pd.NA
    ind["serie"] = ind["serie"].astype(int)
    ind["rede"] = ind["rede"].astype(int)
    ind["media_portugues"] = pd.to_numeric(ind["media_portugues"], errors="coerce")
    out = ind[
        [
            "ano",
            "id_municipio",
            "id_uf",
            "sigla_uf",
            "nome_municipio",
            "pct_alfabetizados",
            "ponto_corte",
            "n_avaliados",
            "serie",
            "rede",
            "media_portugues",
        ]
    ].dropna(subset=["pct_alfabetizados"])
    return out.drop_duplicates(["ano", "id_municipio"])


def build_metas(
    anos: list[int], mun_dim: pd.DataFrame, uf_dim: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    meta_brasil = pd.DataFrame(
        [
            {
                "ano": ano,
                "meta_pct": METAS_NACIONAIS.get(ano, 100.0),
                "ponto_corte": PONTO_CORTE_ALFABETIZACAO,
            }
            for ano in sorted(set(anos) | {2030})
        ]
    )
    meta_uf_rows = []
    for ano in anos:
        base = METAS_NACIONAIS.get(ano, 100.0)
        for _, u in uf_dim.iterrows():
            meta_uf_rows.append(
                {
                    "ano": ano,
                    "id_uf": u["id_uf"],
                    "sigla_uf": u["sigla_uf"],
                    "meta_pct": base,
                }
            )
    meta_uf = pd.DataFrame(meta_uf_rows)
    meta_mun_rows = []
    for ano in anos:
        base = METAS_NACIONAIS.get(ano, 100.0)
        for _, m in mun_dim.iterrows():
            meta_mun_rows.append(
                {
                    "ano": ano,
                    "id_municipio": m["id_municipio"],
                    "id_uf": m["id_uf"],
                    "sigla_uf": m["sigla_uf"],
                    "meta_pct": base,
                }
            )
    meta_mun = pd.DataFrame(meta_mun_rows)
    return meta_brasil, meta_uf, meta_mun


def build_alunos_sinteticos(ind: pd.DataFrame, n_por_mun: int = 8) -> pd.DataFrame:
    """Microdados didáticos: amostra por município alinhada à taxa real."""
    rows = []
    aid = 1
    # limita volume: até 400 municípios × anos (FinOps / demo local)
    base = ind.sort_values(["ano", "id_municipio"]).groupby("ano", group_keys=False).head(200)
    for _, r in base.iterrows():
        p = float(r["pct_alfabetizados"]) / 100.0
        for _ in range(n_por_mun):
            score = float(RNG.normal(780 if RNG.random() < p else 700, 35))
            rows.append(
                {
                    "id_aluno": aid,
                    "ano": int(r["ano"]),
                    "id_municipio": r["id_municipio"],
                    "id_uf": r["id_uf"],
                    "sigla_uf": r["sigla_uf"],
                    "proficiencia_saeb": round(score, 1),
                    "alfabetizado": int(score >= PONTO_CORTE_ALFABETIZACAO),
                }
            )
            aid += 1
    return pd.DataFrame(rows)


def run(raw_dir: Path | None = None) -> dict:
    raw_dir = raw_dir or RAW
    mun_path = raw_dir / "bd_municipio.csv"
    uf_path = raw_dir / "bd_uf.csv"
    if not mun_path.exists() or not uf_path.exists():
        raise FileNotFoundError(
            f"Espere {mun_path.name} e {uf_path.name} em {raw_dir}. "
            "Rode: python scripts/extract_basedosdados_municipio_uf.py"
        )

    bd_mun = _filter_slice(pd.read_csv(mun_path))
    bd_uf = _filter_slice(pd.read_csv(uf_path))
    log.info("Fatia BD municipio: %s linhas | uf: %s linhas", len(bd_mun), len(bd_uf))

    uf_dim = build_uf_dim(bd_uf)
    mun_dim = build_municipio_dim(bd_mun)
    ind = build_indicador(bd_mun, mun_dim)
    anos = sorted(ind["ano"].astype(int).unique())
    meta_br, meta_uf, meta_mun = build_metas(anos, mun_dim, uf_dim)
    alunos = build_alunos_sinteticos(ind)

    outputs = {
        "uf": uf_dim,
        "municipio": mun_dim,
        "indicador_municipio": ind,
        "meta_brasil": meta_br,
        "meta_uf": meta_uf,
        "meta_municipio": meta_mun,
        "alunos": alunos,
    }
    raw_dir.mkdir(parents=True, exist_ok=True)
    for name, df in outputs.items():
        path = raw_dir / f"{name}.csv"
        df.to_csv(path, index=False)
        log.info("Escrito %s (%s linhas)", path.name, len(df))

    manifest = {
        "fonte": "basedosdados:br_inep_avaliacao_alfabetizacao",
        "filtros": {"serie": SERIE_FOCO, "rede": REDE_PADRAO},
        "mapeamento": {
            "taxa_alfabetizacao": "pct_alfabetizados",
            "metas": "derivadas_compromisso_2030",
            "alunos": "sinteticos_alinhados_taxa",
        },
        "anos": [int(a) for a in anos],
        "n_municipios": int(mun_dim["id_municipio"].nunique()),
        "arquivos_brutos": ["bd_municipio.csv", "bd_uf.csv"],
    }
    (raw_dir / "manifest_basedosdados.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Mapeia BD → entidades da pipeline")
    parser.add_argument("--raw", type=Path, default=RAW)
    args = parser.parse_args()
    run(raw_dir=args.raw)


if __name__ == "__main__":
    main()
