# Tech Challenge Fase 2 — Pipeline Híbrida: Alfabetização no Brasil

Pipeline **batch + streaming** em **arquitetura medalhão** (Bronze → Silver → Gold) para o **Indicador Criança Alfabetizada**, com qualidade de dados, FinOps e preparação para análises/IA.

**Curso:** POSTECH / FIAP — AI Scientist  
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

**Cloud:** AWS S3 SOR/SOT/SPEC + Glue (padrão da aula). **Dev local:** Parquet em `data/`. **Streaming:** Kafka ou file-sink. **Dims:** MySQL (`sql/`).

## Tecnologias

| Ferramenta | Uso | Justificativa |
|------------|-----|----------------|
| Python / Pandas / PyArrow | Pipeline local | Rápido, reproduzível, barato |
| Parquet particionado | Lake | FinOps + performance de scan |
| AWS Glue + S3 | Cloud | Mesmo modelo da disciplina ETL |
| Kafka | Streaming | Aula 02_Kafka |
| MySQL | Origens relacionais | Disciplina de BD |
| JSON eventos tipados | NoSQL-like | Padrão DynamoDB Streams da aula Big Data |

## Como reproduzir (local)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

# Pipeline completa (batch + streaming simulado + qualidade + gold)
python -m pipelines.run_pipeline --with-streaming

# Health check
python -m pipelines.monitor_health
```

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

O desenvolvimento usa branches `feat/*` e PRs para `main`, com commits descritivos por camada (bronze → silver → gold → docs), conforme exigido no Tech Challenge.

## Vídeo executivo

Roteiro ≤ 5 min: [`docs/ROTEIRO_VIDEO.md`](docs/ROTEIRO_VIDEO.md).

## Mapa das aulas

[`references/MAPA_AULAS.md`](references/MAPA_AULAS.md)
