# Infra AWS (esqueleto FinOps)

## Buckets (espelho aula Glue)

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

## IAM mínimo

- Glue role: `s3:GetObject/PutObject/ListBucket` nos 3 buckets  
- CloudWatch Logs: criar grupo `/aws-glue/jobs/alfabetiza-*`
