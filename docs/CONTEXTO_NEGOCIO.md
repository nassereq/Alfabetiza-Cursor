# Contexto de negócio — Tech Challenge Fase 2

## Problema

A alfabetização na infância é pilar do desenvolvimento educacional e social. O **Compromisso Nacional Criança Alfabetizada** articula União, estados, DF e municípios para que **todas as crianças estejam alfabetizadas até o final do 2º ano** do ensino fundamental.

A **Pesquisa Alfabetiza Brasil (2023)**, do INEP, definiu o ponto de corte de **743 pontos** na escala de proficiência do Saeb — nível a partir do qual a criança é considerada alfabetizada. Com base nisso foi criado o **Indicador Criança Alfabetizada** (percentual de estudantes que atingem esse patamar). A **meta nacional é 100% até 2030**.

Compreender o que move a alfabetização exige integrar:

- Metas nacionais e estaduais  
- Metas municipais  
- Dados territoriais (UF, município)  
- Microdados educacionais (alunos / avaliações)  
- Indicadores de desempenho  

## Papel da equipe

Atuar como **engenharia de dados** de uma organização pública: construir uma **pipeline híbrida (batch + streaming)** em **arquitetura medalhão** (Bronze → Silver → Gold), com qualidade, monitoramento e FinOps em nuvem.

## Valor para política pública

A camada Gold permite:

- Comparar **meta × resultado** em Brasil, UF e município  
- Acompanhar a **evolução temporal** do indicador  
- Priorizar territórios aquém da meta  
- Alimentar futuros modelos de **predição / desigualdade / clustering de vulnerabilidade**

## Entidades mínimas da pipeline

| Entidade | Papel |
|----------|--------|
| UF | Dimensão territorial estadual |
| Município | Dimensão territorial local |
| Meta Alfabetização Brasil | Meta nacional por ano |
| Meta por UF | Meta estadual |
| Meta por Município | Meta local |
| Dados de alunos | Microdados / proficiência |
| Indicador município | Resultado observado (% alfabetizados) |

Fonte de referência: [Base dos Dados — Indicador Criança Alfabetizada](https://basedosdados.org/).
