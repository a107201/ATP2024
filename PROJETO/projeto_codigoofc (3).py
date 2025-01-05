import json #trabalhar com ficheiros json (passar a list,dict,...)
from collections import Counter #contar elementos de listas, strings, etc.),retorna um dicionário onde as chaves são os elementos e os valores representam suas frequências.
from collections import defaultdict # Importa o defaultdict para facilitar a contagem de publicações 
import FreeSimpleGUI as sg #criar interfaces gráficas (janelas, caixas de texto, botões, tabelas)
import matplotlib.pyplot as plt #criar gráficos
import os #verificar se certa coisa existe

#Carregar a BD para a memória
file_path = r"C:\Users\adria\OneDrive\Documentos\programação\ata_medica_papers.json"
f = open(file_path, encoding='utf-8')
amp = json.load(f)

def carregaAMP(fnome):
    f = open(file_path, encoding='utf-8')
    amp = json.load(f)
    return amp

mybd = carregaAMP("ata_medica_papers.json")

#Guardar a BD em memória no ficheiro
def guardarAMP(fnome, bd):
    fout = open('./datasets' + fnome, "w")
    json.dump(bd, fout)
    fout.close()

# ---------------------------------------------------- MENU -----------------------------------------------------------

# Função para criar o menu principal -----------------------------------------------
def main_menu():
    sg.theme("SandyBeach")
    layout = [
        [sg.Text("Menu Principal", font=("Arial", 24), justification="center", expand_x=True)],
        [sg.Button("Help", key="-HELP-", size=(20, 2))],
        [sg.Button("Criar Publicação", key="-CRIARPUB-", size=(20, 2))],
        [sg.Button("Consulta de Publicação", key="-CONSULTADEPUB-", size=(20, 2))],
        [sg.Button("Listar Publicações", key="-LISTARPUB-", size=(20, 2))],
        [sg.Button("Eliminar Publicação", key="-ELIMINARPUBLICACOES-", size=(20, 2))],
        [sg.Button("Relatório de Estatísticas", key="-RELATORIOESTATISTICAS-", size=(20, 2))],
        [sg.Button("Listar Autores", key="-LISTARAUTORES-", size=(20, 2))],
        [sg.Button("Importar Publicações", key="-IMPORTARPUBLICACOES-", size=(20, 2))],
        [sg.Button("Exportar dados", key="-EXPORTARDADOS-", size=(20, 2))]
    
    ]

    return sg.Window("Menu Principal", layout, font=('Arial', 16), finalize=True)


# primeiro botão do menu principal - Help
def help():
    help_text = (
        "- Criar Publicação: Insira informações sobre uma publicação para adicioná-la ao sistema.\n"
        "- Consulta de Publicação: Insira o identificador de uma publicação para visualizá-la.\n"
        "- Listar Publicações: Lista todas as publicações disponíveis.\n"
        "- Eliminar Publicação: Remova uma publicação específica.\n"
        "- Relatório de Estatísticas: Gere relatórios sobre métricas das publicações.\n"
        "- Listar Autores: Exiba uma lista de autores cadastrados.\n"
        "- Importar Publicações: Importe publicações de um arquivo.\n"
        "- Exportar dados: Permite a exportação parcial para o ficheiro dos registos resultantes de uma pesquisa com filtro."
    )
    sg.popup("Help", help_text, font=("Arial", 14), title="Help", keep_on_top=True)

    return 


# segundo botão do menu principal - Criar Publicação -----------------------------------------------

