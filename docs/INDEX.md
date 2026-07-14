# Índice da documentação

Mapa rápido do que está em `docs/` e `reports/`.

## Negócio e arquitetura
| Arquivo | Uso |
|---------|-----|
| [CONTEXTO_NEGOCIO.md](CONTEXTO_NEGOCIO.md) | Problema, meta 2030, entidades |
| [ARQUITETURA.md](ARQUITETURA.md) | Medalhão, trade-offs, cloud |
| [DICIONARIO_DADOS.md](DICIONARIO_DADOS.md) | Colunas e mapeamento BD |
| [FINOPS_E_MONITORAMENTO.md](FINOPS_E_MONITORAMENTO.md) | Custo e observabilidade |

## Entrega FIAP
| Arquivo | Uso |
|---------|-----|
| [ROTEIRO_ESTAGIOS_DO_PROJETO.md](ROTEIRO_ESTAGIOS_DO_PROJETO.md) | Checklist completo |
| [ROTEIRO_VIDEO.md](ROTEIRO_VIDEO.md) | Narrativa ≤ 5 min |
| [APRESENTACAO_SLIDES.md](APRESENTACAO_SLIDES.md) | Espelho dos slides |
| [Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx](Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx) | Deck para AVA/vídeo |
| [GIT_WORKFLOW.md](GIT_WORKFLOW.md) | Branches e PRs |

## Relatórios gerados (não editar à mão)
| Pasta / arquivo | Como gerar |
|-----------------|------------|
| `reports/executivo/RELATORIO_EXECUTIVO.md` | `python -m pipelines.reports.generate_summary` |
| `reports/gold_preview/*.csv` | Automático no fim da pipeline |
| `reports/cloud_evidence/` | `python -m pipelines.cloud.evidence_bigquery` |

## Guias PDF
Regenerar com `scripts/generate_guia_*.py` e `generate_roteiro_estagios_pdf.py`.
