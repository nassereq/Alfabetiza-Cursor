# Relatório executivo — Indicador Criança Alfabetizada

Gerado em: `2026-07-14T19:15:29.946304+00:00` (UTC)

## Visão nacional

- **Último ano:** 2024
- **Taxa média municipal:** 63.17%
- **Municípios na base:** 5.516
- **Atingiram a meta (trajetória):** 2.968
- **Meta de referência:** 62.0%
- **Gap meta × resultado:** 1.17 p.p.
- **Evolução vs primeiro ano:** 2.7 p.p.

### Série

| Ano | Taxa média (%) |
|-----|----------------|
| 2023 | 60.47 |
| 2024 | 63.17 |

## Destaques territoriais (UF)

### Maior desafio

- **BA:** 36.56% (gap -25.44 p.p.)
- **SE:** 36.91% (gap -25.09 p.p.)
- **RN:** 42.53% (gap -19.47 p.p.)

### Maior desempenho

- **ES:** 78.62% (gap 16.62 p.p.)
- **GO:** 80.26% (gap 18.26 p.p.)
- **CE:** 90.29% (gap 28.29 p.p.)

## Municípios

- Linhas no último ano: **5516**
- Mediana da taxa: **64.28%**
- % que atingiu meta: **53.81%**

## Pipeline e qualidade

- Fonte: `raw`
- Latência: **1.02701** s
- Streaming: `True`
- Qualidade: **OK**

- Checks: 12 · falhas: 0

## Como reproduzir

```powershell
python -m pipelines.run_pipeline --fonte raw --with-streaming
python -m pipelines.reports.generate_summary
```

Artefatos: `reports/gold_preview/`, `reports/executivo/`, `reports/cloud_evidence/`.