def criarPub(users):
    file_name = file_path

    # Verificar se o arquivo existe e carregar dados
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf8") as file_in:
            content = file_in.read().strip()
            if content:
                users = json.loads(content)
    else:
        users = []

    layout = [
        [sg.Text("Criar Publicação", font=("Arial", 20), justification="center", expand_x=True)],
        [sg.Text("Título:"), sg.InputText(key='-TITULO-', size=(40, 1))],
        [sg.Text("Resumo:"), sg.InputText(key='-RESUMO-', size=(40, 1))],
        [sg.Text("Palavras-chave:"), sg.InputText(key='-PALAVRAS-', size=(40, 1))],
        [sg.Text("DOI:"), sg.InputText(key='-DOI-', size=(40, 1))],
        [sg.Text("Autores:"), sg.InputText(key='-AUTORES-', size=(40, 1))],
        [sg.Text("Afiliação:"), sg.InputText(key='-AFILIACAO-', size=(40, 1))],
        [sg.Text("URL do PDF:"), sg.InputText(key='-PDF-', size=(40, 1))],
        [sg.Text("Data de Publicação (YYYY-MM-DD):"), sg.InputText(key='-DATA-', size=(40, 1))],
        [sg.Button("Cancelar"), sg.Button("Criar")]
    ]

    window = sg.Window("Criar Publicação", layout, font=("Arial", 14), finalize=True)

    continuar = True  # Variável de controle para o loop

    while continuar:
        event, values = window.read()

        if event in ("Cancelar", sg.WIN_CLOSED):
            continuar = False

        elif event == "Criar":
            titulo = values["-TITULO-"].strip()
            resumo = values["-RESUMO-"].strip()
            palavras_chave = values["-PALAVRAS-"].strip()
            doi = values["-DOI-"].strip()
            autores = values["-AUTORES-"].strip()
            afiliacao = values["-AFILIACAO-"].strip()
            pdf = values["-PDF-"].strip()
            data = values["-DATA-"].strip()

            if not (titulo and resumo and palavras_chave and doi and autores and afiliacao and pdf and data):
                sg.popup("Por favor, preencha todos os campos.", title="Erro", font=("Arial", 14), keep_on_top=True)
            else:
                # Validação manual da data
                partes_data = data.split("-")
                if len(partes_data) != 3 or not all(p.isdigit() for p in partes_data):
                    sg.popup("Formato de data inválido. Use YYYY-MM-DD.", title="Erro", font=("Arial", 14), keep_on_top=True)
                else:
                    ano, mes, dia = int(partes_data[0]), int(partes_data[1]), int(partes_data[2])
                    if not (1 <= mes <= 12 and 1 <= dia <= 31):
                        sg.popup("Mês ou dia fora do intervalo.", title="Erro", font=("Arial", 14), keep_on_top=True)
                    elif mes in [4, 6, 9, 11] and dia > 30:
                        sg.popup("Mês especificado tem no máximo 30 dias.", title="Erro", font=("Arial", 14), keep_on_top=True)
                    elif mes == 2 and (dia > 29 or (dia == 29 and ano % 4 != 0)):
                        sg.popup("Data inválida em fevereiro.", title="Erro", font=("Arial", 14), keep_on_top=True)
                    else:
                        nova_publicacao = {
                            "title": titulo,
                            "abstract": resumo,
                            "keywords": palavras_chave,
                            "doi": doi,
                            "authors": [
                                {
                                    "name": autores,
                                    "affiliation": afiliacao,
                                },
                            ],
                            "pdf": pdf,
                            "publish_date": data
                        }

                        users.append(nova_publicacao)

                        with open(file_name, "w", encoding="utf8") as file_out:
                            json.dump(users, file_out, indent=4, ensure_ascii=False)

                        sg.popup("Publicação criada com sucesso!", title="Sucesso", font=("Arial", 14), keep_on_top=True)

    window.close()


# terceiro botão do menu principal - Consultar Publicação -----------------------------------------------

