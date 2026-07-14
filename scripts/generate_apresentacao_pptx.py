"""Gera slides refinados da apresentação executiva — Tech Challenge Fase 2.

Inclui gráficos a partir de reports/executivo/kpis.json (ou Gold CSV)
e notas de orador alinhadas ao roteiro do vídeo.
"""
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx"
KPIS_PATH = ROOT / "reports" / "executivo" / "kpis.json"

NAVY = RGBColor(0x0B, 0x2C, 0x4A)
TEAL = RGBColor(0x0D, 0x7A, 0x6F)
ACCENT = RGBColor(0xE8, 0x7A, 0x2E)
LIGHT = RGBColor(0xF4, 0xF7, 0xFA)
MUTED = RGBColor(0x5A, 0x6A, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
SOFT = RGBColor(0xE8, 0xEE, 0xF3)


def _run(p, text, size=18, bold=False, color=DARK):
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return run


def _bg(slide, color=LIGHT):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = sh._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def _header(slide, title: str, subtitle: str | None = None):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.05))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.05), Inches(13.333), Inches(0.07))
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL
    line.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.28), Inches(12.2), Inches(0.45))
    _run(tb.text_frame.paragraphs[0], title, 26, True, WHITE)
    if subtitle:
        sb = slide.shapes.add_textbox(Inches(0.55), Inches(0.68), Inches(12.2), Inches(0.3))
        _run(sb.text_frame.paragraphs[0], subtitle, 12, False, RGBColor(0xB8, 0xC9, 0xD9))


def _footer(slide, n: int, total: int):
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(7.12), Inches(12.2), Inches(0.25))
    _run(
        tb.text_frame.paragraphs[0],
        f"Alfabetiza-Cursor · FIAP POSTECH · github.com/nassereq/Alfabetiza-Cursor · {n}/{total}",
        10,
        False,
        MUTED,
    )


def _notes(slide, text: str):
    slide.notes_slide.notes_text_frame.text = text


def _bullets(slide, items: list[str], top=1.4, size=17, left=0.6, width=12.1):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.4))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        _run(p, "•  " + item, size, False, DARK)


