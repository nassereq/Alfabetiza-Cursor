"""Gera relatórios humanos e sincroniza preview Gold em reports/.

Saídas:
  reports/gold_preview/*.csv          — espelho dos CSVs Gold (para BI/demo)
  reports/executivo/RELATORIO_EXECUTIVO.md
  reports/executivo/kpis.json
  reports/executivo/quality_snapshot.json
"""
from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from pipelines.config import GOLD, GOLD_PREVIEW, LOGS, REPORTS_EXEC

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("reports")

GOLD_CSV_NAMES = [
    "indicador_alfabetizacao_municipio.csv",
    "comparativo_meta_resultado_uf.csv",
    "comparativo_meta_resultado_brasil.csv",
    "evolucao_temporal_municipio.csv",
    "evolucao_temporal_uf.csv",
    "evolucao_temporal_brasil.csv",
]


def sync_gold_preview() -> list[str]:
    GOLD_PREVIEW.mkdir(parents=True, exist_ok=True)
    copied = []
    for name in GOLD_CSV_NAMES:
        src = GOLD / name
        if src.exists():
            shutil.copy2(src, GOLD_PREVIEW / name)
            copied.append(name)
            log.info("Preview: %s", name)
    readme = GOLD_PREVIEW / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# Gold preview",
                "",
                "Espelho dos CSVs da camada Gold (`data/gold/`), gerado por",
                "`python -m pipelines.reports.generate_summary` (também ao final da pipeline).",
                "",
                "Use estes arquivos em Excel / Power BI / slides sem copiar manualmente.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return copied


def _load_csv(name: str) -> pd.DataFrame | None:
    path = GOLD / name
    if not path.exists():
        path = GOLD_PREVIEW / name
    if not path.exists():
        return None
    return pd.read_csv(path)


def build_kpis() -> dict:
    br = _load_csv("comparativo_meta_resultado_brasil.csv")
    uf = _load_csv("comparativo_meta_resultado_uf.csv")
    mun = _load_csv("indicador_alfabetizacao_municipio.csv")
    evo = _load_csv("evolucao_temporal_brasil.csv")

    kpis: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ponto_corte_saeb": 743,
        "meta_nacional_2030": 100.0,
    }

    if br is not None and not br.empty:
        br = br.sort_values("ano")
        latest = br.iloc[-1]
        first = br.iloc[0]
        kpis["brasil"] = {
            "anos": [int(a) for a in br["ano"].tolist()],
            "taxa_media_por_ano": {
                str(int(r.ano)): round(float(r.pct_alfabetizados), 2) for r in br.itertuples()
            },
            "ultimo_ano": int(latest.ano),
            "taxa_media_ultimo": round(float(latest.pct_alfabetizados), 2),
            "n_municipios_ultimo": int(latest.n_municipios),
            "n_atingiram_meta_ultimo": int(latest.n_atingiram_meta),
            "meta_pct_ultimo": round(float(latest.meta_pct_brasil), 2)
            if pd.notna(latest.meta_pct_brasil)
            else None,
            "gap_meta_ultimo": round(float(latest.gap_meta_brasil), 2)
            if pd.notna(latest.gap_meta_brasil)
            else None,
            "delta_pp_vs_primeiro_ano": round(
                float(latest.pct_alfabetizados) - float(first.pct_alfabetizados), 2
            ),
        }

    if uf is not None and not uf.empty and "brasil" in kpis:
        ano = kpis["brasil"]["ultimo_ano"]
        u = uf[uf["ano"] == ano].sort_values("pct_alfabetizados")
        if not u.empty:
            kpis["uf"] = {
                "ano": ano,
                "menor_taxa": [
                    {
                        "sigla_uf": r.sigla_uf,
                        "pct": round(float(r.pct_alfabetizados), 2),
                        "gap": round(float(r.gap_meta_uf), 2)
                        if pd.notna(r.gap_meta_uf)
                        else None,
                    }
                    for r in u.head(3).itertuples()
                ],
                "maior_taxa": [
                    {
                        "sigla_uf": r.sigla_uf,
                        "pct": round(float(r.pct_alfabetizados), 2),
                        "gap": round(float(r.gap_meta_uf), 2)
                        if pd.notna(r.gap_meta_uf)
                        else None,
                    }
                    for r in u.tail(3).itertuples()
                ],
            }

    if mun is not None and not mun.empty and "brasil" in kpis:
        ano = kpis["brasil"]["ultimo_ano"]
        m = mun[mun["ano"] == ano]
        kpis["municipio"] = {
            "ano": ano,
            "n_linhas": int(len(m)),
            "pct_atingiu_meta": round(float(m["atingiu_meta"].mean() * 100), 2)
            if "atingiu_meta" in m.columns
            else None,
            "taxa_mediana": round(float(m["pct_alfabetizados"].median()), 2),
        }

    if evo is not None and not evo.empty and "delta_pp_ano_anterior" in evo.columns:
        kpis["evolucao_brasil"] = [
            {
                "ano": int(r.ano),
                "taxa": round(float(r.pct_alfabetizados), 2),
                "delta_pp": None
                if pd.isna(r.delta_pp_ano_anterior)
                else round(float(r.delta_pp_ano_anterior), 2),
            }
            for r in evo.sort_values("ano").itertuples()
        ]

    return kpis


