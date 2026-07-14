# Tech Challenge Fase 2 — Pipeline Híbrida: Alfabetização no Brasil

Pipeline **batch + streaming** em **arquitetura medalhão** (Bronze → Silver → Gold) para o **Indicador Criança Alfabetizada**, com qualidade de dados, FinOps e preparação para análises/IA.

**Curso:** POSTECH / FIAP — AI Scientist  
**Repositório:** https://github.com/nassereq/Alfabetiza-Cursor  
**Bases didáticas da turma:** [Arquitetura de Big Data](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/Arquitetura%20de%20Big%20Data) · [ETL Pipelines](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/ETL%20Pipelines) · [Bancos relacionais](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/Banco%20de%20dados%20relacionais%20para%20cientistas%20de%20dados) · [NoSQL](https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/NoSQL%20para%20ci%C3%AAncia%20de%20dados)

---

## Contexto do problema

O Compromisso Nacional Criança Alfabetizada busca garantir alfabetização até o fim do 2º ano. A Pesquisa Alfabetiza Brasil (INEP, 2023) fixou o ponto de corte de **743** na escala Saeb. O **Indicador Criança Alfabetizada** mede o percentual de estudantes nesse patamar; a meta nacional é **100% até 2030**.

Detalhes: [`docs/CONTEXTO_NEGOCIO.md`](docs/CONTEXTO_NEGOCIO.md).

## Arquitetura

Ingestão híbrida → medalhão → consumo analítico. Diagrama e trade-offs: [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md).

| Camada | Conteúdo |
|--------|----------|
| **Bronze** | Raw + `_data_ingestao` / `_fonte` (batch e eventos streaming) |
| **Silver** | Limpeza, chaves, integração indicador×meta |
| **Gold** | Indicador municipal, meta×resultado (UF/Brasil), evolução temporal |

**Cloud:** evidência real em **GCP BigQuery** (Base dos Dados) + template **AWS** S3 SOR/SOT/SPEC + Glue (padrão da aula). **Dev local:** Parquet em `data/`. **Streaming:** Kafka ou file-sink. **Dims:** MySQL (`sql/`).

## Tecnologias

| Ferramenta | Uso | Justificativa |
|------------|-----|----------------|
| Python / Pandas / PyArrow | Pipeline local | Rápido, reproduzível, barato |
| Parquet particionado | Lake | FinOps + performance de scan |
| AWS Glue + S3 | Cloud (template aula) | Mesmo modelo da disciplina ETL |
| GCP BigQuery | Origem + evidência cloud | Dataset público Base dos Dados; job com `job_id` |
| Kafka | Streaming | Aula 02_Kafka |
| MySQL | Origens relacionais | Disciplina de BD |
| JSON eventos tipados | NoSQL-like | Padrão DynamoDB Streams da aula Big Data |

## Como reproduzir (local)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

# Pipeline com amostras sintéticas (offline)
python -m pipelines.run_pipeline --with-streaming

# Health check
python -m pipelines.monitor_health
```

### Base dos Dados (dados reais)

Dataset: [`br_inep_avaliacao_alfabetizacao`](https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72) — tabelas `municipio` e `uf`.

Requer Project ID GCP com BigQuery ([guia de acesso](https://basedosdados.org/docs/access_data_bq)). O projeto usado no desenvolvimento: `alfabetiza-fiap-t-challenge-2` (ou `BD_BILLING_PROJECT_ID`).

```bash
# Extrai brutos + mapeia para entidades da pipeline em data/raw/
python -m pipelines.batch.fetch_basedosdados

# Ou só mapeia se bd_municipio.csv / bd_uf.csv já existirem
python -m pipelines.batch.map_basedosdados