def _card(slide, left, top, w, h, title, body, color=TEAL):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = WHITE
    sh.line.color.rgb = SOFT
    tip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.1), Inches(h))
    tip.fill.solid()
    tip.fill.fore_color.rgb = color
    tip.line.fill.background()
    t = slide.shapes.add_textbox(Inches(left + 0.22), Inches(top + 0.15), Inches(w - 0.35), Inches(0.35))
    _run(t.text_frame.paragraphs[0], title, 15, True, NAVY)
    b = slide.shapes.add_textbox(Inches(left + 0.22), Inches(top + 0.55), Inches(w - 0.35), Inches(h - 0.7))
    tf = b.text_frame
    tf.word_wrap = True
    for i, line in enumerate(body.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(4)
        _run(p, line, 13, False, MUTED)


def _load_kpis() -> dict:
    if KPIS_PATH.exists():
        return json.loads(KPIS_PATH.read_text(encoding="utf-8"))
    # fallbacks didáticos se relatório ainda não rodou
    return {
        "brasil": {
            "ultimo_ano": 2024,
            "taxa_media_ultimo": 63.17,
            "n_municipios_ultimo": 5516,
            "taxa_media_por_ano": {"2023": 60.47, "2024": 63.17},
            "meta_pct_ultimo": 62.0,
            "gap_meta_ultimo": 1.17,
            "delta_pp_vs_primeiro_ano": 2.7,
        },
        "uf": {
            "ano": 2024,
            "menor_taxa": [
                {"sigla_uf": "BA", "pct": 36.56, "gap": -25.44},
                {"sigla_uf": "SE", "pct": 36.91, "gap": -25.09},
                {"sigla_uf": "RN", "pct": 42.53, "gap": -19.47},
            ],
            "maior_taxa": [
                {"sigla_uf": "ES", "pct": 78.62, "gap": 16.62},
                {"sigla_uf": "GO", "pct": 80.26, "gap": 18.26},
                {"sigla_uf": "CE", "pct": 90.29, "gap": 28.29},
            ],
        },
    }


def build() -> Path:
    kpis = _load_kpis()
    br = kpis.get("brasil", {})
    uf = kpis.get("uf", {})

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    slides = []

    # 1 capa
    s = prs.slides.add_slide(blank)
    _bg(s, NAVY)
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.55), Inches(13.333), Inches(1.95))
    band.fill.solid()
    band.fill.fore_color.rgb = TEAL
    band.line.fill.background()
    t = s.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(11.7), Inches(0.8))
    _run(t.text_frame.paragraphs[0], "Pipeline híbrida medalhão", 40, True, WHITE)
    t2 = s.shapes.add_textbox(Inches(0.8), Inches(3.0), Inches(11.7), Inches(0.6))
    _run(t2.text_frame.paragraphs[0], "Indicador Criança Alfabetizada · Tech Challenge Fase 2", 22, False, RGBColor(0xC8, 0xE6, 0xE2))
    t3 = s.shapes.add_textbox(Inches(0.8), Inches(5.85), Inches(11.7), Inches(1.2))
    tf = t3.text_frame
    _run(tf.paragraphs[0], "POSTECH / FIAP — AI Scientist", 16, True, WHITE)
    p = tf.add_paragraph()
    _run(p, "Dados públicos → evidência para gestão educacional até 2030", 14, False, WHITE)
    p = tf.add_paragraph()
    _run(p, "github.com/nassereq/Alfabetiza-Cursor", 13, False, WHITE)
    _notes(s, "Abertura: apresentar o projeto como engenharia de dados a serviço da política pública de alfabetização.")
    slides.append(s)

    # 2 agenda
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Agenda")
    _bullets(
        s,
        [
            "Contexto e problema de negócio",
            "Ferramentas e arquitetura da solução",
            "Como o projeto funciona (medalhão)",
            "Resultados Gold — Brasil e UFs",
            "Qualidade, FinOps e evidência em nuvem",
            "Potencial de IA e otimizações",
            "Entregáveis e fechamento",
        ],
        size=18,
    )
    _notes(s, "Vídeo ≤ 5 min: foque problema → arquitetura → 1 resultado → IA → fechamento.")
    slides.append(s)

    # 3 contexto + problema
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Contexto e problema", "Compromisso Nacional Criança Alfabetizada")
    _card(s, 0.5, 1.4, 6.0, 5.2, "Contexto", "Ponto de corte Saeb: 743\nIndicador = % alfabetizados\nMeta nacional: 100% até 2030\nFonte: Base dos Dados / Inep\nFoco: 2º ano do EF", TEAL)
    _card(s, 6.8, 1.4, 6.0, 5.2, "Problema", "Dados fragmentados\n(metas × território × indicador)\n\nSem pipeline integrada,\na gestão não prioriza\nonde agir com evidência.", ACCENT)
    _notes(s, "Bloco 1 do roteiro (~45s): meta 2030, corte 743, fragmentação dos dados.")
    slides.append(s)

    # 4 ferramentas
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Ferramentas", "Stack alinhada às aulas POSTECH")
    tools = [
        ("Python / Pandas / Parquet", "Medalhão local"),
        ("Base dos Dados + BigQuery", "Origem + evidência GCP"),
        ("Kafka / file-sink", "Streaming do indicador"),
        ("MySQL", "Dimensões relacionais"),
        ("AWS Glue (template)", "Deploy aula ETL"),
        ("GitHub + PRs", "Evolução auditável"),
        ("Qualidade + FinOps", "Validate + custo"),
        ("Reports executivos", "KPI + preview Gold"),
    ]
    for i, (title, body) in enumerate(tools):
        _card(s, 0.4 + (i % 4) * 3.2, 1.35 + (i // 4) * 2.7, 3.05, 2.4, title, body, TEAL if i < 4 else NAVY)
    slides.append(s)

    # 5 arquitetura
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Arquitetura", "Batch + streaming → Bronze → Silver → Gold")
    steps = [
        ("Origens", "BD / MySQL\nEventos JSON"),
        ("Bronze", "Bruto +\nmetadados"),
        ("Silver", "Limpeza +\nintegração"),
        ("Gold", "Município\nUF / Brasil"),
        ("Consumo", "BI · IA\nGestão"),
    ]
    for i, (title, body) in enumerate(steps):
        x = 0.45 + i * 2.55
        sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(2.2), Inches(2.3), Inches(3.2))
        sh.fill.solid()
        sh.fill.fore_color.rgb = WHITE
        sh.line.color.rgb = TEAL
        tb = s.shapes.add_textbox(Inches(x + 0.15), Inches(2.4), Inches(2.0), Inches(0.4))
        _run(tb.text_frame.paragraphs[0], f"{i+1}. {title}", 15, True, NAVY)
        bb = s.shapes.add_textbox(Inches(x + 0.15), Inches(3.0), Inches(2.0), Inches(2.0))
        tf = bb.text_frame
        tf.word_wrap = True
        for j, line in enumerate(body.split("\n")):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            _run(p, line, 13, False, MUTED)
        if i < len(steps) - 1:
            arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.25), Inches(3.5), Inches(0.28), Inches(0.28))
            arr.fill.solid()
            arr.fill.fore_color.rgb = ACCENT
            arr.line.fill.background()
    _notes(s, "Bloco 2 (~90s): explicar híbrido e as três camadas; citar GCP + template AWS.")
    slides.append(s)

    # 6 resultados Brasil + chart
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Resultados — Brasil", "Gold: taxa média municipal")
    series = br.get("taxa_media_por_ano", {"2023": 60.47, "2024": 63.17})
    chart_data = CategoryChartData()
    chart_data.categories = list(series.keys())
    chart_data.add_series("Taxa média (%)", tuple(series.values()))
    chart = s.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.5),
        Inches(1.4),
        Inches(7.2),
        Inches(5.3),
        chart_data,
    ).chart
    chart.has_legend = False

    _card(
        s,
        8.0,
        1.5,
        4.8,
        5.1,
        "Leitura executiva",
        f"Último ano: {br.get('ultimo_ano', 2024)}\n"
        f"Taxa: {br.get('taxa_media_ultimo', 63.17)}%\n"
        f"Municípios: {br.get('n_municipios_ultimo', 5516)}\n"
        f"Meta ref.: {br.get('meta_pct_ultimo', 62)}%\n"
        f"Gap: {br.get('gap_meta_ultimo', 1.17)} p.p.\n"
        f"Δ vs 1º ano: {br.get('delta_pp_vs_primeiro_ano', 2.7)} p.p.\n\n"
        "Avanço real, mas longe\nde 100% em 2030.",
        TEAL,
    )
    _notes(s, "Mostrar o gráfico: evolução nacional. Enfatizar que Gold transforma dado em prioridade.")
    slides.append(s)

    # 7 desigualdade UF chart
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Desigualdade territorial", f"UF — {uf.get('ano', 2024)}")
    menor = uf.get("menor_taxa", [])
    maior = uf.get("maior_taxa", [])
    # ordem: menores depois maiores
    labels = [r["sigla_uf"] for r in menor] + [r["sigla_uf"] for r in maior]
    values = [r["pct"] for r in menor] + [r["pct"] for r in maior]
    if labels:
        cd = CategoryChartData()
        cd.categories = labels
        cd.add_series("Taxa média (%)", tuple(values))
        ch = s.shapes.add_chart(
            XL_CHART_TYPE.BAR_CLUSTERED,
            Inches(0.5),
            Inches(1.35),
            Inches(8.0),
            Inches(5.4),
            cd,
        ).chart
        ch.has_legend = False
    _card(
        s,
        8.7,
        1.5,
        4.1,
        5.1,
        "Mensagem",
        "Mesma política,\nrealidades distintas.\n\nGold responde:\nquem está abaixo?\nqual a tendência?\nonde priorizar?",
        ACCENT,
    )
    _notes(s, "Contraste CE vs BA: desigualdade como argumento de valor educacional.")
    slides.append(s)

    # 8 qualidade / cloud / finops
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Qualidade, FinOps e nuvem")
    _card(s, 0.5, 1.4, 4.0, 5.2, "Qualidade", "Duplicidade · nulos · FKs\nConsistência meta×indicador\nquality.passed = true\nSnapshot em reports/", TEAL)
    _card(s, 4.7, 1.4, 4.0, 5.2, "FinOps", "Parquet particionado\nCompute sob demanda\nBQ ~0,7 MB / job\nAWS Glue sob demanda\nDev local barato", ACCENT)
    _card(s, 8.9, 1.4, 4.0, 5.2, "Cloud", "GCP BigQuery (job_id)\nTemplate AWS Glue\nreports/cloud_evidence/\nRelatório executivo\nautomático", NAVY)
    slides.append(s)

    # 9 IA + otimizações
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "IA e otimizações", "O ativo Gold habilita o próximo ciclo")
    _card(
        s,
        0.5,
        1.4,
        6.0,
        5.2,
        "Potencial de IA",
        "Predição de % até 2030\nAnálise de desigualdade\nClusters de vulnerabilidade\nPriorização de intervenção\nAnalytics em linguagem natural",
        TEAL,
    )
    _card(
        s,
        6.8,
        1.4,
        6.0,
        5.2,
        "Próximas otimizações",
        "Microdados reais (alunos)\nNomes IBGE oficiais\nMetas oficiais por ente\nOrquestração (Airflow/SF)\nGlue/S3 em produção\nAlertas de qualidade",
        ACCENT,
    )
    _notes(s, "Bloco IA (~45s): não entrar em hiperparâmetros; frisar que a engenharia entrega o ativo.")
    slides.append(s)

    # 10 entregáveis
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Entregáveis")
    _bullets(
        s,
        [
            "Repo: https://github.com/nassereq/Alfabetiza-Cursor",
            "Pipeline: python -m pipelines.run_pipeline --fonte raw --with-streaming",
            "Relatório: reports/executivo/RELATORIO_EXECUTIVO.md",
            "Preview Gold: reports/gold_preview/",
            "Evidência cloud: reports/cloud_evidence/",
            "Este deck + vídeo ≤ 5 min no AVA",
        ],
        size=18,
    )
    slides.append(s)

    # 11 conclusão
    s = prs.slides.add_slide(blank)
    _bg(s)
    _header(s, "Conclusão")
    _bullets(
        s,
        [
            "Problema: alfabetização exige dados integrados para priorizar.",
            "Solução: pipeline híbrida medalhão com qualidade e FinOps.",
            "Resultado: Gold pronta para gestão e para IA.",
            "Próximo passo: gravar o vídeo com este deck.",
        ],
        size=20,
        top=1.8,
    )
    _notes(s, "Fechamento (~30s): evidência até 2030. Obrigado.")
    slides.append(s)

    # 12 obrigado
    s = prs.slides.add_slide(blank)
    _bg(s, NAVY)
    t = s.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11.7), Inches(1))
    p = t.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _run(p, "Obrigado", 48, True, WHITE)
    t2 = s.shapes.add_textbox(Inches(0.8), Inches(3.7), Inches(11.7), Inches(0.8))
    p2 = t2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    _run(p2, "Perguntas? · github.com/nassereq/Alfabetiza-Cursor", 16, False, RGBColor(0xC8, 0xE6, 0xE2))
    slides.append(s)

    total = len(slides)
    for i, slide in enumerate(slides, 1):
        if i not in (1, total):
            _footer(slide, i, total)

    # Atualiza espelho markdown
    md = ROOT / "docs" / "APRESENTACAO_SLIDES.md"
    md.write_text(
        "\n".join(
            [
                "# Apresentação refinada — Tech Challenge Fase 2",
                "",
                f"Arquivo: [`Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx`](Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx)",
                "",
                "Regenerar (após pipeline/relatório para KPIs reais):",
                "",
                "```powershell",
                "python -m pipelines.reports.generate_summary",
                "python scripts/generate_apresentacao_pptx.py",
                "```",
                "",
                "## Slides (12)",
                "1. Capa  2. Agenda  3. Contexto e problema  4. Ferramentas",
                "5. Arquitetura  6. Resultados Brasil (gráfico)  7. Desigualdade UF (gráfico)",
                "8. Qualidade/FinOps/Cloud  9. IA e otimizações  10. Entregáveis",
                "11. Conclusão  12. Obrigado",
                "",
                "Notas de orador alinhadas a `ROTEIRO_VIDEO.md` (vídeo ≤ 5 min).",
                "",
            ]
        ),
        encoding="utf-8",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    print(f"Salvo: {build()}")