def consultarPub():
    # Nome do arquivo de publicações
    file_name = file_path

    # Carregar publicações existentes
    users = []
    if os.path.exists(file_name):  # Verifica se o arquivo existe
        with open(file_name, "r", encoding="utf8") as file_in:
            content = file_in.read().strip()
            if content:
                users = json.loads(content)
    else:
        sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    # Layout da interface
    layout = [
        [sg.Text("Consulta de Publicações", font=("Arial", 20), justification="center", expand_x=True)],
        [sg.Text("Filtro:"), sg.Combo(
            values=["Título", "Autores", "Afiliação", "Palavras-chave", "Data de Publicação"],
            default_value="Título", key='-FILTRO-', readonly=True, size=(30, 1))],
        [sg.Text("Valor:"), sg.InputText(key='-VALOR-', size=(40, 1))],
        [sg.Button("Fechar"), sg.Button("Listar Todos"), sg.Button("Filtrar")]
    ]

    window = sg.Window("Consulta de Publicações", layout, font=("Arial", 14), finalize=True)

    # Variável de controle para manter a janela aberta
    janela_ativa = True

    # Loop principal
    while janela_ativa:
        event, values = window.read()

        # Fechar janela
        if event in ("Fechar", sg.WIN_CLOSED):
            janela_ativa = False

        # Listar todas as publicações
        elif event == "Listar Todos":
            if users:
                detalhes = "\n\n".join(
                    [f"{pub.get('title', 'Sem título')} - {pub.get('publish_date', 'Sem data')}" for pub in users]
                )
                sg.popup_scrolled(detalhes, title="Lista de Publicações", font=("Arial", 14), size=(50, 20), keep_on_top=True)
            else:
                sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)

        # Filtrar publicações
        elif event == "Filtrar":
            filtro_selecionado = values["-FILTRO-"]
            valor = values["-VALOR-"].strip().lower()

            # Mapear filtro para a chave correspondente no JSON
            filtro_mapeado = {
                "Título": "title",
                "Autores": "authors",
                "Afiliação": "affiliation",
                "Palavras-chave": "keywords",
                "Data de Publicação": "publish_date"
            }.get(filtro_selecionado, "")

            if not filtro_mapeado:
                sg.popup("Filtro inválido selecionado.", title="Erro", font=("Arial", 14), keep_on_top=True)
            else:
                # Aplicar filtro
                resultados = [
                    pub for pub in users if valor in str(pub.get(filtro_mapeado, "")).lower()
                ]

                # Exibir resultados filtrados
                if resultados:
                    detalhes = "\n\n".join(
                        [f"Título: {pub.get('title', 'Sem título')}\nAutores: {pub.get('authors', 'Desconhecidos')}\n"
                         f"Afiliação: {pub.get('affiliation', 'Desconhecida')}\nData de Publicação: {pub.get('publish_date', 'Sem data')}\n"
                         f"Palavras-chave: {pub.get('keywords', 'Não informadas')}" for pub in resultados]
                    )
                    sg.popup_scrolled(detalhes, title="Publicações Encontradas", font=("Arial", 14), size=(50, 20), keep_on_top=True)
                else:
                    sg.popup("Nenhuma publicação encontrada com os critérios informados.", title="Erro", font=("Arial", 14), keep_on_top=True)

    window.close()

# quarto botão do menu principal - Consultar/Listar Publicações -----------------------------------------------

