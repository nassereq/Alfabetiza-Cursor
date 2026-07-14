# Evidência de execução em nuvem (GCP)

- **Projeto (billing):** `alfabetiza-fiap-t-challenge-2`
- **Serviço:** BigQuery
- **Job ID:** `d3ee0480-757f-4ab4-be1f-2f1edfe66c8a`
- **Location:** `US`
- **Estado:** `DONE`
- **Bytes processados:** 743845 (~0.709 MB)
- **Cache hit:** False
- **Latência cliente:** 1.87s
- **Gerado em:** 2026-07-14T18:48:59.206654+00:00

## Resultado (agregado)

```json
[
  {
    "ano": 2023,
    "n_linhas": 4950,
    "n_municipios": 4950,
    "taxa_media": 60.47
  },
  {
    "ano": 2024,
    "n_linhas": 5516,
    "n_municipios": 5516,
    "taxa_media": 63.17
  }
]
```

## Como reproduzir

```powershell
python -m pipelines.cloud.evidence_bigquery
```

Arquivo JSON completo: `reports/cloud_evidence/bigquery_job_evidence.json`.
