"""PDF didatico: roteiro por estagios do Tech Challenge Fase 2.

Otimizado para Ler em voz alta (Edge): sem cabecalho, rodape ou numero de pagina.
"""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Roteiro_Estagios_Tech_Challenge_Fase2.pdf"

FONT = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


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

    pdf.h1("Roteiro por estágios — Tech Challenge Fase 2")
    pdf.p(
        "Este documento ensina, em ordem, como o projeto Alfabetiza Cursor foi criado "
        "e o que ainda falta para concluir a entrega. "
        "Foi escrito para leitura em voz alta: sem cabeçalho, sem rodapé, sem número de página, "
        "com frases completas e estágios bem nomeados."
    )
    pdf.p(
        "O enunciado oficial é o PDF IAST Tech Challenge Fase 2. "
        "A fonte de dados oficial é a Base dos Dados, conjunto Avaliação da Alfabetização, do Inep. "
        "O projeto fica na pasta FIAP, Alfabetiza Cursor."
    )
    pdf.p(
        "Como usar. "
        "Os estágios um a seis mostram como replicar o que já foi feito. "
        "Os estágios sete a dez mostram o que falta para fechar a nota. "
        "Faça na ordem na primeira vez."
    )

    pdf.h1("Visão geral dos dez estágios")
    pdf.p(
        "Estágio um: entender o desafio e o domínio. Já feito nos documentos. "
        "Estágio dois: criar o repositório e a estrutura. Já feito. "
        "Estágio três: implementar o medalhão local, Bronze, Silver e Gold. Já feito com amostras. "
        "Estágio quatro: batch, streaming, qualidade e FinOps. Já feito. "
        "Estágio cinco: material didático e roteiro de vídeo. Já feito. "
        "Estágio seis: Git com branches e merges estilo pull request. Já feito no computador local. "
        "Estágio sete: trocar amostras pelos dados reais da Base dos Dados. Ainda a fazer. "
        "Estágio oito: evidência de cloud em AWS, GCP ou Azure. Ainda a fazer. "
        "Estágio nove: publicar no GitHub com pull requests reais. Ainda a fazer. "
        "Estágio dez: vídeo executivo e entrega no AVA. Ainda a fazer."
    )

    # ===== PARTE A =====
    pdf.h1("Parte A. Como o projeto foi criado, para replicar")

    pdf.h2("Estágio 1. Entender o desafio e o domínio")
    pdf.p(
        "Objetivo: saber o que entregar e por que os dados existem, antes de escrever código."
    )
    pdf.p(
        "O que fazer. "
        "Leia o PDF do Tech Challenge Fase 2. "
        "Anote o ponto de corte setecentos e quarenta e três, a meta dois mil e trinta, "
        "a pipeline híbrida e o medalhão Bronze, Silver e Gold. "
        "Liste as entidades: unidade federativa, município, metas nacional, estadual e municipal, "
        "alunos e indicador. "
        "Abra a página da Base dos Dados do conjunto Avaliação da Alfabetização e entenda "
        "que a fonte oficial é o Inep."
    )
    pdf.p(
        "Entregáveis deste estágio. "
        "Contexto mental claro, ou o arquivo de contexto de negócio preenchido. "
        "Checklist do enunciado separando o que é obrigatório do que é opcional."
    )
    pdf.p(
        "No repositório já existem o contexto de negócio, o guia didático resumido em PDF "
        "e o guia extensivo das aulas POSTECH."
    )

    pdf.h2("Estágio 2. Criar o repositório e a estrutura")
    pdf.p(
        "Objetivo: ter uma pasta com Git e camadas alinhadas ao enunciado e às aulas da Pós Tech."
    )
    pdf.p(
        "O que fazer. "
        "Crie a pasta Alfabetiza Cursor, por exemplo dentro de FIAP. "
        "Inicie o Git e use a branch main. "
        "Crie as pastas docs, diagrams, notebooks, pipelines batch, pipelines streaming, "
        "quality, sql, data com sample, raw, bronze, silver e gold, "
        "infra, references, reports, scripts e logs. "
        "Crie o README, o requirements e o gitignore. "
        "Abra essa pasta como workspace no Cursor."
    )
    pdf.p(
        "Entregáveis. "
        "Repositório local com pastas e gitignore. "
        "Arquivo requirements com pandas, pyarrow e demais dependências básicas. "
        "No projeto atual também existe o mapa das aulas na pasta references."
    )

    pdf.h2("Estágio 3. Medalhão local, Bronze, Silver e Gold")
    pdf.p(
        "Objetivo: ter uma pipeline que roda no computador, gera as três camadas "
        "e os produtos analíticos pedidos no enunciado."
    )
    pdf.p(
        "O que fazer. "
        "Primeiro, gere ou obtenha dados de entrada. No protótipo usamos data sample. "
        "Na Bronze, grave o dado bruto com metadados de data de ingestão e fonte, "
        "em Parquet particionado por data. "
        "Na Silver, limpe, tipe, deduplique e integre indicador com meta e município. "
        "Na Gold, materialize o indicador por município, a comparação entre meta e resultado "
        "por unidade federativa e pelo Brasil, e a evolução temporal. "
        "Orquestre tudo com um comando único."
    )
    pdf.p(
        "Como replicar no terminal. "
        "Entre na pasta do projeto. "
        "Crie e ative o ambiente virtual Python. "
        "Instale as dependências do arquivo requirements. "
        "Rode o módulo pipelines.run_pipeline com a opção with-streaming. "
        "Rode o módulo pipelines.monitor_health."
    )
    pdf.p(
        "Entregáveis. "
        "Scripts load bronze, load silver e load gold. "
        "Saídas nas pastas data bronze, silver e gold, e preview em reports gold preview. "
        "Relatório da pipeline na pasta logs. "
        "Também há o notebook que espelha os passos um a quatro do medalhão."
    )

    pdf.h2("Estágio 4. Híbrido, qualidade e FinOps")
    pdf.p(
        "Objetivo: cobrir batch mais streaming, qualidade de dados, custo e monitoramento básico."
    )
    pdf.p(
        "O que fazer. "
        "No batch, ingira as tabelas históricas periodicamente. "
        "No streaming, use um producer de eventos de atualização do indicador, "
        "com file sink e, se quiser, Kafka. "
        "Na qualidade, verifique duplicidade, nulos, chaves e consistência entre tabelas. "
        "Documente FinOps: Parquet, particionamento, compute sob demanda e estimativa de custo. "
        "Faça um health check de latência, volume e falhas."
    )
    pdf.p(
        "Entregáveis. "
        "Producer de eventos e consumer opcional. "
        "Script de qualidade com passed igual a true. "
        "Documento de FinOps e monitoramento, mais a seção correspondente no README. "
        "Template de jobs Glue e notas em infra. "
        "No estado atual, isso já foi validado localmente com amostras."
    )

    pdf.h2("Estágio 5. Documentação didática e roteiro de vídeo")
    pdf.p(
        "Objetivo: estudar e apresentar sem depender de ter visto todas as aulas."
    )
    pdf.p(
        "O que fazer. "
        "Escreva um README completo com contexto, arquitetura, trade-offs, aplicação em IA "
        "e como reproduzir. "
        "Inclua diagrama ou fluxo de dados. "
        "Gere os PDFs resumido e extensivo. "
        "Escreva o roteiro do vídeo de até cinco minutos."
    )
    pdf.p(
        "Entregáveis. "
        "README alinhado ao PDF do desafio. "
        "Arquivos de arquitetura e roteiro de vídeo. "
        "PDFs na pasta docs. "
        "Para regenerar os PDFs, rode os scripts generate guia didatico e generate guia extensivo."
    )

    pdf.h2("Estágio 6. Git com evolução visível")
    pdf.p(
        "Objetivo: cumprir a exigência de commits, branches e integração estilo pull request."
    )
    pdf.p(
        "O que fazer. "
        "Trabalhe em branches com prefixo feat, por exemplo bronze, silver, gold e docs. "
        "Faça commits pequenos e descritivos. "
        "Integre na main com merge. "
        "No GitHub, o ideal é abrir pull requests de verdade. Isso fica no estágio nove."
    )
    pdf.p(
        "No repositório local já existem branches feat e merges na main, "
        "além do arquivo de fluxo Git na pasta docs."
    )

    # ===== PARTE B =====
    pdf.h1("Parte B. O que falta para terminar a entrega")

    pdf.h2("Estágio 7. Base dos Dados real. Prioridade um")
    pdf.p(
        "Objetivo: substituir ou complementar as amostras sintéticas pelos dados oficiais do enunciado."
    )
    pdf.p(
        "Passo um deste estágio. "
        "Crie um projeto no Google Cloud e copie o Project ID. "
        "Esse valor será o billing project id. "
        "Não é necessário cartão no modo sandbox. Há cerca de um terabyte gratuito de consulta por mês."
    )
    pdf.p(
        "Passo dois. "
        "No ambiente virtual do projeto, instale o pacote basedosdados."
    )
    pdf.p(
        "Passo três. "
        "Extraia primeiro as tabelas leves. "
        "O dataset é br inep avaliacao alfabetizacao. "
        "As tabelas iniciais são municipio e uf. "
        "Salve em data raw, por exemplo bd municipio ponto csv e bd uf ponto csv."
    )
    pdf.p(
        "Passo quatro. "
        "Olhe as colunas e monte um mapa mental: ano, identificador de município, "
        "indicador de alfabetização e meta, se existir. "
        "Atualize o dicionário de dados."
    )
    pdf.p(
        "Passo cinco. "
        "Só depois extraia alunos. Comece com limite para explorar, porque é microdado e pesa mais."
    )
    pdf.p(
        "Passo seis. "
        "Adapte o load bronze, ou um script de fetch, para ler data raw em vez de depender só de data sample."
    )
    pdf.p(
        "Passo sete. "
        "Ajuste a Silver aos nomes reais das colunas."
    )
    pdf.p(
        "Passo oito. "
        "Rode de novo a pipeline e a qualidade."
    )
    pdf.p(
        "Critério de pronto do estágio sete. "
        "Há CSV reais em data raw. "
        "Bronze, Silver e Gold rodam com esses dados. "
        "O README cita a Base dos Dados com link, dataset id e table id."
    )
    pdf.p(
        "Exemplo de ideia do código de extração. "
        "Importe basedosdados. "
        "Defina o Project ID. "
        "Use read table para municipio e uf. "
        "Grave os CSV em data raw. "
        "Na primeira execução o navegador pede autorização da conta Google."
    )

    pdf.h2("Estágio 8. Evidência de implementação em nuvem")
    pdf.p(
        "Objetivo: atender o requisito de implementar em AWS, GCP ou Azure, não só no computador."
    )
    pdf.p(
        "Opção um, alinhada à aula de ETL: Amazon S3 com buckets SOR, SOT e SPEC, mais um job Glue, "
        "mesmo que seja uma demonstração de uma entidade. "
        "Opção dois: Google Cloud, aproveitando que a Base dos Dados já está no BigQuery, "
        "com exportação para storage ou job agendado. "
        "Opção três, mínimo defensável: arquitetura documentada, template executável "
        "e evidência de uma execução cloud, como print ou log."
    )
    pdf.p(
        "Critério de pronto. "
        "README com diagrama cloud e trade-offs. "
        "Pelo menos uma evidência de execução ou deploy. "
        "Seção FinOps com estimativa realista. "
        "No projeto já existem o template Glue, o README de infra e o documento de arquitetura."
    )

    pdf.h2("Estágio 9. GitHub público com pull requests reais")
    pdf.p(
        "Objetivo: histórico Git visível na internet, com pull requests."
    )
    pdf.p(
        "O que fazer. "
        "Crie um repositório público, por exemplo fiap alfabetiza fase dois. "
        "Adicione o remote origin e faça push da main. "
        "Abra uma branch feat, envie, crie o pull request, descreva a mudança e faça o merge. "
        "Cole o link do repositório no README e no AVA."
    )
    pdf.p(
        "Critério de pronto. "
        "O repositório abre sem login. "
        "Há pelo menos um ou dois pull requests mergeados com descrição. "
        "Os commits mostram evolução: bronze, silver, gold e docs."
    )

    pdf.h2("Estágio 10. Vídeo executivo e submissão na FIAP")
    pdf.p(
        "Objetivo: fechar a apresentação executiva e a entrega formal, que concentram grande parte da nota."
    )
    pdf.p(
        "O que fazer. "
        "Ensaie o roteiro de vídeo de até cinco minutos. "
        "Grave falando de problema de negócio, arquitetura da solução, "
        "valor para análises educacionais e potencial de inteligência artificial. "
        "Use linguagem para liderança, sem entrar em código. "
        "Suba o vídeo onde o AVA pedir. "
        "Envie link do GitHub, vídeo e o que mais a plataforma solicitar. "
        "Confira prazo e identificação do grupo."
    )
    pdf.p(
        "Critério de pronto. "
        "Vídeo de até cinco minutos em linguagem executiva. "
        "Formulário do AVA salvo com sucesso. "
        "Link do GitHub testado em aba anônima."
    )

    # ===== PARTE C =====
    pdf.h1("Parte C. Ordem sugerida a partir de agora")
    pdf.p(
        "Primeiro, faça o estágio sete: criar o Project ID no Google e extrair municipio e uf. "
        "Em seguida, ainda no sete, mapeie as colunas e adapte Bronze e Silver. "
        "Depois, publique no GitHub, estágio nove. Pode começar o push assim que tiver o primeiro CSV real. "
        "Em seguida, monte a evidência mínima de cloud, estágio oito. "
        "Por fim, grave o vídeo e entregue no AVA, estágio dez."
    )
    pdf.p(
        "Opcional, só se sobrar tempo: enriquecimento com IBGE, Censo Escolar ou Cadastro Único. "
        "O PDF do desafio marca isso como opcional."
    )

    pdf.h1("Parte D. Ligação com as quatro aulas da Pós Tech")
    pdf.p(
        "Arquitetura de Big Data, notebooks um a quatro do medalhão, aparece nos scripts load "
        "e nos notebooks do projeto. "
        "ETL Pipelines, com Pandas, PySpark, Kafka e Glue, aparece na pasta streaming "
        "e no template Glue. "
        "Bancos relacionais aparece no SQL de dimensões MySQL. "
        "NoSQL e eventos aparece no producer de eventos em JSON tipado."
    )
    pdf.p(
        "Há mais detalhes no arquivo mapa aulas, na pasta references, "
        "e no guia extensivo em PDF, na pasta docs."
    )

    pdf.h1("Parte E. Como usar este roteiro no dia a dia")
    pdf.p(
        "Para replicar o projeto do zero, siga os estágios um a seis. "
        "Para terminar a entrega da disciplina, siga os estágios sete a dez. "
        "Para estudar a teoria, ouça primeiro o guia didático resumido e depois o guia extensivo. "
        "Quando um estágio terminar, marque mentalmente ou anote no arquivo Markdown "
        "Roteiro Estagios do Projeto, na pasta docs, para não perder o fio."
    )
    pdf.p(
        "Mensagem final. "
        "O medalhão local e a documentação já existem. "
        "O caminho crítico agora é dados reais da Base dos Dados, "
        "depois GitHub, cloud e vídeo. "
        "Faça um estágio por vez."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    return OUT


if __name__ == "__main__":
    print(build())
