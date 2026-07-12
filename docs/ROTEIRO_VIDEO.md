# Roteiro — Vídeo executivo (até 5 minutos)

Linguagem para liderança / stakeholders. Sem código na tela.

**Duração-alvo:** 4 min 30 s – 5 min.

---

## Bloco 1 — Problema de negócio (~45 s)

> A alfabetização até o 2º ano é meta de política pública. Com o ponto de corte de **743** no Saeb, o Indicador Criança Alfabetizada mostra o percentual de crianças alfabetizadas — e a meta é **100% até 2030**. Hoje os dados estão fragmentados: metas nacionais, estaduais, municipais, território e microdados. Sem integrar essas fontes, a gestão não prioriza onde agir.

## Bloco 2 — Arquitetura (~90 s)

> Construímos uma **pipeline híbrida** em arquitetura **medalhão**:
> - **Batch** carrega históricos da Base dos Dados (e dimensões em MySQL).  
> - **Streaming** (Kafka) simula atualizações quase em tempo real do indicador.  
> - **Bronze** guarda o bruto com rastreabilidade.  
> - **Silver** limpa, valida e integra.  
> - **Gold** entrega três produtos: indicador por município, comparação meta×resultado e evolução temporal.  
> Em nuvem usamos o padrão **AWS S3 + Glue** (SOR/SOT/SPEC), o mesmo da disciplina de ETL.

*(Mostrar diagrama `diagrams/pipeline.txt` / mermaid da arquitetura.)*

## Bloco 3 — Valor para análises educacionais (~60 s)

> Com a Gold, um gestor vê em segundos quais municípios estão **abaixo da meta**, a trajetória ano a ano e o gap agregado por UF e Brasil. Isso transforma dados públicos em **prioridade operacional** — não só em relatório retrospectivo.

*(Mostrar 1 tabela Gold CSV ou gráfico simples meta×resultado.)*

## Bloco 4 — Potencial para IA (~45 s)

> A mesma base Gold alimenta modelos de **predição de alfabetização**, estudos de **desigualdade** e **clusters de vulnerabilidade**. A engenharia de dados entrega o ativo; a ciência de dados consome com confiança.

## Bloco 5 — Fechamento (~30 s)

> Em resumo: pipeline híbrida, medalhão, qualidade e FinOps — para que a política Criança Alfabetizada seja guiada por evidência até 2030. Obrigado.

---

## Checklist de gravação

- [ ] Diagrama da pipeline visível  
- [ ] Mencionar ponto de corte 743 e meta 2030  
- [ ] Mencionar batch + streaming + Bronze/Silver/Gold  
- [ ] Mostrar um produto Gold  
- [ ] Citar potencial de IA (sem entrar em hiperparâmetros)  
- [ ] Cronometrar ≤ 5 min  
