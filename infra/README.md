# Infra cloud — GCP (evidência) + AWS (template aula)

## Estratégia

| Camada | Provedor | Papel |
|--------|----------|-------|
| Origem / billing | **GCP BigQuery** | Dados públicos Base dos Dados; job real com `job_id` |
| Medalhão (dev) | Local Parquet | Bronze → Silver → Gold sem custo |
| Medalhão (aula ETL) | **AWS** S3 SOR/SOT/SPEC + Glue | Template pronto para deploy |

## GCP — evidência de execução

```powershell
python -m pipelines.cloud.evidence_bigquery
```

| Campo | Valor (execução de referência) |
|-------|--------------------------------|
| Projeto | `alfabetiza-fiap-t-challenge-2` |
| Job ID | `d3ee0480-757f-4ab4-be1f-2f1edfe66c8a` |
| Dataset | `basedosdados.br_inep_avaliacao_alfabetizacao.municipio` |
| Artefatos | `reports/cloud_evidence/` |

Detalhes: [`reports/cloud_evidence/EVIDENCIA_CLOUD.md`](../reports/cloud_evidence/EVIDENCIA_CLOUD.md).

## AWS — buckets (espelho aula Glue)

| Bucket | Camada |
|--------|--------|
| `<account>-alfabetiza-sor` | Bronze |
| `<account>-alfabetiza-sot` | Silver |
| `<account>-alfabetiza-spec` | Gold |

## Jobs Glue

Ver `pipelines/batch/glue_jobs_template.py`.

Parâmetros típicos:

```text
--JOB_NAME alfabetiza-etl-bronze
--ENTIDADE indicador_municipio
--BUCKET_SOR <account>-alfabetiza-sor
```

## Kafka

```text
bootstrap: localhost:9092
topic: alfabetiza.indicador.updates
```

Docker Compose opcional (quando for subir broker local):

```yaml
# docker-compose.kafka.yml (referência)
services:
  kafka:
    image: bitnami/kafka:latest
    ports: ["9092:9092"]
```

## IAM mínimo (AWS)

- Glue role: `s3:GetObject/PutObject/ListBucket` nos 3 buckets  
- CloudWatch Logs: criar grupo `/aws-glue/jobs/alfabetiza-*`
