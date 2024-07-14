from playwright.sync_api import sync_playwright
from os import listdir, path
import json
from bs4 import BeautifulSoup

# Função para ler um arquivo de texto e retornar seu conteúdo como uma lista de strings, sem quebras de linha
def ler_arquivo_de_texto(caminho):
    if path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as file_a:
            lista = file_a.readlines()
            lista_sem_quebra = []
            for item in lista:
                lista_sem_quebra.append(item.replace('\n', ''))
            return lista_sem_quebra
    else:
        return ''

# Função para registrar erros em um arquivo de texto
def registrar_erro(nome_arquivo, texto):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file_a:
            conteudo_atual = file_a.read()
        with open(nome_arquivo, 'a', encoding='utf-8') as file_b:
            if conteudo_atual:
                file_b.write('\n' + '=-' * 35 + '\n')
            file_b.write(texto)
    except FileNotFoundError:
        with open(nome_arquivo, 'w', encoding='utf-8') as file_c:
            file_c.write(texto)

# Função para criar um arquivo JSON com um conteúdo específico
def criar_arquivo_json(caminho='Resultado', nome_do_arquivo='Novo.json', conteudo=None):
    if conteudo is None:
        conteudo = {}
    if not path.exists(f'{caminho}\\{nome_do_arquivo}'):
        with open(f'{caminho}\\{nome_do_arquivo}', 'w') as arquivo:
            json.dump({}, arquivo)
    with open(f'{caminho}\\{nome_do_arquivo}', 'w') as json_file:
        json.dump(conteudo, json_file, indent=4)

# Função para registrar o progresso em um arquivo de texto
def registrar_progresso(nome_arquivo, texto):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file_a:
            conteudo_atual = file_a.read()
        with open(nome_arquivo, 'a', encoding='utf-8') as file_b:
            if conteudo_atual:
                file_b.write('\n')
            file_b.write(texto)
    except FileNotFoundError:
        with open(nome_arquivo, 'w', encoding='utf-8') as file_c:
            file_c.write(texto)

# Função para ler o conteúdo completo de um arquivo JSON
def lendo_json_completo(arquivo):
    try:
        with open(arquivo, 'r') as arc:
            conteudo = json.load(arc)
        return conteudo
    except FileNotFoundError:
        return []

# Função para ler o conteúdo de um arquivo JSON e retornar a lista de temporadas e episódios
def lendo_json(arquivo):
    try:
        with open(arquivo, 'r') as arc:
            conteudo = json.load(arc)
        return conteudo['temporadas_episodios']
    except FileNotFoundError:
        return []

# Função para listar diretórios e verificar se possuem um arquivo específico
def lista_diretorios(diretorio):
    diretorios_encontrados = []
    animes_nao_capiturados = []
    if path.exists(diretorio):
        for item in listdir(diretorio):
            if path.isdir(path.join(diretorio, item)):
                diretorios_encontrados.append(item)
    for anime in diretorios_encontrados:
        diretorio_anime = f'{diretorio}\\{anime}'
        lista = [arquivo for arquivo in listdir(diretorio_anime) if path.isfile(path.join(diretorio_anime, arquivo))]
        if f'{anime}-episodios.json' not in lista:
            animes_nao_capiturados.append(anime)
    return animes_nao_capiturados

# Definindo os gêneros
generos = ['dublado', 'legendado']
c = 0

# Usando Playwright para abrir um navegador
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for genero in generos:
        lista_de_diretorios = lista_diretorios(f'.\\Resultado\\{genero}\\Animes\\')
        print(f'Total de anmes: {len(lista_de_diretorios)}')
        c = 0
        for diretorio in lista_de_diretorios:
            c += 1
            try:
                lista_de_episodios = lendo_json(f'.\\Resultado\\{genero}\\Animes\\{diretorio}\\{diretorio}.json')
                nome_do_arquivo = f'.\\Resultado\\{genero}\\Animes\\{diretorio}\\{diretorio}.json'
                caminho_arquivo = path.join(f'Resultado\\{genero}\\Animes\\{diretorio}', f'{diretorio}-episodios.json')
                dados = lendo_json_completo(f'.\\Resultado\\{genero}\\Animes\\{diretorio}\\{diretorio}.json')

                if path.exists(caminho_arquivo):
                    print(f'passei por {caminho_arquivo}')
                else:
                    dic = {}
                    total_de_temporadas = len(lista_de_episodios)
                    novo_dic_temporadas = {}
                    dic_url_epi = {}

                    for temporada in lista_de_episodios:
                        dic_temporada = lista_de_episodios[temporada]
                        dic_temporada = dic_temporada['episodios']
                        for url in dic_temporada:
                            anime_capiturados = ler_arquivo_de_texto(f"Resultado\\{genero}\\Animes-capiturados.txt")

                            if url not in anime_capiturados:
                                page.goto(url=url, timeout=50000, wait_until="domcontentloaded")
                                try:
                                    iframe_src = page.query_selector('div.play-box-iframe iframe').get_attribute('src')
                                    numero_episodio = str(int(page.text_content('xpath=//*[@id="info"]/h1').split()[-2]))
                                    numero_episodio = str(f"Ep_{numero_episodio.zfill(4)}")

                                    dic[numero_episodio] = iframe_src
                                    page.goto(url=iframe_src, timeout=50000, wait_until="domcontentloaded")
                                    page.wait_for_selector('.play-button')
                                    page.click(".play-button")
                                    page.wait_for_selector('#videocontainer')
                                    page.wait_for_timeout(5000)
                                    iframe_element = page.query_selector('#videocontainer')
                                    iframe = iframe_element.content_frame()
                                    html_do_iframe = iframe.content()
                                    soup = BeautifulSoup(html_do_iframe, 'html.parser')
                                    video_element = soup.find('div', class_='html5-video-container')
                                    video_src = str(video_element.find('video')['src']).split('&id=')[1].split('&itag')[0]
                                except:
                                    video_src = 'uncaptured code'
                                    registrar_erro(nome_arquivo=r"Codigos invalidos.txt", texto=str(f'{diretorio}: {numero_episodio}'))
                                    registrar_erro(nome_arquivo=r"Erros.txt", texto=str(f'{diretorio}: {numero_episodio}'))
                                dic_url_epi[numero_episodio] = str(video_src)
                            novo_dic_temporadas[temporada] = dic_url_epi

                    dados['temporadas_episodios'] = novo_dic_temporadas
                    registrar_progresso(nome_arquivo=f"Resultado\\{genero}\\Animes-episodios-capiturados.txt", texto=str(url))
                    criar_arquivo_json(caminho=f'Resultado\\{genero}\\Animes\\{diretorio}', nome_do_arquivo=f'{diretorio}-episodios.json', conteudo=dados)
            except:
                print(f'Erro: {diretorio}')
                import traceback
                traceback_str = str(traceback.format_exc())
                registrar_erro(nome_arquivo=r"Erros.txt", texto=str(traceback_str + diretorio))

    browser.close()
