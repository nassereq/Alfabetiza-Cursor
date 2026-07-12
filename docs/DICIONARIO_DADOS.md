# Dicionário de dados — entidades da pipeline

## Fonte

- **Produção:** [Base dos Dados](https://basedosdados.org/) (BigQuery / pacote `basedosdados`) — Indicador Criança Alfabetizada e dimensões territoriais.
- **Demo local:** `data/sample/*.csv` gerados por `pipelines/batch/generate_sample_data.py` (mesmas chaves e tipos lógicos).

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
| nome_municipio | Nome |

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
| pct_alfabetizados | % que atingem o ponto de corte |
| ponto_corte | 743 |
| n_avaliados | Volume amostral / avaliado |

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
| `_fonte` | Bronze | Origem (`batch:sample`, `streaming:kafka_sim`, …) |
| `_modo` | Bronze | `batch` ou `streaming` |
| `_data_processamento` | Silver | Timestamp do tratamento |

## Qualidade esperada

- Sem duplicata em chaves naturais  
- Sem nulos em chaves e medidas principais  
- FKs município→UF, indicador→município, alunos→município  
- Anos do indicador cobertos por `meta_municipio`  

Validação automatizada: `python -m quality.validate`.
