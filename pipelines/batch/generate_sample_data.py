"""Gera amostras locais no formato das entidades do enunciado.

Em produção, as mesmas entidades vêm da Base dos Dados / BigQuery.
Este gerador permite rodar a pipeline offline (FinOps / demo).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from pipelines.config import SAMPLE, PONTO_CORTE_ALFABETIZACAO

RNG = np.random.default_rng(42)

UFS = [
    ("11", "RO"), ("12", "AC"), ("13", "AM"), ("14", "RR"), ("15", "PA"),
    ("16", "AP"), ("17", "TO"), ("21", "MA"), ("22", "PI"), ("23", "CE"),
    ("24", "RN"), ("25", "PB"), ("26", "PE"), ("27", "AL"), ("28", "SE"),
    ("29", "BA"), ("31", "MG"), ("32", "ES"), ("33", "RJ"), ("35", "SP"),
    ("41", "PR"), ("42", "SC"), ("43", "RS"), ("50", "MS"), ("51", "MT"),
    ("52", "GO"), ("53", "DF"),
]

ANOS = [2021, 2022, 2023]


def _municipios(n_per_uf: int = 3) -> pd.DataFrame:
    rows = []
    mid = 1000000
    for id_uf, sigla in UFS:
        for i in range(n_per_uf):
            mid += 1
            rows.append(
                {
                    "id_municipio": str(mid),
                    "id_uf": id_uf,
                    "sigla_uf": sigla,
                    "nome_municipio": f"Municipio_{sigla}_{i+1}",
                }
            )
    return pd.DataFrame(rows)


def build_samples(out: Path | None = None) -> dict[str, Path]:
    out = out or SAMPLE
    out.mkdir(parents=True, exist_ok=True)

    uf = pd.DataFrame(
        [{"id_uf": a, "sigla_uf": b, "nome_uf": b} for a, b in UFS]
    )
    mun = _municipios()

    meta_brasil = pd.DataFrame(
        [
            {"ano": 2021, "meta_pct": 60.0, "ponto_corte": PONTO_CORTE_ALFABETIZACAO},
            {"ano": 2022, "meta_pct": 70.0, "ponto_corte": PONTO_CORTE_ALFABETIZACAO},
            {"ano": 2023, "meta_pct": 80.0, "ponto_corte": PONTO_CORTE_ALFABETIZACAO},
            {"ano": 2030, "meta_pct": 100.0, "ponto_corte": PONTO_CORTE_ALFABETIZACAO},
        ]
    )

    meta_uf_rows = []
    for ano in ANOS:
        base = 55 + (ano - 2021) * 8
        for id_uf, sigla in UFS:
            meta_uf_rows.append(
                {
                    "ano": ano,
                    "id_uf": id_uf,
                    "sigla_uf": sigla,
                    "meta_pct": round(float(base + RNG.uniform(-10, 10)), 2),
                }
            )
    meta_uf = pd.DataFrame(meta_uf_rows)

    meta_mun_rows = []
    ind_rows = []
    aluno_rows = []
    aid = 1
    for _, m in mun.iterrows():
        for ano in ANOS:
            meta = round(float(50 + (ano - 2021) * 10 + RNG.uniform(-8, 8)), 2)
            resultado = round(float(meta + RNG.uniform(-15, 12)), 2)
            resultado = float(np.clip(resultado, 5, 99))
            meta_mun_rows.append(
                {
                    "ano": ano,
                    "id_municipio": m["id_municipio"],
                    "id_uf": m["id_uf"],
                    "sigla_uf": m["sigla_uf"],
                    "meta_pct": meta,
                }
            )
            ind_rows.append(
                {
                    "ano": ano,
                    "id_municipio": m["id_municipio"],
                    "id_uf": m["id_uf"],
                    "sigla_uf": m["sigla_uf"],
                    "nome_municipio": m["nome_municipio"],
                    "pct_alfabetizados": resultado,
                    "ponto_corte": PONTO_CORTE_ALFABETIZACAO,
                    "n_avaliados": int(RNG.integers(80, 800)),
                }
            )
            for _ in range(int(RNG.integers(5, 12))):
                score = float(RNG.normal(720 if resultado < 60 else 780, 40))
                aluno_rows.append(
                    {
                        "id_aluno": aid,
                        "ano": ano,
                        "id_municipio": m["id_municipio"],
                        "id_uf": m["id_uf"],
                        "sigla_uf": m["sigla_uf"],
                        "proficiencia_saeb": round(score, 1),
                        "alfabetizado": int(score >= PONTO_CORTE_ALFABETIZACAO),
                    }
                )
                aid += 1

    frames = {
        "uf": uf,
        "municipio": mun,
        "meta_brasil": meta_brasil,
        "meta_uf": meta_uf,
        "meta_municipio": pd.DataFrame(meta_mun_rows),
        "indicador_municipio": pd.DataFrame(ind_rows),
        "alunos": pd.DataFrame(aluno_rows),
    }

    paths = {}
    for name, df in frames.items():
        p = out / f"{name}.csv"
        df.to_csv(p, index=False)
        paths[name] = p

    (out / "manifest.json").write_text(
        json.dumps(
            {
                "fonte": "amostra_sintetica_offline",
                "ponto_corte": PONTO_CORTE_ALFABETIZACAO,
                "entidades": list(frames.keys()),
                "nota": "Substituir por Base dos Dados em produção",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return paths


if __name__ == "__main__":
    built = build_samples()
    for k, v in built.items():
        print(f"{k}: {v}")
