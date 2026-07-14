# Roteiro por estágios — Tech Challenge Fase 2 (Alfabetiza-Cursor)

Documento mestre para **entender**, **replicar** e **terminar** o projeto.  
Organize o trabalho em estágios. Não pule a ordem na primeira vez.

**Projeto:** `FIAP/Alfabetiza-Cursor`  
**Enunciado:** `[IAST] - Tech Challenge - Fase 2.pdf`  
**Fonte de dados:** [Avaliação da Alfabetização — Base dos Dados](https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72)

---

## Mapa rápido

| Estágio | Nome | Status típico hoje |
|--------|------|--------------------|
| 1 | Entender o desafio e o domínio | Feito (docs + guias) |
| 2 | Criar o repositório e a estrutura | Feito |
| 3 | Implementar medalhão local (Bronze → Silver → Gold) | Feito (com amostras) |
| 4 | Batch + streaming + qualidade + FinOps (docs) | Feito |
| 5 | Material didático e roteiro de vídeo | Feito |
| 6 | Git com branches / merges estilo PR | Feito (local) |
| 7 | Trocar amostras pela Base dos Dados real | **Feito** (municipio/uf + pipeline `--fonte raw`) |
| 8 | Evidência de cloud (AWS/GCP/Azure) | **A fazer** |
| 9 | Publicar GitHub com PRs reais | **Feito** (https://github.com/nassereq/Alfabetiza-Cursor) |
| 10 | Vídeo executivo + entrega no AVA | **A fazer** |

- **Estágios 1–6:** como o projeto foi criado (para replicar no futuro).  
- **Estágios 7–10:** o que falta para fechar conforme o PDF oficial.

---

# PARTE A — Como o projeto foi criado (replicar)

## Estágio 1 — Entender o desafio e o domínio

### Objetivo
Saber *o que* entregar e *por que* os dados existem, antes de escrever código.

### O que fazer
1. Ler o PDF do Tech Challenge (Fase 2).
2. Anotar: ponto de corte **743**, meta **2030**, pipeline **híbrida**, medalhão **Bronze/Silver/Gold**.
3. Listar entidades: UF, município, metas (Brasil/UF/município), alunos, indicador.
4. Abrir a página da Base dos Dados (link acima) e entender que a fonte oficial é o Inep / Avaliação da Alfabetização.

### Entregáveis deste estágio
- [ ] Contexto mental claro (ou `docs/CONTEXTO_NEGOCIO.md` preenchido)
- [ ] Checklist do enunciado (o que é obrigatório vs opcional)

### No repositório (já existe)
- `docs/CONTEXTO_NEGOCIO.md`
- `docs/Guia_Didatico_Tech_Challenge_Fase2_Alfabetizacao.pdf` (resumo)
- `docs/Guia_Extensivo_Aulas_POSTECH_e_Tech_Challenge_Fase2.pdf` (aulas + projeto)

---

## Estágio 2 — Criar o repositório e a estrutura

### Objetivo
Ter uma pasta Git com camadas e pastas alinhadas ao enunciado e às aulas POSTECH.

### O que fazer
1. Criar pasta `Alfabetiza-Cursor` (ex.: dentro de `FIAP/`).
2. `git init` e branch `main`.
3. Criar a estrutura:

```text
Alfabetiza-Cursor/
  README.md
  requirements.txt
  .gitignore
  docs/
  diagrams/
  notebooks/
  pipelines/batch/
  pipelines/streaming/
  quality/
  sql/
  data/sample|raw|bronze|silver|gold/
  infra/
  references/
  reports/
  scripts/
  logs/
```

4. Ligar o workspace do Cursor a essa pasta.

### Entregáveis
- [ ] Repo local com pastas e `.gitignore`
- [ ] `requirements.txt` básico (pandas, pyarrow, etc.)

### No repositório (já existe)
- Estrutura acima + `references/MAPA_AULAS.md` (liga as 4 aulas POSTECH ao código)

---

## Estágio 3 — Medalhão local (Bronze → Silver → Gold)

### Objetivo
Ter uma pipeline que **roda no PC**, gera camadas e produtos Gold do enunciado.

### O que fazer
1. Gerar ou obter dados de entrada (`data/sample` no protótipo).
2. **Bronze:** gravar bruto + metadados (`_data_ingestao`, `_fonte`) em Parquet particionado.
3. **Silver:** limpar, tipar, deduplicar, integrar indicador × meta × município.
4. **Gold:** materializar:
   - indicador por município  
   - comparação meta × resultado (UF / Brasil)  
   - evolução temporal  
5. Orquestrar com um comando único.

### Comandos (replicação)
```powershell
cd "…\FIAP\Alfabetiza-Cursor"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m pipelines.run_pipeline --with-streaming
python -m pipelines.monitor_health
```

### Entregáveis
- [ ] Scripts `load_bronze.py`, `load_silver.py`, `load_gold.py`
- [ ] Saídas em `data/bronze|silver|gold` e preview em `reports/gold_preview/`
- [ ] Pipeline summary em `logs/`

### No repositório (já existe)
- `pipelines/batch/generate_sample_data.py`
- `pipelines/batch/load_*.py`
- `pipelines/run_pipeline.py`
- `notebooks/01_a_04_medalhao.ipynb`

---

## Estágio 4 — Híbrido, qualidade e FinOps

### Objetivo
Cobrir os requisitos modernos do PDF: batch + streaming, qualidade, custo e monitoramento básico.

### O que fazer
1. **Batch:** ingestão periódica das tabelas históricas.
2. **Streaming:** producer de eventos (atualização de indicador); file-sink e/ou Kafka.
3. **Qualidade:** duplicidade, nulos, chaves, consistência entre tabelas.
4. Documentar FinOps (Parquet, partições, compute sob demanda, estimativa de custo).
5. Health check (latência, volume, falhas).

### Entregáveis
- [ ] `pipelines/streaming/producer_eventos.py` (+ consumer opcional)
- [ ] `quality/validate.py` com `passed=true`
- [ ] `docs/FINOPS_E_MONITORAMENTO.md` + seção no README
- [ ] Template cloud (`pipelines/batch/glue_jobs_template.py`, `infra/`)

### No repositório (já existe)
- Tudo acima, validado localmente com amostras

---

## Estágio 5 — Documentação didática e roteiro de vídeo

### Objetivo
Conseguir estudar e apresentar sem depender de ter visto 100% das aulas.

### O que fazer
1. README completo (contexto, arquitetura, trade-offs, IA, como rodar).
2. Diagrama / fluxo de dados.
3. Guias PDF (resumo + extensivo com as 4 pastas POSTECH).
4. Roteiro do vídeo ≤ 5 min.

### Entregáveis
- [ ] `README.md` alinhado ao PDF do desafio
- [ ] `docs/ARQUITETURA.md`, `docs/ROTEIRO_VIDEO.md`
- [ ] PDFs em `docs/`

### Regenerar PDFs
```powershell
python scripts/generate_guia_didatico_pdf.py
python scripts/generate_guia_extensivo_pdf.py
```

---

## Estágio 6 — Git com evolução visível

### Objetivo
Cumprir a exigência de commits, branches e integração estilo PR.

### O que fazer
1. Trabalhar em branches `feat/...` (bronze, silver, gold, docs).
2. Commits pequenos e descritivos.
3. Integrar na `main` com merge (idealmente PR no GitHub — ver Estágio 9).

### No repositório (já existe localmente)
- Branches `feat/*` e merges `--no-ff` na `main`
- `docs/GIT_WORKFLOW.md`

---

# PARTE B — O que falta para terminar (fechar a entrega)

## Estágio 7 — Base dos Dados real (prioridade 1)

### Objetivo
Substituir (ou complementar) as amostras sintéticas pelos dados oficiais do enunciado.

### Passos didáticos
1. **Criar projeto no Google Cloud** e copiar o **Project ID** (`billing_project_id`).  
   Guia: https://basedosdados.org/docs/access_data_bq  
2. **Instalar** `basedosdados` no venv do projeto.  
3. **Extrair tabelas leves primeiro:**
   - dataset: `br_inep_avaliacao_alfabetizacao`
   - tabelas: `municipio`, `uf`
   - salvar em `data/raw/bd_municipio.csv`, `data/raw/bd_uf.csv`
4. **Mapear colunas** (ano, id_municipio, indicador, meta se existir) → atualizar `docs/DICIONARIO_DADOS.md`.  
5. **Só depois** extrair `alunos` (começar com `limit=` para explorar).  
6. **Adaptar** `load_bronze` / fetch para ler `data/raw` em vez de só `data/sample`.  
7. **Ajustar Silver** aos nomes reais das colunas.  
8. **Rodar** pipeline + qualidade de novo.

### Critério de pronto
- [x] CSV reais em `data/raw/`
- [x] Bronze/Silver/Gold rodando com esses dados
- [x] README cita Base dos Dados com link e dataset_id/table_id

### Como repetir
```powershell
python -m pipelines.batch.fetch_basedosdados
# ou, se os brutos já existem:
python scripts/extract_basedosdados_municipio_uf.py
python -m pipelines.batch.map_basedosdados
python -m pipelines.run_pipeline --fonte raw --with-streaming
```

Mapeamento: `pipelines/batch/map_basedosdados.py` (`taxa_alfabetizacao` → `pct_alfabetizados`, `serie=2`, `rede=5`).

---

## Estágio 8 — Evidência de implementação em nuvem

### Objetivo
Atender “implementar em AWS / GCP / Azure” (não só código local).

### Opções (escolha uma e documente)
1. **AWS (alinhada à aula ETL):** buckets S3 SOR/SOT/SPEC + job Glue (mesmo que 1 entidade demo).  
2. **GCP:** dados já nascem no BigQuery (Base dos Dados) + export para GCS / job agendado.  
3. **Mínimo defensável:** arquitetura documentada + template executável + *prints* / log de uma execução cloud.

### Critério de pronto
- [ ] README com diagrama cloud e trade-offs
- [ ] Pelo menos uma evidência de execução/deploy (print, log, job ID)
- [ ] Seção FinOps com estimativa realista

### Já existe como base
- `pipelines/batch/glue_jobs_template.py`
- `infra/README.md`
- `docs/ARQUITETURA.md`

---

## Estágio 9 — GitHub público + PRs reais

### Objetivo
Histórico Git **visível na internet**, com Pull Requests.

### Passos
1. Criar repo público (ex.: `fiap-alfabetiza-fase2`).  
2. `git remote add origin …` e `git push -u origin main`.  
3. Abrir branch `feat/...`, push, `gh pr create`, merge.  
4. Colar o link do repo no README e no AVA.

### Critério de pronto
- [ ] Repo público abre sem login
- [ ] Pelo menos 1–2 PRs mergeados com descrição
- [ ] Commits mostram evolução (bronze → silver → gold → docs)

---

## Estágio 10 — Vídeo e submissão FIAP

### Objetivo
Fechar os 90% da nota: apresentação executiva + entrega formal.

### Passos
1. Ensaiar `docs/ROTEIRO_VIDEO.md` (≤ 5 min).  
2. Gravar: problema → arquitetura → valor educacional → potencial de IA.  
3. Subir vídeo (Drive / YouTube não listado / o que o AVA pedir).  
4. Enviar no AVA: link GitHub + vídeo (+ slides se pedido).  
5. Conferir prazo e identificação do grupo.

### Critério de pronto
- [ ] Vídeo ≤ 5 min, linguagem executiva
- [ ] Formulário/AVA salvo com sucesso
- [ ] Link do GitHub testado em aba anônima

---

# PARTE C — Ordem sugerida daqui pra frente

Faça nesta sequência (com calma):

1. ~~**Estágio 7** — Project ID Google + extrair `municipio`/`uf`~~ **feito**
2. ~~Mapear colunas / adaptar Bronze/Silver~~ **feito** (`--fonte raw`)
3. **Estágio 9** — publicar GitHub (pode ser em paralelo)
4. **Estágio 8** — evidência mínima de cloud
5. **Estágio 10** — vídeo + AVA
6. Opcional: extrair tabela `alunos` (com `limit=`) e enriquecer nomes IBGE

Opcional (só se sobrar tempo): enriquecimento IBGE/Censo/CadÚnico (PDF marca como opcional).

---

# PARTE D — Comandos úteis (colar e usar)

```powershell
# Ambiente
cd "C:\Users\capis\OneDrive\Área de Trabalho\FIAP\Alfabetiza-Cursor"
.\.venv\Scripts\activate

# Pipeline local (amostras)
python -m pipelines.run_pipeline --with-streaming

# Pipeline com Base dos Dados (após fetch/map)
python -m pipelines.run_pipeline --fonte raw --with-streaming

python -m pipelines.monitor_health
python -m quality.validate

# Base dos Dados
python -m pipelines.batch.fetch_basedosdados

# Guias PDF
python scripts/generate_guia_didatico_pdf.py
python scripts/generate_guia_extensivo_pdf.py
```

---

# PARTE E — Ligação com as 4 aulas POSTECH

| Aula | Pasta da turma | Onde aparece neste projeto |
|------|----------------|----------------------------|
| Arquitetura de Big Data | notebooks 01→04 medalhão | `pipelines/batch/load_*.py`, notebooks |
| ETL Pipelines | Pandas/PySpark, Kafka, Glue | `streaming/`, `glue_jobs_template.py` |
| Bancos relacionais | MySQL / DBeaver | `sql/01_dimensoes_mysql.sql` |
| NoSQL | eventos / streams | `producer_eventos.py` (JSON tipado) |

Detalhe: `references/MAPA_AULAS.md` e o PDF extensivo em `docs/`.

---

## Como usar este arquivo

- **Replicar do zero:** siga Estágios **1 → 6**.  
- **Terminar a entrega:** siga Estágios **7 → 10**.  
- **Estudar teoria:** leia os dois PDFs em `docs/` na ordem resumo → extensivo.  

Quando um estágio terminar, marque os checkboxes neste arquivo para não perder o fio.
