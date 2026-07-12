"""
Templates AWS Glue (adaptados de ETL Pipelines/03_Cloud/etl).

Em produção, estes jobs leem/escrevem S3:
  SOR  = Bronze
  SOT  = Silver
  SPEC = Gold

Localmente, use pipelines/batch/load_*.py (Pandas + Parquet).
Os stubs abaixo documentam parâmetros e o fluxo para deploy no Glue.
"""
# ruff: noqa: E402
GLUE_BRONZE_DOC = """
Job: alfabetiza-etl-bronze
Params:
  --JOB_NAME alfabetiza-etl-bronze
  --ENTIDADE indicador_municipio
  --BUCKET_SOR <account>-alfabetiza-sor
  --SOURCE_URI s3://.../raw/indicador_municipio/

Fluxo (espelho da aula):
  1. Ler origem (API / CSV Base dos Dados / dump)
  2. Adicionar _data_ingestao, _fonte, hash de linha
  3. Escrever Parquet particionado em s3://BUCKET_SOR/bronze/ENTIDADE/dt=YYYY-MM-DD/
"""

GLUE_SILVER_DOC = """
Job: alfabetiza-etl-silver
Params:
  --JOB_NAME alfabetiza-etl-silver
  --ENTIDADE indicador_municipio
  --BUCKET_SOR <account>-alfabetiza-sor
  --BUCKET_SOT <account>-alfabetiza-sot

Fluxo:
  1. Ler Bronze SOR
  2. Tipagem, nulos, dedup, padronização de chaves
  3. Escrever SOT/silver/ENTIDADE/
"""

GLUE_GOLD_DOC = """
Job: alfabetiza-etl-gold
Params:
  --JOB_NAME alfabetiza-etl-gold
  --BUCKET_SOT <account>-alfabetiza-sot
  --BUCKET_SPEC <account>-alfabetiza-spec

Fluxo:
  1. Ler Silver integrado
  2. Agregar município / UF / Brasil + evolução temporal
  3. Escrever SPEC/gold/
"""


def describe() -> None:
    print(GLUE_BRONZE_DOC)
    print(GLUE_SILVER_DOC)
    print(GLUE_GOLD_DOC)


if __name__ == "__main__":
    describe()
