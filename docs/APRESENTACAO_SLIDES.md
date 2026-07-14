# Apresentação — Tech Challenge Fase 2 (Alfabetiza-Cursor)

Espelho em Markdown dos slides. Arquivo PowerPoint:

[`docs/Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx`](Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx)

Regenerar: `python scripts/generate_apresentacao_pptx.py`

---

## 1. Capa
**Pipeline Híbrida Medalhão** — Indicador Criança Alfabetizada  
POSTECH / FIAP — AI Scientist  
https://github.com/nassereq/Alfabetiza-Cursor

## 2. Agenda
Introdução · Contextualização · Problema · Ferramentas · Projeto · Resultados · Qualidade/FinOps/Cloud · IA · Otimizações · Entregáveis · Fechamento

## 3. Introdução
- Papel: engenharia de dados em organização pública  
- Objetivo: pipeline híbrida medalhão + qualidade + FinOps + preparação para IA  
- 90% nota: vídeo/apresentação executiva ≤ 5 min  
- 10%: repositório GitHub com evolução e docs  

## 4. Contextualização
- Compromisso Nacional Criança Alfabetizada  
- Ponto de corte **743** (Alfabetiza Brasil / Saeb)  
- Meta **100% até 2030**  
- Fonte: Base dos Dados / Inep  

## 5. O problema
Dados fragmentados (metas, território, indicador, alunos) → gestão sem priorização clara. Falta pipeline rastreável, tratada e analítica.

## 6. Ferramentas
Python/Pandas/Parquet · Base dos Dados/BigQuery · Medalhão · Kafka/file-sink · MySQL · AWS Glue (template) · GitHub/PRs · Qualidade/FinOps

## 7. Arquitetura
Batch + streaming → Bronze → Silver → Gold → BI/IA. Cloud: GCP (evidência) + AWS (template aula).

## 8. Projeto em prática
Ingestão BD → Bronze → Silver (qualidade) → Gold (município/UF/Brasil + evolução)

## 9. Resultados Brasil
| Ano | Taxa média | Municípios | Meta traj. | Gap |
|-----|------------|------------|------------|-----|
| 2023 | 60,47% | 4.950 | 56% | +4,5 p.p. |
| 2024 | 63,17% | 5.516 | 62% | +1,2 p.p. |

## 10. Desigualdade UF (2024)
- Top: CE 90,3% · GO 80,3% · ES 78,6%  
- Desafio: BA 36,6% · SE 36,9% · RN 42,5%  

## 11. Produtos Gold
Indicador municipal · Meta×resultado UF/Brasil · Evolução temporal · Qualidade `passed=true`

## 12. Qualidade, FinOps e nuvem
Validate · Parquet/FinOps · Job BigQuery `d3ee0480-757f-4ab4-be1f-2f1edfe66c8a`

## 13. Uso de IA
Predição · Desigualdade · Clustering · Priorização · Analytics assistida (futuro)

## 14. Otimizações
Alunos reais · Nomes IBGE · Metas oficiais · Orquestração · Glue prod · Kafka gerenciado · Catálogo · Alertas

## 15. Entregáveis AVA
Repo + PRs + pipeline `--fonte raw` + docs + evidência cloud + este deck + vídeo ≤ 5 min

## 16–17. Conclusão / Obrigado
Pipeline híbrida medalhão para guiar a política até 2030 com evidência.
