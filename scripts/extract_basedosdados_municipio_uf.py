"""Compat: preferir `python -m pipelines.batch.fetch_basedosdados`.

Mantido para atalhos documentados no roteiro.
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    # Delega ao fetch canônico (extrai + mapeia entidades)
    runpy.run_module("pipelines.batch.fetch_basedosdados", run_name="__main__")
