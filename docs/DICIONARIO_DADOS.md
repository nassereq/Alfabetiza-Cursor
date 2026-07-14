# Dicionário de dados — entidades da pipeline

## Fonte

- **Produção:** [Base dos Dados — Avaliação da Alfabetização](https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72)  
  - dataset_id: `br_inep_avaliacao_alfabetizacao`  
  - table_id: `municipio`, `uf` (e `alunos` em etapa futura)  
  - Extração: `python -m pipelines.batch.fetch_basedosdados`  
  - Brutos: `data/raw/bd_municipio.csv`, `data/raw/bd_uf.csv`
- **Demo local:** `data/sample/*.csv` gerados por `pipelines/batch/generate_sample_data.py` (mesmas chaves e tipos lógicos).

## Mapeamento Base dos Dados → pipeline

| Coluna BD | Entidade / coluna pipeline | Observação |
|-----------|----------------------------|------------|
| `ano` | `ano` | 2023–2024 na publicação atual |
| `id_municipio` | `id_municipio` (+ `id_uf` = 2 primeiros dígitos) | IBGE 7 dígitos |
| `sigla_uf` | `sigla_uf` / dim `uf` | tabela `uf` |
| `serie` | filtro `serie=2` | 2º ano do EF |
| `rede` | filtro `rede=5` | agregado com maior cobertura municipal |
| `taxa_alfabetizacao` | `pct_alfabetizados` | Indicador Criança Alfabetizada |
| `media_portugues` | `media_portugues` (Silver) | preservada no indicador |
| *(ausente)* | `meta_pct` | trajetória didática até 100% em 2030 |
| *(ausente)* | `alunos` | microdados sintéticos alinhados à taxa (até extrair `alunos`) |
| — | `ponto_corte` | 743 (Alfabetiza Brasil) |

## Chaves de relacionamento

| Chave | Tipo lógico | Usada em |
|-------|-------------|----------|
| `id_uf` | CHAR(2) IBGE | uf, municipio, metas, indicador, alunos |
| `sigla_uf` | CHAR(2) | denormalização / conferência |
| `id_municipio` | VARCHAR código IBGE | municipio, metas, indicador, alunos |
| `ano` | INT | metas, indicador, alunos |
| `id_aluno` | INT | alunos |

## Entidades

### `uf`
| Coluna | Descrição |
|--------|-----------|
| id_uf | Código IBGE da UF |
| sigla_uf | Sigla |
| nome_uf | Nome |

### `municipio`
| Coluna | Descrição |
|--------|-----------|
| id_municipio | Código IBGE |
| id_uf / sigla_uf | UF |
| nome_municipio | Nome (placeholder `Mun_{id}` até enriquecer com diretório IBGE) |

### `meta_brasil` / `meta_uf` / `meta_municipio`
| Coluna | Descrição |
|--------|-----------|
| ano | Ano de referência da meta |
| meta_pct | Meta percentual de crianças alfabetizadas |
| ponto_corte | 743 (Saeb) — quando aplicável |
| id_uf / id_municipio | Escopo territorial |

### `indicador_municipio`
| Coluna | Descrição |
|--------|-----------|
| ano, id_municipio, id_uf, sigla_uf, nome_municipio | Escopo |
| pct_alfabetizados | % que atingem o ponto de corte (`taxa_alfabetizacao` na BD) |
| ponto_corte | 743 |
| n_avaliados | Volume amostral (NA na fatia BD atual) |
| serie, rede, media_portugues | Metadados da publicação BD |

### `alunos`
| Coluna | Descrição |
|--------|-----------|
| id_aluno, ano, id_municipio, id_uf | Identificação |
| proficiencia_saeb | Nota na escala |
| alfabetizado | 1 se proficiência ≥ 743 |

## Metadados técnicos (medalhão)

| Campo | Camada | Significado |
|-------|--------|-------------|
| `_data_ingestao` | Bronze | Timestamp UTC da ingestão |
| `_fonte` | Bronze | Origem (`batch:sample`, `batch:raw`, `streaming:kafka_sim`, …) |
| `_modo` | Bronze | `batch` ou `streaming` |
| `_data_processamento` | Silver | Timestamp do tratamento |

## Qualidade esperada

- Sem duplicata em chaves naturais  
- Sem nulos em chaves e medidas principais  
- FKs município→UF, indicador→município, alunos→município  
- Anos do indicador cobertos por `meta_municipio`  

Validação automatizada: `python -m quality.validate`.
