"""Opcional: baixar tabelas públicas via basedosdados (requer setup GCP/BD).

Se falhar (sem credenciais), use generate_sample_data.py.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("fetch_bd")

# IDs ilustrativos — ajustar conforme dataset publicado na Base dos Dados
# Consulte: https://basedosdados.org/
DATASET_QUERIES = {
    "nota": (
        "Substitua pelas queries oficiais do Indicador Criança Alfabetizada "
        "no catalogo Base dos Dados / BigQuery."
    )
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    try:
        import basedosdados as bd  # noqa: F401
    except ImportError:
        log.error("Pacote basedosdados não instalado.")
        raise SystemExit(1)

    log.warning(
        "Configure as tabelas/queries oficiais do Indicador Criança Alfabetizada "
        "em DATASET_QUERIES antes de usar em produção. "
        "Para a demo acadêmica, rode: python -m pipelines.batch.generate_sample_data"
    )
    (args.out / "BASEDADOS_README.txt").write_text(
        DATASET_QUERIES["nota"] + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
