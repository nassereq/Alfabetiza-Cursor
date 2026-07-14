"""Gera PDF didatico otimizado para leitura em voz (Edge Ler em voz alta).

Sem cabecalho, rodape ou numero de pagina.
Prosa linear, frases completas, estrutura previsivel para TTS.
"""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Guia_Didatico_Tech_Challenge_Fase2_Alfabetizacao.pdf"

FONT = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


class GuidePDF(FPDF):
    def __init__(self) -> None:
        super().__init__(format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(18, 18, 18)
        self.add_font("Body", "", FONT)
        self.add_font("Body", "B", FONT_BOLD)

    def header(self) -> None:
        return

    def footer(self) -> None:
        return

    def title_block(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.ln(2)
        self.set_font("Body", "B", 14)
        self.set_text_color(20, 40, 70)
        self.multi_cell(0, 8, text)
        self.set_x(self.l_margin)
        self.ln(4)

    def subtitle(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.ln(2)
        self.set_font("Body", "B", 11)
        self.set_text_color(30, 60, 100)
        self.multi_cell(0, 7, text)
        self.set_x(self.l_margin)
        self.ln(2)

    def para(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Body", "", 11)
        self.set_text_color(25, 25, 25)
        self.multi_cell(0, 6.5, text)
        self.set_x(self.l_margin)
        self.ln(3)


def build() -> Path:
    pdf = GuidePDF()
    pdf.add_page()

    pdf.title_block("Guia didático do Tech Challenge Fase 2")
    pdf.para(
        "Este é o guia da pipeline híbrida para análise da alfabetização no Brasil. "
        "O documento explica a teoria das aulas da Pós Tech e mostra o que foi construído "
        "no repositório Alfabetiza Cursor. Foi escrito para leitura em voz alta: "
        "frases completas, ordem linear e sem cabeçalho, rodapé ou número de página."
    )
    pdf.para(
        "Como usar este material. Ouça na ordem. Cada parte começa pela teoria, o porquê, "
        "e depois explica onde isso aparece no projeto, o como."
    )

    pdf.title_block("Parte 1. Para que serve este projeto")
    pdf.para(
        "O Tech Challenge da Fase 2 pede que você atue como um time de engenharia de dados "
        "de uma organização pública. O tema é a alfabetização infantil no Brasil."
    )
    pdf.para(
        "A ideia central em uma frase é a seguinte. Existe uma meta de política pública: "
        "todas as crianças alfabetizadas até o fim do segundo ano do ensino fundamental, "
        "até o ano de dois mil e trinta. Para saber se o país está no caminho, usamos o "
        "Indicador Criança Alfabetizada."
    )
    pdf.para(
        "O ponto de corte setecentos e quarenta e três significa o seguinte. "
        "A Pesquisa Alfabetiza Brasil, do Inep, em dois mil e vinte e três, definiu que, "
        "na escala de proficiência do Saeb, a partir de setecentos e quarenta e três pontos "
        "a criança pode ser considerada alfabetizada. O indicador é o percentual de estudantes "
        "que atingem esse patamar."
    )
    pdf.para(
        "Por que precisa de uma pipeline de dados? Porque as informações estão espalhadas: "
        "metas nacionais, estaduais e municipais; cadastros de unidade federativa e município; "
        "microdados de alunos; e resultados do indicador. Sem integrar essas fontes com qualidade, "
        "um gestor não consegue comparar meta com resultado nem priorizar onde agir."
    )
    pdf.para(
        "No nosso repositório, há também o arquivo de contexto de negócio na pasta docs. "
        "A camada Gold entrega os produtos analíticos que um gestor usaria: indicador por município, "
        "comparação com a meta e evolução no tempo."
    )

    pdf.title_block("Parte 2. O que é uma pipeline de dados")
    pdf.para(
        "Pipeline é uma sequência automatizada de passos que leva o dado da origem até um formato "
        "confiável para análise. Em engenharia de dados, costumamos falar em ETL, ou seja, "
        "extrair, transformar e carregar."
    )
    pdf.para(
        "Extrair significa buscar dados da origem, por exemplo uma API, um arquivo, um banco "
        "ou a plataforma Base dos Dados. Transformar significa limpar, tipar, juntar tabelas e "
        "calcular campos. Carregar significa gravar o resultado em um armazenamento analítico."
    )
    pdf.para(
        "No lago de dados moderno, muitas vezes fazemos primeiro a carga do bruto e depois as "
        "transformações em camadas. Isso casa com a arquitetura medalhão, que veremos a seguir."
    )

    pdf.subtitle("Batch versus streaming")
    pdf.para(
        "Batch processa um volume histórico de uma vez, em janelas diárias ou semanais. "
        "É ideal para metas, municípios e séries anuais. Em geral é mais barato e mais simples."
    )
    pdf.para(
        "Streaming processa eventos contínuos, quase em tempo real. É ideal para situações como: "
        "acabou de chegar uma atualização do indicador do município X. Para isso usamos filas "
        "ou mensageria, por exemplo Kafka."
    )
    pdf.para(
        "Pipeline híbrida significa usar os dois juntos. O enunciado exige isso: históricos em batch "
        "e simulação de eventos em streaming."
    )
    pdf.para(
        "No nosso repositório, o batch está nos scripts load bronze, load silver e load gold, "
        "dentro da pasta pipelines batch. O streaming está no producer de eventos, "
        "dentro da pasta pipelines streaming. Esse producer grava eventos na Bronze e, "
        "opcionalmente, pode publicar no Kafka."
    )

    pdf.title_block("Parte 3. Arquitetura medalhão: Bronze, Silver e Gold")
    pdf.para(
        "Esta é a ideia central da disciplina Arquitetura de Big Data. A metáfora da medalha, "
        "do bronze para a prata e depois para o ouro, organiza o lago de dados em três níveis "
        "de refinamento."
    )

    pdf.subtitle("Camada Bronze, o dado bruto")
    pdf.para(
        "A Bronze guarda o que chegou, com pouca ou nenhuma transformação. Ela preserva histórico "
        "e rastreabilidade: quando o dado entrou e de onde veio. Se algo der errado na Silver, "
        "você ainda tem o original para reprocessar."
    )
    pdf.para(
        "No nosso projeto, cada entidade vira arquivo Parquet na pasta data bronze, organizada "
        "por entidade e por data. Há colunas técnicas de data de ingestão, fonte e modo, "
        "indicando se veio de batch ou de streaming."
    )

    pdf.subtitle("Camada Silver, o dado tratado e integrado")
    pdf.para(
        "A Silver faz limpeza: trata nulos, tipagem, padronização de nomes e textos. "
        "Também faz deduplicação e validação de chaves, como identificador de município, "
        "identificador de unidade federativa e ano. Por fim, integra: junta o indicador com a meta "
        "e com a dimensão município."
    )
    pdf.para(
        "No nosso projeto, o script load silver gera, entre outras, a tabela indicador meta integrado, "
        "já com o campo de diferença em relação à meta e o campo que indica se a meta foi atingida."
    )

    pdf.subtitle("Camada Gold, o dado analítico")
    pdf.para(
        "A Gold contém tabelas agregadas e fatos prontos para dashboard, consulta SQL e, no futuro, "
        "aprendizado de máquina. Não é lugar de JSON bagunçado: é um contrato estável para o negócio."
    )
    pdf.para(
        "No nosso projeto, a Gold entrega o mínimo pedido pelo enunciado: "
        "indicador de alfabetização por município; "
        "comparativo entre meta e resultado por unidade federativa e pelo Brasil; "
        "e evolução temporal por município, unidade federativa e Brasil."
    )
    pdf.para(
        "Uma analogia simples ajuda. Bronze é a caixa de entrada do correio. "
        "Silver são as cartas abertas, organizadas e grampeadas por assunto. "
        "Gold é o relatório executivo que a diretoria lê."
    )

    pdf.subtitle("Correspondência com a aula de nuvem")
    pdf.para(
        "Na aula de ETL em AWS Glue, os buckets se chamam SOR, SOT e SPEC. "
        "É o mesmo medalhão com outros nomes. SOR corresponde à Bronze. "
        "SOT corresponde à Silver. SPEC corresponde à Gold. "
        "Os templates estão no arquivo glue jobs template, na pasta pipelines batch."
    )

    pdf.title_block("Parte 4. Data Lake, Warehouse e Lakehouse")
    pdf.para(
        "Data Lake armazena arquivos em larga escala, por exemplo no S3 da Amazon, "
        "em formatos como Parquet. É flexível e barato, mas sem governança vira pântano de dados."
    )
    pdf.para(
        "Data Warehouse é um banco analítico estruturado, como BigQuery ou Redshift. "
        "É ótimo para SQL e painéis de negócio, com esquemas mais rígidos e, em geral, custo maior."
    )
    pdf.para(
        "Lakehouse une o melhor dos dois: arquivos no lake com uma camada de tabela, "
        "como Delta, permitindo qualidade e consultas. Databricks, usado na aula, é um exemplo "
        "de plataforma lakehouse."
    )
    pdf.para(
        "No nosso repositório, o desenvolvimento local usa a pasta data como um mini lake em Parquet. "
        "A nuvem alvo do enunciado é AWS com S3 e Glue. A demo didática espelha os notebooks "
        "Databricks um a quatro da turma."
    )

    pdf.title_block("Parte 5. Bancos relacionais e MySQL")
    pdf.para(
        "A disciplina de bancos relacionais ensina tabelas, chaves primárias, chaves estrangeiras e SQL. "
        "Isso não desaparece no Big Data. Dimensões estáveis, como unidade federativa, município e metas, "
        "frequentemente nascem ou são governadas em um banco relacional e depois entram no lake."
    )
    pdf.para(
        "Chave primária identifica unicamente uma linha, por exemplo o identificador do município. "
        "Chave estrangeira garante que o município da meta existe na dimensão município. "
        "Normalização separa quem é o município de qual foi o resultado no ano X."
    )
    pdf.para(
        "No nosso repositório, o arquivo SQL de dimensões MySQL cria as tabelas de unidade federativa, "
        "município e fatos de meta e indicador, além de uma view que antecipa a ideia da Gold."
    )

    pdf.title_block("Parte 6. NoSQL e eventos em JSON")
    pdf.para(
        "Bancos NoSQL, por exemplo DynamoDB, e streams de eventos muitas vezes entregam JSON "
        "com tipos explícitos, como S para texto e N para número. Na aula de Big Data isso é "
        "simulado antes da Bronze."
    )
    pdf.para(
        "No streaming do projeto, o producer gera eventos no mesmo espírito: uma imagem nova com "
        "atualização do percentual de alfabetizados de um município. A Bronze guarda o evento. "
        "A Silver achata o JSON e mescla com o indicador batch. A última escrita vence."
    )
    pdf.para(
        "No nosso repositório, isso está no producer de eventos. "
        "Para rodar junto com a pipeline, use o módulo pipelines.run_pipeline com a opção with-streaming."
    )

    pdf.title_block("Parte 7. Kafka, mensageria para streaming")
    pdf.para(
        "Kafka é um sistema de log distribuído de mensagens. Produtores publicam eventos em tópicos. "
        "Consumidores leem esses eventos. Isso desacopla quem gera o dado de quem processa."
    )
    pdf.para(
        "Tópico é o canal nomeado, por exemplo alfabetiza.indicador.updates. "
        "Producer é quem publica, no nosso caso a simulação de atualização de indicador. "
        "Consumer é quem lê e grava na Bronze."
    )
    pdf.para(
        "Para estudar sem pagar nuvem, o projeto também tem um file sink: grava os mesmos eventos "
        "na pasta data bronze events indicador. O conceito pedagógico é o mesmo."
    )

    pdf.title_block("Parte 8. Qualidade de dados")
    pdf.para(
        "Dado errado em dashboard vira decisão errada. O enunciado pede validações mínimas: "
        "verificar duplicidade, ou seja, a mesma chave duas vezes; "
        "detectar valores ausentes em campos críticos; "
        "validar chaves de relacionamento; "
        "e checar consistência entre tabelas, por exemplo se o ano do indicador existe na meta."
    )
    pdf.para(
        "No nosso repositório, rode o módulo quality.validate. "
        "O resultado fica no arquivo quality report, dentro da pasta logs. "
        "A orquestração falha se a qualidade não passar."
    )

    pdf.title_block("Parte 9. FinOps, custo em nuvem")
    pdf.para(
        "FinOps é a disciplina de gastar bem na nuvem. Não significa deixar de usar nuvem. "
        "Significa usar o recurso certo, no tamanho certo, só quando precisa."
    )
    pdf.para(
        "Práticas importantes: usar Parquet com particionamento para ler menos bytes e pagar menos; "
        "usar computação sob demanda, como Glue ou Databricks serverless, pagando enquanto roda; "
        "desenvolver com amostras locais para ter custo zero de nuvem no dia a dia; "
        "e aplicar qualidade cedo, para evitar reprocessar a Gold e os painéis à toa."
    )
    pdf.para(
        "No nosso repositório, o arquivo de FinOps e monitoramento na pasta docs traz uma estimativa "
        "aproximada de cinco a vinte dólares por mês para uma demo acadêmica em AWS, "
        "além dos sinais de monitoramento: latência, volume e falhas."
    )

    pdf.title_block("Parte 10. Mapa das aulas da Pós Tech para as pastas do projeto")
    pdf.para(
        "O repositório da turma é o POSTECH AI Scientist, pasta Fase 2, da Ana Raquel Café."
    )
    pdf.para(
        "A pasta Arquitetura de Big Data, com notebooks um a quatro do medalhão, corresponde "
        "aos notebooks e aos scripts load da pasta pipelines batch do nosso projeto."
    )
    pdf.para(
        "A pasta ETL Pipelines, com Pandas, PySpark, Kafka e Glue, corresponde às pastas "
        "pipelines batch e pipelines streaming, e ao template de jobs Glue."
    )
    pdf.para(
        "A pasta de bancos relacionais corresponde ao script SQL de dimensões MySQL."
    )
    pdf.para(
        "A pasta de NoSQL corresponde ao formato JSON do producer de eventos."
    )
    pdf.para(
        "Há mais detalhes no arquivo mapa aulas, dentro da pasta references."
    )

    pdf.title_block("Parte 11. O que cada parte do repositório faz")
    pdf.para(
        "O arquivo config, em pipelines, guarda caminhos, o ponto de corte setecentos e quarenta e três, "
        "e os nomes de recursos AWS e Kafka."
    )
    pdf.para(
        "O script generate sample data cria arquivos CSV didáticos para rodar offline. "
        "O load bronze faz a ingestão bruta com metadados. "
        "O load silver faz limpeza, deduplicação e integração. "
        "O load gold materializa os produtos analíticos."
    )
    pdf.para(
        "Os scripts de streaming contêm o producer e o consumer de eventos. "
        "O run pipeline orquestra tudo. "
        "O monitor health faz a checagem de saúde depois da execução. "
        "O validate, na pasta quality, aplica as regras de qualidade do enunciado."
    )
    pdf.para(
        "A pasta data sample tem as entradas versionadas. "
        "As pastas bronze, silver e gold dentro de data recebem as saídas locais. "
        "A pasta reports gold preview tem CSV da Gold para abrir no Excel ou Power BI. "
        "A pasta docs tem os textos de entrega: negócio, arquitetura, FinOps, vídeo e Git."
    )

    pdf.title_block("Parte 12. Como rodar o projeto")
    pdf.para(
        "No diretório do projeto Alfabetiza Cursor, crie um ambiente virtual Python. "
        "No Windows, ative o ambiente e instale as dependências a partir do arquivo requirements."
    )
    pdf.para(
        "Em seguida rode o módulo pipelines.run_pipeline com a opção with-streaming. "
        "Depois rode o módulo pipelines.monitor_health."
    )
    pdf.para(
        "Se a saída mostrar health OK, e se o quality report mostrar passed igual a true, "
        "a pipeline de ponta a ponta funcionou. Abra os CSV em reports gold preview para ver os resultados."
    )
    pdf.subtitle("O que acontece ao rodar, em ordem")
    pdf.para(
        "Primeiro, o sistema gera ou usa as amostras e copia para data raw. "
        "Segundo, a Bronze batch grava Parquet particionado. "
        "Terceiro, o producer cria cerca de dez eventos de atualização do indicador. "
        "Quarto, a Silver trata, mescla eventos e integra com metas. "
        "Quinto, a qualidade valida chaves, nulos e duplicatas. "
        "Sexto, a Gold materializa as tabelas analíticas e os CSV de preview."
    )

    pdf.title_block("Parte 13. Aplicação em inteligência artificial")
    pdf.para(
        "Você não precisa entregar um modelo treinado nesta fase. Precisa explicar como a Gold "
        "habilita inteligência artificial depois."
    )
    pdf.para(
        "Predição: estimar o percentual de alfabetizados futuro por município, usando histórico, "
        "meta, unidade federativa e volume avaliado. "
        "Desigualdade: encontrar grupos de municípios cronicamente abaixo da meta. "
        "Política pública: priorizar intervenção onde a diferença entre meta e resultado é maior."
    )
    pdf.para(
        "Uma frase pronta para o vídeo é esta. A engenharia de dados entrega um ativo confiável na Gold. "
        "A ciência de dados consome esse ativo para prever e priorizar."
    )

    pdf.title_block("Parte 14. Git com branches e pull requests")
    pdf.para(
        "O enunciado exige histórico Git mostrando evolução, branches e pull requests. "
        "No Alfabetiza Cursor já existem branches com prefixo feat e merges na main no estilo de "
        "pull request. Veja o arquivo de fluxo Git na pasta docs para publicar no GitHub."
    )

    pdf.title_block("Parte 15. Roteiro rápido do vídeo de cinco minutos")
    pdf.para(
        "Nos primeiros quarenta e cinco segundos, apresente o problema: alfabetização, "
        "ponto de corte setecentos e quarenta e três, meta dois mil e trinta, e dados fragmentados."
    )
    pdf.para(
        "Nos noventa segundos seguintes, explique a arquitetura: batch mais streaming, "
        "mais Bronze, Silver e Gold. Mostre o diagrama."
    )
    pdf.para(
        "Nos sessenta segundos seguintes, mostre o valor: comparação entre meta e resultado "
        "e priorização territorial. Mostre um CSV da Gold."
    )
    pdf.para(
        "Nos quarenta e cinco segundos seguintes, fale do potencial de inteligência artificial: "
        "predição, desigualdade e política baseada em evidência."
    )
    pdf.para(
        "Nos trinta segundos finais, faça o fechamento. "
        "O texto completo está no roteiro de vídeo, na pasta docs."
    )

    pdf.title_block("Parte 16. Glossário mínimo")
    pdf.para(
        "Pipeline é o fluxo automatizado de dados. "
        "Ingestão é a entrada dos dados no sistema. "
        "Schema é a estrutura de colunas de uma tabela. "
        "Partição é uma fatia de dados, por exemplo por data, para ler menos. "
        "Parquet é um formato colunar compacto, padrão em lakes. "
        "Deduplicação é remover linhas repetidas pela chave. "
        "Join, ou merge, é juntar tabelas por chave comum. "
        "Observabilidade é saber se a pipeline falhou, atrasou ou processou pouco. "
        "FinOps é gestão de custo em nuvem. "
        "Base dos Dados é uma plataforma de dados públicos brasileiros, origem sugerida pelo enunciado."
    )

    pdf.title_block("Parte 17. Checklist de estudo se as aulas ficaram pela metade")
    pdf.para(
        "Estude nesta ordem, cerca de uma a duas horas por bloco. "
        "Bloco A, negócio: esta Parte 1 e o arquivo de contexto de negócio. "
        "Bloco B, medalhão: esta Parte 3; rode a pipeline e inspecione as pastas bronze, silver e gold. "
        "Bloco C, híbrida: Partes 2 e 7; olhe o producer de eventos. "
        "Bloco D, qualidade e FinOps: Partes 8 e 9; veja o quality report e o documento de FinOps. "
        "Bloco E, contar a história: roteiro de vídeo e o README."
    )
    pdf.para(
        "Mensagem final. Você não precisa ter assistido cem por cento das aulas para defender o projeto. "
        "Precisa entender o porquê do medalhão, a diferença entre batch e streaming, "
        "o valor da Gold para política pública, e saber rodar e explicar o que está no Alfabetiza Cursor. "
        "Este guia foi feito para isso."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    return OUT


if __name__ == "__main__":
    path = build()
    print(path)