def listarPub():
    file_name = file_path
    users = []  # Inicializa a lista de publicações

    # Verificar se o arquivo existe
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf8") as file_in:
            content = file_in.read().strip()
            if content:  # Verifica se o arquivo não está vazio
                users = json.loads(content)
    else:
        sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    # Define os valores da lista para o Combo
    filtro = ["Título", "Resumo", "Palavras-chave", "Autores", "Afiliação", "DOI", "PDF", "Data de Publicação", "URL"]

    # Layout para consulta de publicação
    layout = [
        [sg.Text("Consulta de Publicação", font=("Arial", 24), justification="center", expand_x=True)],
        [sg.Text("Selecione o critério de filtro:"), sg.Combo(values=filtro, default_value="Título", key='-FILTRO-', readonly=True, size=(30, 1))],
        [sg.Text("Introduza um identificador para filtrar:"), sg.InputText(key="-IDENTIFICADOR-", size=(50, 1))],  # p.e. uma das palavras chave do titulo
        [sg.Button("Cancelar"), sg.Button("Consultar")],
        [sg.Listbox(values=[], size=(80, 15), key="-RESULTADO-", select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
    ]

    window = sg.Window("Consulta de Publicação", layout, font=('Arial', 16), finalize=True)

    continue_event = True  # Variável de controle para o loop

    while continue_event:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            continue_event = False  # Atualiza o controle para sair do loop

        elif event == "Consultar":
            filtro_selecionado = values["-FILTRO-"]
            identificador = values["-IDENTIFICADOR-"].strip().lower()

            # Filtrar as publicações de acordo com o critério selecionado
            resultado_filtrado = []

            for pub in users:
                if filtro_selecionado == "Título" and identificador in pub.get("title", "").lower():
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "Resumo" and identificador in pub.get("abstract", "").lower():
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "Palavras-chave" and identificador in pub.get("keywords", "").lower():
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "Autores" and any(identificador in author.get("name", "").lower() for author in pub.get("authors", [])):
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "Afiliação" and any(identificador in author.get("affiliation", "").lower() for author in pub.get("authors", [])):
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "DOI" and identificador in pub.get("doi", "").lower():
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "PDF" and identificador in pub.get("pdf", "").lower():
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "Data de Publicação" and identificador in pub.get("publish_date", "").lower():
                    resultado_filtrado.append(pub["title"])
                elif filtro_selecionado == "URL" and identificador in pub.get("url", "").lower():
                    resultado_filtrado.append(pub["title"])

            # Atualizar a lista de resultados
            if resultado_filtrado:
                window["-RESULTADO-"].update(resultado_filtrado)
            else:
                window["-RESULTADO-"].update(["Nenhuma publicação encontrada."])

    window.close()


# quinto botão do menu principal - Eliminar Publicações -----------------------------------------------

def elimPub():
    # Carregar publicações existentes
    file_name = file_path
    users = []  # Inicializa a lista de publicações

    # Verificar se o arquivo existe
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf8") as file_in:
            content = file_in.read().strip()
            if content:  # Verifica se o arquivo não está vazio
                users = json.loads(content)
    else:
        sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    # Layout para a janela de eliminação
    layout = [
        [sg.Text("Eliminar Publicação", font=("Arial", 24), justification="center", expand_x=True)],
        [sg.Text("O título da publicação que deseja eliminar:"), sg.InputText(key="-IDENTIFICADOR-", size=(50, 1))],
        [sg.Button("Cancelar"), sg.Button("Eliminar")]
    ]

    window = sg.Window("Eliminar Publicação", layout, font=('Arial', 16), finalize=True)

    continue_event = True  # Variável de controle para sair do loop

    while continue_event:
        event, values = window.read()

        # Fechar a janela ou cancelar
        if event in ("Cancelar", sg.WIN_CLOSED):
            continue_event = False  # Atualiza o flag para sair do loop

        # Eliminar a publicação ao pressionar "Eliminar"
        elif event == "Eliminar":
            identificador = values["-IDENTIFICADOR-"].strip()  # Obtém o identificador digitado
            resultado = next(
                (pub for pub in users if pub.get("doi") == identificador or pub.get("title") == identificador),
                None
            )

            if resultado:
                # Confirmar a eliminação
                confirmacao = sg.popup("Tem certeza que deseja eliminar esta publicação?", 
                                       title="Confirmação", 
                                       font=("Arial", 14), 
                                       keep_on_top=True,
                                       custom_text=("Sim", "Não"))  # Altera os botões para "Sim" e "Não"
                if confirmacao == "Sim":  # Verifica se o usuário escolheu "Sim"
                    users.remove(resultado)  # Remove a publicação da lista

                    # Salva a lista atualizada no arquivo JSON
                    with open(file_name, "w", encoding="utf8") as file_out:
                        json.dump(users, file_out, indent=4, ensure_ascii=False)

                    sg.popup("Publicação eliminada com sucesso!", title="Sucesso", font=("Arial", 14), keep_on_top=True)
            else:
                sg.popup("Publicação não encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)  # Mensagem de erro      

            continue_event = False  # Atualiza o flag para sair do loop
        
    window.close()  # Fecha a janela



# sexto botão do menu principal - Relatório de Estatísticas -----------------------------------------------

def relEstat():
    # Carregar publicações existentes
    arquivo_publicacoes = file_path
    publicacoes = []  # Inicializa a lista de publicações

    # Verificar se o arquivo existe
    if os.path.exists(arquivo_publicacoes): # Verifica se o arquivo existe
        with open(arquivo_publicacoes, "r", encoding="utf8") as file_in:
            conteudo = file_in.read().strip()
            if conteudo:  # Verifica se o arquivo não está vazio
                publicacoes = json.loads(conteudo)
    else:
        sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    # Extrair dados para análise
    palavras_chave = []
    autores = []
    anos = []
    meses = []
    publicacoes_por_autor_por_ano = defaultdict(lambda: defaultdict(int))
    palavras_chave_por_ano = defaultdict(list)

    for pub in publicacoes:
        if "keywords" in pub and pub["keywords"]:
            palavras_chave.extend(pub["keywords"].split(","))
        
        if "authors" in pub:
            for autor in pub["authors"]:
                autores.append(autor["name"])

        if "publish_date" in pub:
            data_publicacao = pub["publish_date"]
            ano = data_publicacao.split("-")[0]
            mes = data_publicacao.split("-")[1]
            anos.append(ano)
            meses.append(f"{ano}-{mes}")

            if "authors" in pub:
                for autor in pub["authors"]:
                    publicacoes_por_autor_por_ano[autor["name"]][ano] += 1

            if ano not in palavras_chave_por_ano:
                palavras_chave_por_ano[ano] = []
            if "keywords" in pub and pub["keywords"]:
                palavras_chave_por_ano[ano].extend(pub["keywords"].split(","))

    # Contagem de palavras-chave, autores, e anos
    contagem_palavras_chave = {}
    for palavra in palavras_chave:
        contagem_palavras_chave[palavra] = contagem_palavras_chave.get(palavra, 0) + 1

    contagem_autores = {}
    for autor in autores:
        contagem_autores[autor] = contagem_autores.get(autor, 0) + 1

    contagem_anos = {}
    for ano in anos:
        contagem_anos[ano] = contagem_anos.get(ano, 0) + 1

    contagem_meses = {}
    for mes in meses:
        contagem_meses[mes] = contagem_meses.get(mes, 0) + 1

    # Top 20 autores e palavras-chave
    top_autores = sorted(contagem_autores.items(), key=lambda x: x[1], reverse=True)[:20]
    top_palavras_chave = sorted(contagem_palavras_chave.items(), key=lambda x: x[1], reverse=True)[:20]

    # Layout para a janela de relatórios
    layout = [
            [sg.Text("Gerar Relatórios", font=("Arial", 24), justification="center", expand_x=True)],
            [sg.Button("Distribuição de Publicações por Ano")],
            [sg.Button("Distribuição por Mês do Ano")],
            [sg.Button("Publicações por Autor (Top 20)")],
            [sg.Button("Distribuição de Palavras-chave por Frequência")],
            [sg.Button("Palavras-chave mais frequentes por Ano")],
            [sg.Button("Cancelar")]
        ]

    janela = sg.Window("Gerar Relatórios", layout, font=('Arial', 16), finalize=True)

    janela_meses_ano_active = False
    janela_autor_ano_active = False
    janela_ano_palavras_active = False

    while True:
        evento, valores = janela.read()

        if evento == sg.WIN_CLOSED or evento == "Cancelar":
            janela.close()
            return  # Em vez de break, apenas retornamos para sair da função

        # Gerar gráficos conforme os eventos
        if evento == "Distribuição de Publicações por Ano":
            gerarGraficoPorAno(contagem_anos)

        elif evento == "Distribuição por Mês do Ano":
            if not janela_meses_ano_active:
                janela_meses_ano = sg.Window(
                    "Escolher Ano",
                    [[sg.Text("Escolha o ano")],
                     [sg.Combo(list(contagem_anos.keys()), key="-ANO-", size=(20, 1)), sg.Button("Gerar Gráfico")],
                     [sg.Button("Cancelar")]]
                )
                janela_meses_ano_active = True

            if janela_meses_ano_active:
                event, values = janela_meses_ano.read()
                if event in ("Cancelar", sg.WIN_CLOSED):
                    janela_meses_ano.close()
                    janela_meses_ano_active = False
                elif event == "Gerar Gráfico":
                    ano_escolhido = values["-ANO-"]
                    if ano_escolhido:
                        gerarGraficoPorMesAno(contagem_meses, ano_escolhido)

        elif evento == "Publicações por Autor (Top 20)":
            gerarGraficoPorAutor(top_autores)

        elif evento == "Distribuição de Palavras-chave por Frequência":
            gerarGraficoPalavrasChave(contagem_palavras_chave)

        elif evento == "Palavras-chave mais frequentes por Ano":
            if not janela_ano_palavras_active:
                janela_ano_palavras = sg.Window(
                    "Escolher Ano",
                    [[sg.Text("Escolha o ano")],
                     [sg.Combo(list(palavras_chave_por_ano.keys()), key="-ANO-", size=(20, 1)), sg.Button("Gerar Gráfico")],
                     [sg.Button("Cancelar")]]
                )
                janela_ano_palavras_active = True

            if janela_ano_palavras_active:
                event, values = janela_ano_palavras.read()
                if event in ("Cancelar", sg.WIN_CLOSED):
                    janela_ano_palavras.close()
                    janela_ano_palavras_active = False
                elif event == "Gerar Gráfico":
                    ano_escolhido = values["-ANO-"]
                    if ano_escolhido:
                        gerarGraficoPalavrasAno(palavras_chave_por_ano, ano_escolhido)


# Função para gerar gráfico de distribuição de publicações por ano
def gerarGraficoPorAno(contagem_anos):
    anos = list(contagem_anos.keys())
    publicacoes = list(contagem_anos.values())
    plt.figure(figsize=(10, 6))
    plt.bar(anos, publicacoes, color='skyblue')
    plt.title("Distribuição de Publicações por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Número de Publicações")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para gerar gráfico de distribuição de publicações por mês de um determinado ano
def gerarGraficoPorMesAno(contagem_meses, ano_escolhido):
    # Filtra os meses do ano escolhido
    meses_ano = {mes: count for mes, count in contagem_meses.items() if mes.startswith(ano_escolhido)}
    
    # Ordena os meses de forma cronológica
    meses_ordenados = sorted(meses_ano.keys())
    publicacoes_ordenadas = [meses_ano[mes] for mes in meses_ordenados]
    
    # Criação do gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(meses_ordenados, publicacoes_ordenadas, color='lightcoral')
    plt.title(f"Distribuição de Publicações por Mês de {ano_escolhido}")
    plt.xlabel("Mês")
    plt.ylabel("Número de Publicações")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para gerar gráfico de número de publicações por autor (top 20 autores)
def gerarGraficoPorAutor(top_autores):
    autores = [autor for autor, _ in top_autores]
    publicacoes = [count for _, count in top_autores]
    plt.figure(figsize=(10, 6))
    plt.barh(autores, publicacoes, color='lightgreen')
    plt.title("Número de Publicações por Autor (Top 20)")
    plt.xlabel("Número de Publicações")
    plt.ylabel("Autor")
    plt.tight_layout()
    plt.show()

# Função para gerar gráfico de distribuição de palavras-chave pela sua frequência (top 20 palavras-chave)
def gerarGraficoPalavrasChave(contagem_palavras_chave):
    # Ordena as palavras-chave por frequência e pega as 20 mais frequentes
    top_palavras = sorted(contagem_palavras_chave.items(), key=lambda x: x[1], reverse=True)[:20]
    
    palavras = [palavra for palavra, _ in top_palavras]
    frequencias = [count for _, count in top_palavras]
    
    plt.figure(figsize=(10, 6))
    plt.barh(palavras, frequencias, color='salmon')
    plt.title("Palavras-chave mais Frequentes")
    plt.xlabel("Frequência")
    plt.ylabel("Palavra-chave")
    plt.tight_layout()
    plt.show()

# Função para gerar gráfico de palavras-chave mais frequentes em um ano específico
def gerarGraficoPalavrasAno(palavras_chave_por_ano, ano_escolhido):
    palavras_ano = palavras_chave_por_ano.get(ano_escolhido, [])
    if palavras_ano:
        contagem_palavras_ano = defaultdict(int)
        for palavra in palavras_ano:
            contagem_palavras_ano[palavra] =contagem_palavras_ano[palavra] + 1

        # Ordena por frequência e seleciona as 20 palavras mais frequentes
        palavras_ordenadas = sorted(contagem_palavras_ano.items(), key=lambda x: x[1], reverse=True)[:20]
        palavras, frequencias = zip(*palavras_ordenadas) if palavras_ordenadas else ([], [])

        plt.figure(figsize=(10, 6))
        plt.barh(palavras, frequencias, color='lightblue')
        plt.title(f"Top 20 Palavras-chave mais Frequentes em {ano_escolhido}")
        plt.xlabel("Frequência")
        plt.ylabel("Palavra-chave")
        plt.tight_layout()
        plt.show()
    else:
        sg.popup("Não há palavras-chave registradas para este ano.", title="Erro", font=("Arial", 14), keep_on_top=True)


# setimo botão do menu principal - Listar Autores -----------------------------------------------

def listAutores():

    # Carregar publicações existentes
    file_name = file_path
    users = []  # Inicializa a lista de publicações

    # Verificar se o arquivo existe
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf8") as file_in:
            content = file_in.read().strip()
            if content:  # Verifica se o arquivo não está vazio
                users = json.loads(content)
    else:
        sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    # Extrair nomes dos autores e suas publicações
    autores_publicacoes = {}
    for pub in users:
        if "authors" in pub:
            for autor in pub["authors"]:
                nome_autor = autor["name"]
                if nome_autor not in autores_publicacoes:
                    autores_publicacoes[nome_autor] = []
                autores_publicacoes[nome_autor].append(pub["title"] if "title" in pub else "Título Desconhecido") 

    # Ordenar autores alfabeticamente
    autores_ordenados = [
        f"{autor}: {', '.join(autores_publicacoes[autor])}"
        for autor in sorted(autores_publicacoes.keys())
    ]

    # Layout para a janela de listagem de autores
    layout = [
        [sg.Text("Listar Autores", font=("Arial", 24), justification="center", expand_x=True)],
        [sg.Listbox(values=autores_ordenados, size=(50, 15), key="-AUTOR-", select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
        [sg.Button("Fechar")]
    ]

    window = sg.Window("Listar Autores", layout, font=('Arial', 16), finalize=True)

    continue_event = True  # Variável de controle para sair do loop

    while continue_event:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Fechar"):
            continue_event = False  # Atualiza o flag para sair do loop

    window.close()  # Fecha a janela


# oitavo botão do menu principal - Importar Publicações -----------------------------------------------

def importar_dados(users, caminho_arquivo):  # Função auxiliar para importar dados de um arquivo JSON
    with open(caminho_arquivo, "r", encoding="utf8") as file_in:
        novos_dados = json.load(file_in)
    
    if isinstance(novos_dados, list):  # Verifica se os dados carregados são uma lista
        users.extend(novos_dados)  # Adiciona os novos dados à lista existente
        # Salva os dados atualizados no arquivo original
        with open(file_path, "w", encoding="utf8") as file_out:
            json.dump(users, file_out, ensure_ascii=False, indent=4)
        sg.popup("Dados importados com sucesso!", title="Sucesso", font=("Arial", 14), keep_on_top=True)
    else:
        sg.popup("Arquivo inválido: deve conter uma lista de objetos.", title="Erro", font=("Arial", 14), keep_on_top=True)

def importarPubs():
    users = []

    # Verifica se o arquivo já existe
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf8") as file_in:
            content = file_in.read().strip()
            users = json.loads(content) if content else []
    else:
        sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    caminho_arquivo = sg.popup_get_file(
        "Selecione o arquivo JSON para importar", 
        file_types=(('JSON Files', '.json'), ('Todos os Arquivos', '.*')),  # Apenas arquivos JSON
        no_window=True  # Abre a janela de seleção de arquivo sem exibir a janela principal
    )

    if caminho_arquivo:
        importar_dados(users, caminho_arquivo)  # Chama a função para adicionar os dados
    else:
        sg.popup("Nenhum arquivo selecionado.", title="Aviso", font=("Arial", 14), keep_on_top=True)

# nono botão do menu principal - Exportar dados -----------------------------------------------

def exportarDados():
    # Carregar publicações existentes
    file_name = file_path 
    users = []  # Inicializa a lista de publicações

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf8") as file_in:
            content = file_in.read().strip()
            if content:
                users = json.loads(content)
    else:
        sg.popup("Nenhuma publicação encontrada.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    if not users:
        sg.popup("Nenhum dado disponível para exportação.", title="Erro", font=("Arial", 14), keep_on_top=True)
        return

    # Layout para filtro
    filtros = ["Título", "Autor", "Ano de Publicação", "Exportar Todos"]
    layout_filtro = [
        [sg.Text("Exportar Dados - Filtrar Publicações", font=("Arial", 24), justification="center", expand_x=True)],
        [sg.Text("Selecione o tipo de filtro:"), sg.Combo(filtros, key="-TIPO-FILTRO-", readonly=True, size=(30, 1))],
        [sg.Text("Insira o valor do filtro:"), sg.InputText(key="-VALOR-FILTRO-", size=(50, 1))],
        [sg.Button("Aplicar Filtro"), sg.Button("Cancelar")]
    ]

    janela_filtro = sg.Window("Filtro para Exportação", layout_filtro, font=("Arial", 16), finalize=True)

    valores_filtrados = []
    filtro_aplicado = False

    while not filtro_aplicado:
        evento, valores = janela_filtro.read()
        if evento in (sg.WIN_CLOSED, "Cancelar"):
            janela_filtro.close()
            return

        tipo_filtro = valores["-TIPO-FILTRO-"]
        valor_filtro = valores["-VALOR-FILTRO-"].strip()

        if tipo_filtro == "Exportar Todos":
            valores_filtrados = users  # Exporta todos os dados
            filtro_aplicado = True  # Marca que o filtro foi aplicado
        elif tipo_filtro and valor_filtro:
            if tipo_filtro == "Título":
                valores_filtrados = [pub for pub in users if valor_filtro.lower() in pub.get("title", "").lower()]
            elif tipo_filtro == "Autor":
                valores_filtrados = [
                    pub for pub in users if any(
                        valor_filtro.lower() in autor.get("name", "").lower() for autor in pub.get("authors", []))
                ]
            elif tipo_filtro == "Ano de Publicação":
                valores_filtrados = [pub for pub in users if pub.get("year", "") == valor_filtro]

            if valores_filtrados:
                filtro_aplicado = True  # Marca que o filtro foi aplicado

        if not filtro_aplicado:
            sg.popup("Por favor, preencha todos os campos corretamente ou escolha uma opção válida.", title="Erro", font=("Arial", 14), keep_on_top=True)

    janela_filtro.close()

    if not valores_filtrados:
        sg.popup("Nenhuma publicação encontrada com o filtro fornecido.", title="Aviso", font=("Arial", 14), keep_on_top=True)
        return

    # Abrir janela de seleção de local e nome do arquivo para exportação
    caminho_arquivo = sg.popup_get_file(
        "Selecione o local para salvar o arquivo exportado",
        save_as=True,
        file_types=(('JSON Files', '*.json'), ('Todos os Arquivos', '*.*')),
        no_window=True
    )

    if caminho_arquivo:
        with open(caminho_arquivo, "w", encoding="utf8") as file_out:
            json.dump(valores_filtrados, file_out, ensure_ascii=False, indent=4)
        sg.popup("Dados exportados com sucesso!", title="Sucesso", font=("Arial", 14), keep_on_top=True)
    else:
        sg.popup("Exportação cancelada ou nenhum local selecionado.", title="Aviso", font=("Arial", 14), keep_on_top=True)


# Inicializar a janela principal ---------------------------------------------------------------
window = main_menu()

# Variável de controle para o loop
current_window = "main"

while current_window != "exit":
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "-EXIT-"):
        current_window = "exit"  # Atualiza para sair do loop principal

    elif event == "-HELP-":
        help()

    elif event == "-CRIARPUB-":
        users = []
        criarPub(users)

    elif event == "-CONSULTADEPUB-":
        consultarPub()
    
    elif event == "-LISTARPUB-":
        listarPub()
    
    elif event == "-ELIMINARPUBLICACOES-":
        elimPub()
    
    elif event == "-RELATORIOESTATISTICAS-":
        relEstat()
    
    elif event == "-LISTARAUTORES-":
        listAutores()
    
    elif event == "-IMPORTARPUBLICACOES-":
        importarPubs()
    
    elif event == "-EXPORTARDADOS-":
        exportarDados()
    

    # Voltar para o menu principal
    elif event == "-BACK-":
        window.close()
        window = main_menu()
        current_window = "main"

# Fechar a janela ao sair
window.close()