# Pipeline com dados reais
python -m pipelines.run_pipeline --fonte raw --with-streaming
```

Mapeamento principal: `taxa_alfabetizacao` → `pct_alfabetizados` (filtro `serie=2`, `rede=5`). Metas seguem trajetória didática até 100% em 2030 (as tabelas BD não trazem coluna de meta).

Saídas:

- `data/bronze/`, `data/silver/`, `data/gold/`  
- Relatórios em `logs/`  
- CSVs Gold prontos para Excel/Power BI  

### Streaming Kafka (opcional)

```bash
pip install kafka-python
python -m pipelines.streaming.producer_eventos --kafka --n 10
python -m pipelines.streaming.consumer_eventos
```

### MySQL

Execute [`sql/01_dimensoes_mysql.sql`](sql/01_dimensoes_mysql.sql) no DBeaver e carregue CSVs de `data/sample/`.

## Qualidade de dados

`python -m quality.validate` — duplicidade, nulos, FKs, consistência entre tabelas. Ver [`docs/DICIONARIO_DADOS.md`](docs/DICIONARIO_DADOS.md).

## Monitoramento e FinOps

[`docs/FINOPS_E_MONITORAMENTO.md`](docs/FINOPS_E_MONITORAMENTO.md) — práticas de custo, estimativa mensal e sinais de observabilidade.

### Evidência cloud (GCP)

```powershell
python -m pipelines.cloud.evidence_bigquery
```

Gera `reports/cloud_evidence/` com **Job ID** BigQuery. Arquitetura e trade-offs: [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md). Infra: [`infra/README.md`](infra/README.md).

## Aplicação em IA

A Gold habilita modelos de predição de alfabetização, análise de desigualdade e apoio a políticas territoriais — sem exigir ML nesta entrega (o enunciado pede o **potencial**).

## Estrutura do repositório

```text
Alfabetiza-Cursor/
  docs/               # negócio, arquitetura, FinOps, roteiro do vídeo
  notebooks/          # espelho didático 01–04 (medalhão)
  pipelines/batch/    # bronze / silver / gold (+ template Glue)
  pipelines/streaming/# producer / consumer
  quality/            # validações
  sql/                # MySQL dimensões
  data/sample|bronze|silver|gold/
  infra/              # notas AWS / Kafka
  references/         # mapa das aulas POSTECH
  diagrams/
```

## Git e PRs

Repositório público: https://github.com/nassereq/Alfabetiza-Cursor  

O desenvolvimento usa branches `feat/*` e Pull Requests para `main`, com commits descritivos por camada (bronze → silver → gold → Base dos Dados → docs), conforme exigido no Tech Challenge.

## Guias didáticos (PDF)

1. **Resumo** (leitura rápida / voz): [`docs/Guia_Didatico_Tech_Challenge_Fase2_Alfabetizacao.pdf`](docs/Guia_Didatico_Tech_Challenge_Fase2_Alfabetizacao.pdf)  
2. **Extensivo** (4 aulas POSTECH + caminho até a entrega): [`docs/Guia_Extensivo_Aulas_POSTECH_e_Tech_Challenge_Fase2.pdf`](docs/Guia_Extensivo_Aulas_POSTECH_e_Tech_Challenge_Fase2.pdf)

**Roteiro por estágios** (Markdown): [`docs/ROTEIRO_ESTAGIOS_DO_PROJETO.md`](docs/ROTEIRO_ESTAGIOS_DO_PROJETO.md)  
**Roteiro por estágios** (PDF, leitura em voz): [`docs/Roteiro_Estagios_Tech_Challenge_Fase2.pdf`](docs/Roteiro_Estagios_Tech_Challenge_Fase2.pdf)

Regenerar:
`python scripts/generate_guia_didatico_pdf.py`  
`python scripts/generate_guia_extensivo_pdf.py`  
`python scripts/generate_roteiro_estagios_pdf.py`

## Vídeo executivo

Roteiro ≤ 5 min: [`docs/ROTEIRO_VIDEO.md`](docs/ROTEIRO_VIDEO.md).  
**Slides (PPTX):** [`docs/Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx`](docs/Apresentacao_Tech_Challenge_Fase2_Alfabetiza.pptx)  
Espelho Markdown: [`docs/APRESENTACAO_SLIDES.md`](docs/APRESENTACAO_SLIDES.md)

Regenerar slides: `python scripts/generate_apresentacao_pptx.py`

## Mapa das aulas

[`references/MAPA_AULAS.md`](references/MAPA_AULAS.md)
