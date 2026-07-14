"""Extrai municipio e uf da Base dos Dados (br_inep_avaliacao_alfabetizacao)."""
from __future__ import annotations

from pathlib import Path

import basedosdados as bd

PROJECT = "alfabetiza-fiap-t-challenge-2"
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def main() -> None:
    print(f"Projeto GCP: {PROJECT}")
    print("Baixando municipio...")
    mun = bd.read_table(
        "br_inep_avaliacao_alfabetizacao",
        "municipio",
        billing_project_id=PROJECT,
    )
    print("Baixando uf...")
    uf = bd.read_table(
        "br_inep_avaliacao_alfabetizacao",
        "uf",
        billing_project_id=PROJECT,
    )

    print("municipio:", mun.shape)
    print("uf:", uf.shape)
    print("colunas municipio:", list(mun.columns))
    print("colunas uf:", list(uf.columns))

    mun_path = RAW / "bd_municipio.csv"
    uf_path = RAW / "bd_uf.csv"
    mun.to_csv(mun_path, index=False)
    uf.to_csv(uf_path, index=False)
    print("Salvo:", mun_path)
    print("Salvo:", uf_path)


if __name__ == "__main__":
    main()
