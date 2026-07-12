# FinOps e monitoramento

## Práticas FinOps adotadas

1. **Parquet + particionamento** (`dt=`, e em cloud por `ano`/`sigla_uf`) — menos scan e storage vs CSV.  
2. **Compute sob demanda** — Glue jobs / Databricks serverless só quando a pipeline roda; nada 24×7.  
3. **Amostras locais** — desenvolvimento e CI sem custo de cloud (`data/sample`).  
4. **Bronze append / Silver-Gold overwrite seletivo** — evita reprocessar histórico sem necessidade.  
5. **Qualidade cedo** (`quality/validate.py`) — falha barata antes de popular Gold/BI.  
6. **Kafka opcional** — demo com file-sink; broker só quando necessário.

## Estimativa de custo (ordem de grandeza — AWS, conta de estudos)

| Item | Uso mensal estimado (demo acadêmica) | Custo aproximado |
|------|--------------------------------------|------------------|
| S3 SOR/SOT/SPEC (< 5 GB) | Storage + requests baixos | US$ 0,50 – 2 |
| Glue (3 jobs × 10 min × 20 dias, 2 DPU) | ~20 DPU-hours | US$ 5 – 15 |
| CloudWatch logs/métricas | Básico | US$ 0 – 2 |
| MSK / Kafka | Preferir local Docker na demo | US$ 0 (local) |
| **Total demo** | | **~US$ 5 – 20 / mês** |

Em Databricks Free Edition o compute de estudo pode ser **US$ 0** (com limites da free edition).

## Monitoramento implementado

| Sinal | Onde |
|-------|------|
| Falhas de ingestão | logs dos scripts + exit code ≠ 0 |
| Volume processado | `logs/*_report.json` (`rows` por entidade) |
| Latência end-to-end | `logs/pipeline_summary.json` → `latency_seconds` |
| Qualidade | `logs/quality_report.json` → `passed` |
| Streaming | `logs/streaming_producer_report.json` |

Script auxiliar: `python -m pipelines.monitor_health`.

## Alertas (evolução natural)

- CloudWatch Alarm se Glue job `FAILED`  
- Alerta se `quality.passed == false`  
- Alerta se volume Bronze cair > 50% vs execução anterior (dados faltando)