def write_executive_md(kpis: dict, quality: dict | None, summary: dict | None) -> Path:
    REPORTS_EXEC.mkdir(parents=True, exist_ok=True)
    br = kpis.get("brasil", {})
    uf = kpis.get("uf", {})
    lines = [
        "# Relatório executivo — Indicador Criança Alfabetizada",
        "",
        f"Gerado em: `{kpis.get('generated_at')}` (UTC)",
        "",
        "## Visão nacional",
        "",
    ]
    if br:
        lines += [
            f"- **Último ano:** {br['ultimo_ano']}",
            f"- **Taxa média municipal:** {br['taxa_media_ultimo']}%",
            f"- **Municípios na base:** {br['n_municipios_ultimo']:,}".replace(",", "."),
            f"- **Atingiram a meta (trajetória):** {br['n_atingiram_meta_ultimo']:,}".replace(",", "."),
            f"- **Meta de referência:** {br.get('meta_pct_ultimo')}%",
            f"- **Gap meta × resultado:** {br.get('gap_meta_ultimo')} p.p.",
            f"- **Evolução vs primeiro ano:** {br.get('delta_pp_vs_primeiro_ano')} p.p.",
            "",
            "### Série",
            "",
            "| Ano | Taxa média (%) |",
            "|-----|----------------|",
        ]
        for ano, taxa in br.get("taxa_media_por_ano", {}).items():
            lines.append(f"| {ano} | {taxa} |")
        lines.append("")

    if uf:
        lines += ["## Destaques territoriais (UF)", "", "### Maior desafio", ""]
        for r in uf.get("menor_taxa", []):
            lines.append(f"- **{r['sigla_uf']}:** {r['pct']}% (gap {r['gap']} p.p.)")
        lines += ["", "### Maior desempenho", ""]
        for r in uf.get("maior_taxa", []):
            lines.append(f"- **{r['sigla_uf']}:** {r['pct']}% (gap {r['gap']} p.p.)")
        lines.append("")

    mun = kpis.get("municipio", {})
    if mun:
        lines += [
            "## Municípios",
            "",
            f"- Linhas no último ano: **{mun.get('n_linhas')}**",
            f"- Mediana da taxa: **{mun.get('taxa_mediana')}%**",
            f"- % que atingiu meta: **{mun.get('pct_atingiu_meta')}%**",
            "",
        ]

    lines += ["## Pipeline e qualidade", ""]
    if summary:
        lines += [
            f"- Fonte: `{summary.get('fonte')}`",
            f"- Latência: **{summary.get('latency_seconds')}** s",
            f"- Streaming: `{summary.get('streaming')}`",
            f"- Qualidade: **{'OK' if summary.get('quality_passed') else 'FALHOU'}**",
            "",
        ]
    if quality:
        fails = [c for c in quality.get("checks", []) if not c.get("ok")]
        lines.append(f"- Checks: {len(quality.get('checks', []))} · falhas: {len(fails)}")
        lines.append("")

    lines += [
        "## Como reproduzir",
        "",
        "```powershell",
        "python -m pipelines.run_pipeline --fonte raw --with-streaming",
        "python -m pipelines.reports.generate_summary",
        "```",
        "",
        "Artefatos: `reports/gold_preview/`, `reports/executivo/`, `reports/cloud_evidence/`.",
        "",
    ]
    path = REPORTS_EXEC / "RELATORIO_EXECUTIVO.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run() -> dict:
    REPORTS_EXEC.mkdir(parents=True, exist_ok=True)
    copied = sync_gold_preview()
    kpis = build_kpis()
    (REPORTS_EXEC / "kpis.json").write_text(
        json.dumps(kpis, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    quality = None
    summary = None
    qpath = LOGS / "quality_report.json"
    spath = LOGS / "pipeline_summary.json"
    if qpath.exists():
        quality = json.loads(qpath.read_text(encoding="utf-8"))
        (REPORTS_EXEC / "quality_snapshot.json").write_text(
            json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    if spath.exists():
        summary = json.loads(spath.read_text(encoding="utf-8"))
        (REPORTS_EXEC / "pipeline_snapshot.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    md = write_executive_md(kpis, quality, summary)
    result = {
        "gold_preview_files": copied,
        "kpis_path": str(REPORTS_EXEC / "kpis.json"),
        "executive_md": str(md),
        "brasil_ultimo": kpis.get("brasil", {}).get("taxa_media_ultimo"),
    }
    log.info("Relatório executivo: %s", md)
    return result


if __name__ == "__main__":
    run()
