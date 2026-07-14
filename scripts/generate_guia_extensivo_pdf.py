"""Guia extensivo: 4 repositorios da POSTECH + caminho ate o Tech Challenge.

Otimizado para leitura em voz (sem cabecalho, rodape ou numero de pagina).
"""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Guia_Extensivo_Aulas_POSTECH_e_Tech_Challenge_Fase2.pdf"

FONT = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

LINKS = {
    "bigdata": "https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/Arquitetura%20de%20Big%20Data",
    "relacional": "https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/Banco%20de%20dados%20relacionais%20para%20cientistas%20de%20dados",
    "nosql": "https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/NoSQL%20para%20ci%C3%AAncia%20de%20dados",
    "etl": "https://github.com/AnaRaquelCafe/POSTECH_AI_SCIENTIST/tree/main/Fase%202/ETL%20Pipelines",
}


class GuidePDF(FPDF):
    def __init__(self) -> None:
        super().__init__(format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(16, 16, 16)
        self.add_font("Body", "", FONT)
        self.add_font("Body", "B", FONT_BOLD)

    def header(self) -> None:
        return

    def footer(self) -> None:
        return

    def h1(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.ln(3)
        self.set_font("Body", "B", 14)
        self.set_text_color(15, 45, 80)
        self.multi_cell(0, 8, text)
        self.set_x(self.l_margin)
        self.ln(3)

    def h2(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.ln(2)
        self.set_font("Body", "B", 11.5)
        self.set_text_color(25, 70, 110)
        self.multi_cell(0, 7, text)
        self.set_x(self.l_margin)
        self.ln(2)

    def p(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Body", "", 10.5)
        self.set_text_color(25, 25, 25)
        self.multi_cell(0, 6.2, text)
        self.set_x(self.l_margin)
        self.ln(2.5)


def build() -> Path:
    pdf = GuidePDF()
    pdf.add_page()

    # ===== ABERTURA =====
    pdf.h1("Guia extensivo: aulas da Pós Tech e o Tech Challenge Fase 2")
    pdf.p(
        "Este documento é um segundo guia, mais longo que o guia didático resumido. "
        "Ele ensina, passo a passo, o que você precisa entender nas quatro pastas de material "
        "da turma para concluir o projeto Alfabetiza Cursor, do Tech Challenge Fase 2."
    )
    pdf.p(
        "Foi escrito para leitura em voz alta: sem cabeçalho, sem rodapé, sem número de página, "
        "com frases completas e seções bem nomeadas."
    )
    pdf.p(
        "Os quatro materiais oficiais da turma são os seguintes. "
        "Primeiro, Arquitetura de Big Data. "
        "Segundo, Banco de dados relacionais para cientistas de dados. "
        "Terceiro, NoSQL para ciência de dados. "
        "Quarto, ETL Pipelines. "
        "Todos ficam no repositório POSTECH AI Scientist, pasta Fase 2, da Ana Raquel Café."
    )
    pdf.p(
        "O desafio da FIAP pede uma pipeline híbrida, batch mais streaming, em arquitetura medalhão, "
        "sobre o Indicador Criança Alfabetizada, com qualidade, FinOps, README completo, "
        "histórico Git com pull requests e vídeo executivo de até cinco minutos."
    )

    pdf.h1("Como estudar este guia")
    pdf.p(
        "Siga a ordem dos módulos. Em cada módulo você verá três blocos: "
        "o que a aula ensina; a teoria por trás; e como aplicar no Alfabetiza Cursor. "
        "No final há um roteiro de execução do projeto e um checklist de entrega."
    )
    pdf.p(
        "Se você perdeu aulas, não tente assistir tudo de uma vez. "
        "Este texto já organiza o mínimo necessário para defender o trabalho com segurança."
    )

    # ===== MODULO 0 =====
    pdf.h1("Módulo zero. Visão geral do que o Tech Challenge exige")
    pdf.h2("O problema de negócio em linguagem simples")
    pdf.p(
        "O Brasil tem o Compromisso Nacional Criança Alfabetizada. "
        "A meta é alfabetizar todas as crianças até o fim do segundo ano, até dois mil e trinta. "
        "A Pesquisa Alfabetiza Brasil definiu o ponto de corte setecentos e quarenta e três "
        "na escala Saeb. O Indicador Criança Alfabetizada é o percentual de estudantes nesse patamar."
    )
    pdf.p(
        "Para apoiar políticas públicas, é preciso integrar metas nacionais, estaduais e municipais, "
        "dados de território, microdados de alunos e indicadores de desempenho. "
        "Essa integração é o trabalho de engenharia de dados do desafio."
    )
    pdf.h2("Entregáveis que não podem faltar")
    pdf.p(
        "Código da pipeline com camadas Bronze, Silver e Gold. "
        "Ingestão batch e streaming. "
        "Scripts de qualidade. "
        "Implementação ou demonstração em nuvem, preferencialmente AWS alinhada à aula. "
        "README com contexto, arquitetura, tecnologias, trade-offs, monitoramento, FinOps e uso em IA. "
        "Histórico Git com branches e pull requests. "
        "Vídeo executivo de até cinco minutos."
    )
    pdf.h2("Onde cada aula entra no desafio")
    pdf.p(
        "Arquitetura de Big Data ensina o medalhão e o fluxo um, dois, três, quatro. "
        "Bancos relacionais ensinam dimensões, chaves e SQL, úteis para UF, município e metas. "
        "NoSQL ensina o formato de eventos que alimenta o braço streaming. "
        "ETL Pipelines ensina ETL com Pandas e PySpark, Kafka e jobs Glue na AWS com buckets SOR, SOT e SPEC."
    )

    # ===== MODULO 1 RELACIONAL =====
    pdf.h1("Módulo 1. Banco de dados relacionais")
    pdf.p(
        "Material da turma: pasta Banco de dados relacionais para cientistas de dados. "
        "Há guia de instalação MySQL e DBeaver, e uma pasta app com script SQL e gerador de dados."
    )

    pdf.h2("O que esta disciplina quer que você saiba")
    pdf.p(
        "Um banco relacional organiza dados em tabelas com linhas e colunas. "
        "Cada tabela representa uma entidade do mundo real, por exemplo município ou meta anual. "
        "Relações entre tabelas são feitas por chaves."
    )
    pdf.p(
        "Chave primária identifica unicamente uma linha. "
        "Exemplo: o código IBGE do município. "
        "Chave estrangeira garante que um valor em uma tabela exista em outra. "
        "Exemplo: a meta municipal só pode referenciar um município que exista na dimensão município."
    )
    pdf.p(
        "Normalização evita repetir a mesma informação em vários lugares. "
        "Em vez de repetir o nome do município em todas as linhas de resultado, "
        "guardamos o nome na dimensão município e usamos só o identificador nos fatos."
    )

    pdf.h2("Por que isso importa no Tech Challenge")
    pdf.p(
        "O enunciado pede entidades como UF, município, meta Brasil, meta por UF, meta por município "
        "e dados de alunos. Isso é naturalmente modelável como dimensões e fatos. "
        "Mesmo que a pipeline rode em lake e Parquet, o raciocínio relacional continua válido "
        "na Silver e na Gold."
    )

    pdf.h2("Como estudar o material da turma")
    pdf.p(
        "Instale MySQL e DBeaver com o guia da pasta. "
        "Abra o arquivo globaltech database ponto sql para ver como a aula cria tabelas e relacionamentos. "
        "Observe tipos de dados, chaves e nomes de colunas. "
        "Não copie o domínio de vendas da aula. Copie o estilo de modelagem."
    )

    pdf.h2("Como aplicar no Alfabetiza Cursor")
    pdf.p(
        "No projeto, o arquivo SQL de dimensões MySQL, na pasta sql, cria dim UF, dim município "
        "e fatos de meta e indicador, além de uma view que compara meta e resultado. "
        "Use isso para explicar no README que as origens relacionais alimentam o lake. "
        "Na prática local, as mesmas entidades também existem como CSV em data sample."
    )
    pdf.p(
        "Exercício sugerido. No DBeaver, rode o SQL do projeto. "
        "Depois importe os CSV de UF e município. "
        "Faça um SELECT que junte município com meta. "
        "Isso fixa a ideia de join, que a Silver fará em escala."
    )

    # ===== MODULO 2 NOSQL =====
    pdf.h1("Módulo 2. NoSQL para ciência de dados")
    pdf.p(
        "Material da turma: pasta NoSQL para ciência de dados. "
        "No GitHub há pouco código; o README aponta para material no Google Drive. "
        "O padrão prático de eventos NoSQL também aparece no material de Arquitetura de Big Data, "
        "na simulação de DynamoDB Streams."
    )

    pdf.h2("O que é NoSQL, em termos simples")
    pdf.p(
        "NoSQL cobre bancos que não seguem o modelo clássico só de tabelas relacionais. "
        "Exemplos comuns: documentos, chave valor, colunar e grafos. "
        "DynamoDB é um banco de chave valor e documentos, muito usado em aplicações transacionais na AWS."
    )
    pdf.p(
        "Em sistemas reais, mudanças nesses bancos viram eventos. "
        "DynamoDB Streams, por exemplo, emite registros de inserção, alteração e exclusão. "
        "Esses eventos costumam chegar ao lake em JSON, muitas vezes com tipos explícitos: "
        "S para string, N para número, e NULL para valor nulo."
    )

    pdf.h2("Por que o desafio fala de streaming e eventos")
    pdf.p(
        "A alfabetização, no mundo real, também gera atualizações: nova medição, revisão de meta, "
        "correção de indicador. O enunciado pede simular ingestão quase em tempo real. "
        "Eventos NoSQL são o modelo mental certo para isso, mesmo que a fonte final seja a Base dos Dados."
    )

    pdf.h2("Como estudar")
    pdf.p(
        "Se tiver acesso ao Drive da disciplina, leia a parte de modelagem e de eventos. "
        "No material de Big Data, abra o notebook um, criação de origens transacionais, "
        "e observe o JSON no estilo DynamoDB. Entenda como from json e explode transformam "
        "evento aninhado em tabela."
    )

    pdf.h2("Como aplicar no Alfabetiza Cursor")
    pdf.p(
        "O producer de eventos cria mensagens com event name, event source e New Image, "
        "atualizando o percentual de alfabetizados de um município. "
        "A Bronze guarda o evento bruto. "
        "A Silver achata o JSON e mescla com o indicador batch. "
        "Assim você demonstra o braço streaming sem precisar de DynamoDB real."
    )
    pdf.p(
        "Exercício sugerido. Rode o producer e abra o arquivo JSON L gerado na pasta de eventos. "
        "Leia um evento em voz alta e explique cada campo. Depois rode a Silver e veja se o município "
        "atualizado mudou na tabela integrada."
    )

    # ===== MODULO 3 BIG DATA =====
    pdf.h1("Módulo 3. Arquitetura de Big Data e medalhão")
    pdf.p(
        "Material da turma: pasta Arquitetura de Big Data. "
        "Este é o coração conceitual do Tech Challenge. "
        "A aula três organiza notebooks um a quatro mais um tutorial hands on de PySpark no Databricks Free Edition."
    )

    pdf.h2("Data Lake versus Data Warehouse")
    pdf.p(
        "Data Lake guarda arquivos em grande volume, com schema flexível, bom custo e boa escala. "
        "O risco é virar pântano se não houver organização e qualidade. "
        "Data Warehouse guarda dados bem modelados para SQL e BI, com mais governança e, em geral, mais custo. "
        "Lakehouse tenta unir os dois: arquivos no lake com camada de tabela confiável, como Delta no Databricks."
    )

    pdf.h2("Arquitetura medalhão, a teoria completa")
    pdf.p(
        "Bronze é a zona raw. Você preserva o dado como chegou, ou bem próximo disso, "
        "com metadados de ingestão. Objetivo: rastreabilidade e reprocessamento."
    )
    pdf.p(
        "Silver é a zona tratada. Você limpa, tipa, padroniza, deduplica e integra. "
        "Objetivo: dataset confiável e reutilizável por vários consumidores."
    )
    pdf.p(
        "Gold é a zona analítica. Você cria tabelas prontas para dashboard, relatório e machine learning. "
        "Objetivo: responder perguntas de negócio sem o analista refazer joins complexos toda vez."
    )

    pdf.h2("O que cada notebook da aula faz")
    pdf.p(
        "Notebook um cria origens simuladas no schema origens. "
        "Simula DynamoDB, CDC ou DMS de clientes, e arquivos de vendas. "
        "Aqui ainda não existe medalhão: só a chegada do dado."
    )
    pdf.p(
        "Notebook dois lê as origens, interpreta JSON e grava tabelas bronze com dados raw "
        "e metadados de ingestão."
    )
    pdf.p(
        "Notebook três lê bronze, aplica limpeza, padronização, tipagem e deduplicação, "
        "e grava silver."
    )
    pdf.p(
        "Notebook quatro lê silver, faz join entre fatos e dimensões, agrega e grava gold."
    )
    pdf.p(
        "O tutorial hands on usa essas tabelas para ensinar select, filtro, limpeza, joins, "
        "agregações, funções de janela, performance e persistência com PySpark."
    )

    pdf.h2("Ordem de estudo recomendada nesta pasta")
    pdf.p(
        "Primeiro, leia o README da pasta para entender a ordem. "
        "Segundo, se puder, importe os notebooks no Databricks Free Edition e execute um a quatro. "
        "Terceiro, mesmo sem Databricks, leia os arquivos ponto py equivalentes e anote "
        "quais transformações acontecem em cada camada. "
        "Quarto, traduza mentalmente vendas e clientes para indicador, meta e município."
    )

    pdf.h2("Como aplicar no Alfabetiza Cursor")
    pdf.p(
        "O projeto espelha exatamente essa ordem. "
        "Geração de amostras e raw equivale às origens. "
        "Load bronze equivale ao notebook dois. "
        "Load silver equivale ao notebook três, inclusive integração. "
        "Load gold equivale ao notebook quatro, com agregações de município, UF e Brasil "
        "e evolução temporal."
    )
    pdf.p(
        "Diferença importante: o domínio não é varejo. É alfabetização. "
        "Na defesa, diga claramente: reaproveitamos o esqueleto da aula e trocamos o caso de negócio."
    )
    pdf.p(
        "Exercício sugerido. Depois de rodar a pipeline, abra um Parquet da Bronze e um da Silver "
        "do mesmo indicador. Liste três diferenças. Em seguida abra uma tabela Gold e explique "
        "qual pergunta de gestão ela responde."
    )

    # ===== MODULO 4 ETL =====
    pdf.h1("Módulo 4. ETL Pipelines")
    pdf.p(
        "Material da turma: pasta ETL Pipelines. "
        "Ela se divide em três frentes. "
        "Primeiro, pipeline ETL com Pandas e PySpark. "
        "Segundo, Kafka. "
        "Terceiro, cloud com AWS Glue."
    )

    pdf.h2("Frente A. ETL com Pandas e PySpark")
    pdf.p(
        "ETL é o ciclo extrair, transformar e carregar. "
        "Pandas é excelente para volumes menores, prototipagem e ensino. "
        "PySpark entra quando o volume cresce ou quando você está no Databricks e no Glue."
    )
    pdf.p(
        "Nos notebooks da pasta um, Pipeline ETL, a aula demonstra o fluxo completo em duas tecnologias. "
        "O aprendizado-chave não é a sintaxe: é garantir que extração, transformação e carga "
        "estejam separadas, testáveis e observáveis."
    )
    pdf.p(
        "No Alfabetiza Cursor, a implementação local usa Pandas e Parquet de propósito, "
        "para rodar sem custo e ainda assim respeitar o medalhão. "
        "Os templates Glue mostram como a mesma lógica sobe para Spark na AWS."
    )

    pdf.h2("Frente B. Kafka e streaming")
    pdf.p(
        "A pasta dois, Kafka, tem quatro demos. "
        "Parte um: setup e tópicos. "
        "Parte dois: produce e consume. "
        "Parte três: streaming com janelas e alertas. "
        "Parte quatro: confiabilidade e tempo."
    )
    pdf.p(
        "Conceitos que você precisa falar com segurança. "
        "Produtor publica eventos. "
        "Tópico é o canal. "
        "Consumidor processa. "
        "Offset marca até onde o consumidor leu. "
        "Partições permitem escala. "
        "Janelas agregam eventos por intervalo de tempo. "
        "Alertas disparam quando uma regra de negócio ou de operação é violada."
    )
    pdf.p(
        "No projeto, o streaming pode rodar de dois jeitos. "
        "Jeito didático e gratuito: file sink na Bronze de eventos. "
        "Jeito alinhado à aula: producer e consumer com Kafka local. "
        "Os dois são válidos se você explicar o conceito e mostrar evidência nos logs."
    )
    pdf.p(
        "Exercício sugerido. Leia os títulos das quatro partes Kafka e, para cada uma, "
        "escreva uma frase dizendo o que mudaria no Alfabetiza Cursor se você implementasse "
        "só aquela parte. Isso prepara respostas orais na banca."
    )

    pdf.h2("Frente C. Cloud AWS Glue e buckets SOR, SOT e SPEC")
    pdf.p(
        "A pasta três, Cloud, traz jobs etl bronze, etl silver e etl gold. "
        "Eles usam AWS Glue com Spark. "
        "Parâmetros típicos incluem nome do job, entidade e buckets."
    )
    pdf.p(
        "SOR é a zona de dados brutos, equivalente à Bronze. "
        "SOT é a zona tratada, equivalente à Silver. "
        "SPEC é a zona de consumo analítico, equivalente à Gold. "
        "Essa nomenclatura aparece na aula e deve aparecer no seu README e no vídeo."
    )
    pdf.p(
        "O job bronze da aula busca dados, por exemplo de uma API, adiciona metadados "
        "como timestamp de ingestão e escreve Parquet particionado no bucket SOR. "
        "O job silver lê SOR, tipa e limpa, e escreve no SOT. "
        "O job gold lê SOT, agrega e escreve no SPEC."
    )
    pdf.p(
        "FinOps entra aqui. "
        "Glue sob demanda evita cluster ligado o tempo todo. "
        "Parquet e partições reduzem scan. "
        "Logs e parâmetros claros evitam reexecução às cegas. "
        "Desenvolver localmente com amostras reduz custo a quase zero."
    )
    pdf.p(
        "No Alfabetiza Cursor, o arquivo glue jobs template documenta esses jobs. "
        "Mesmo que a demo principal rode local, você cumpre o requisito de desenho em nuvem "
        "explicando a arquitetura AWS e mostrando o caminho de deploy."
    )

    # ===== MODULO 5 QUALIDADE FINOPS =====
    pdf.h1("Módulo 5. Qualidade, monitoramento e FinOps")
    pdf.p(
        "Esses temas atravessam todas as aulas, embora o enunciado destaque qualidade como obrigatória "
        "e monitoramento como fortemente desejável."
    )
    pdf.h2("Qualidade")
    pdf.p(
        "Implemente e saiba explicar quatro checagens. "
        "Duplicidade por chave natural. "
        "Nulos em campos críticos. "
        "Integridade referencial entre município, UF, indicador e alunos. "
        "Consistência entre tabelas, por exemplo anos do indicador cobertos pela meta."
    )
    pdf.p(
        "No projeto, o módulo quality.validate gera um relatório JSON. "
        "A pipeline orquestrada falha se a qualidade falhar. "
        "Isso é uma boa prática de governança: não publicar Gold suja."
    )
    pdf.h2("Monitoramento")
    pdf.p(
        "Observe falhas de ingestão, volume processado, latência total e alertas. "
        "No projeto, os arquivos de log e o monitor health cobrem o básico. "
        "Na AWS, o passo natural seria CloudWatch sobre jobs Glue."
    )
    pdf.h2("FinOps")
    pdf.p(
        "Conte no README quais decisões reduzem custo: formato Parquet, particionamento, "
        "compute sob demanda, amostras locais e qualidade cedo. "
        "Traga uma estimativa de ordem de grandeza para demo acadêmica."
    )

    # ===== MODULO 6 MONTAGEM =====
    pdf.h1("Módulo 6. Como montar o projeto do zero, unindo as quatro aulas")
    pdf.p(
        "Este módulo é o roteiro prático de conclusão."
    )

    pdf.h2("Passo 1. Entender o domínio")
    pdf.p(
        "Leia o PDF do Tech Challenge e o contexto de negócio do repositório. "
        "Decore: ponto de corte setecentos e quarenta e três; meta dois mil e trinta; "
        "entidades UF, município, metas e alunos."
    )

    pdf.h2("Passo 2. Modelar como relacional")
    pdf.p(
        "Desenhe no papel dimensões e fatos, inspirado na aula de MySQL. "
        "Confirme as chaves id UF, id município e ano. "
        "Implemente ou revise o SQL do projeto."
    )

    pdf.h2("Passo 3. Definir origens e eventos NoSQL")
    pdf.p(
        "Batch: Base dos Dados ou amostras CSV. "
        "Streaming: eventos JSON de atualização do indicador, no espírito DynamoDB Streams."
    )

    pdf.h2("Passo 4. Implementar medalhão")
    pdf.p(
        "Siga a ordem da aula de Big Data: origens, bronze, silver, gold. "
        "No Alfabetiza Cursor isso já está nos scripts load. "
        "Rode a pipeline com streaming e confira as pastas data."
    )

    pdf.h2("Passo 5. Acrescentar a narrativa de ETL cloud e Kafka")
    pdf.p(
        "No README, desenhe batch mais Kafka mais Glue SOR SOT SPEC. "
        "Mostre o template Glue e o producer. "
        "Explique trade-offs: batch versus streaming; lake versus warehouse; custo versus performance."
    )

    pdf.h2("Passo 6. Qualidade, FinOps e Git")
    pdf.p(
        "Rode a validação. "
        "Escreva a seção FinOps. "
        "Garanta branches feat e merges ou pull requests na main. "
        "Há um arquivo de fluxo Git na pasta docs."
    )

    pdf.h2("Passo 7. README, vídeo e entrega")
    pdf.p(
        "Complete o README com todos os blocos do enunciado. "
        "Grave o vídeo com o roteiro de cinco minutos. "
        "Suba o repositório público e envie o que o AVA pedir."
    )

    # ===== MODULO 7 COMANDOS =====
    pdf.h1("Módulo 7. Comandos essenciais do Alfabetiza Cursor")
    pdf.p(
        "Crie e ative o ambiente virtual Python. Instale as dependências do arquivo requirements. "
        "Rode o módulo pipelines.run_pipeline com a opção with-streaming. "
        "Rode o módulo pipelines.monitor_health. "
        "Rode o módulo quality.validate se quiser ver só a qualidade. "
        "Abra os CSV em reports gold preview para a apresentação."
    )
    pdf.p(
        "Se HEALTH estiver OK e a qualidade estiver passed igual a true, "
        "a demonstração técnica local está pronta."
    )

    # ===== MODULO 8 DEFESA =====
    pdf.h1("Módulo 8. Como falar na banca ou no vídeo sem travar")
    pdf.p(
        "Estrutura sugerida de fala. "
        "Primeiro, o problema social e o indicador. "
        "Segundo, por que engenharia de dados: fontes heterogêneas. "
        "Terceiro, arquitetura híbrida e medalhão, citando a aula de Big Data. "
        "Quarto, AWS Glue e SOR SOT SPEC, citando a aula de ETL. "
        "Quinto, Kafka e eventos NoSQL para o frescor do dado. "
        "Sexto, MySQL para dimensões governadas. "
        "Sétimo, qualidade e FinOps. "
        "Oitavo, potencial de IA sobre a Gold. "
        "Nono, fechamento com valor para política pública até dois mil e trinta."
    )
    pdf.p(
        "Frase útil. "
        "Nós não reinventamos a arquitetura: adaptamos o esqueleto das disciplinas da Fase 2 "
        "ao domínio do Indicador Criança Alfabetizada."
    )

    # ===== MODULO 9 CHECKLIST =====
    pdf.h1("Módulo 9. Checklist final de conclusão")
    pdf.p(
        "Negócio. Consigo explicar o ponto de corte e a meta dois mil e trinta. "
        "Relacional. Consigo explicar chaves e dimensões UF e município. "
        "NoSQL. Consigo explicar um evento JSON de atualização. "
        "Medalhão. Consigo contrastar Bronze, Silver e Gold com exemplos do projeto. "
        "ETL. Consigo explicar batch Pandas e o caminho Glue. "
        "Kafka. Consigo explicar producer, tópico e consumer. "
        "Qualidade. Tenho relatório passed. "
        "FinOps. Tenho parágrafo de custo no README. "
        "Git. Tenho branches e histórico de integração. "
        "Vídeo. Tenho roteiro ensaiado em até cinco minutos. "
        "Repositório. README completo e pipeline reproduzível."
    )

    # ===== MODULO 10 LINKS =====
    pdf.h1("Módulo 10. Links dos quatro materiais da turma")
    pdf.p("Arquitetura de Big Data.")
    pdf.p(LINKS["bigdata"])
    pdf.p("Banco de dados relacionais para cientistas de dados.")
    pdf.p(LINKS["relacional"])
    pdf.p("NoSQL para ciência de dados.")
    pdf.p(LINKS["nosql"])
    pdf.p("ETL Pipelines.")
    pdf.p(LINKS["etl"])
    pdf.p(
        "Repositório do projeto desta entrega: pasta Alfabetiza Cursor, "
        "dentro de FIAP na Área de Trabalho do OneDrive. "
        "Há também o guia didático resumido na pasta docs, se quiser uma versão mais curta "
        "para ouvir antes da prova oral."
    )

    pdf.h1("Encerramento")
    pdf.p(
        "Se você estudar este guia na ordem dos módulos, terá a teoria das quatro disciplinas "
        "e o caminho concreto até fechar o Tech Challenge. "
        "O segredo não é memorizar cada linha de código das aulas. "
        "É entender o papel de cada peça e mostrar, no Alfabetiza Cursor, "
        "que essas peças se encaixam em uma pipeline híbrida medalhão a serviço da alfabetização."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    return OUT


if __name__ == "__main__":
    path = build()
    print(path)
