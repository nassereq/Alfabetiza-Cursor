# Mapa das aulas POSTECH → Tech Challenge

Repositório-base da turma: [POSTECH_AI_SCIENTIST / Fase 2](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202)

| Material | O que reaproveitamos | Onde está neste repo |
|----------|----------------------|----------------------|
| [Arquitetura de Big Data](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/Arquitetura%20de%20Big%20Data) | Fluxo `01_origens → 02_bronze → 03_silver → 04_gold`, schemas medalhão, metadados `_data_ingestao` / `_fonte`, limpeza e agregações PySpark/Delta | `notebooks/01–04_*.ipynb`, `pipelines/batch/` |
| [ETL Pipelines](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/ETL%20Pipelines) | Pandas/PySpark ETL; Kafka produce/consume; **AWS Glue** `etl-bronze/silver/gold` com buckets SOR/SOT/SPEC | `pipelines/batch/glue_*.py`, `pipelines/streaming/` |
| [Banco de dados relacionais](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/Banco%20de%20dados%20relacionais%20para%20cientistas%20de%20dados) | MySQL + dimensões (UF, município, metas) como origem relacional | `sql/01_dimensoes_mysql.sql` |
| [NoSQL para ciência de dados](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/NoSQL%20para%20ci%C3%AAncia%20de%20dados) | Eventos JSON (padrão DynamoDB Streams da aula de Big Data) para streaming de indicadores | `pipelines/streaming/producer_eventos.py` |

**Regra:** reaproveitar o *esqueleto* das aulas; domínio = Indicador Criança Alfabetizada (não o case de vendas).
