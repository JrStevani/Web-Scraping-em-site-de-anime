from playwright.sync_api import sync_playwright
from os import path, makedirs
import json
from unidecode import unidecode
from re import sub

# Função para registrar o progresso em um arquivo de texto
def registrar_progresso(nome_arquivo, texto):
    try:
        # Tenta abrir o arquivo em modo de leitura e lê o conteúdo atual
        with open(nome_arquivo, 'r', encoding='utf-8') as file_a:
            conteudo_atual = file_a.read()
        # Abre o arquivo em modo de adição para escrever o novo texto
        with open(nome_arquivo, 'a', encoding='utf-8') as file_b:
            if conteudo_atual:
                file_b.write('\n')
            file_b.write(texto)
    except FileNotFoundError:
        # Se o arquivo não existir, cria um novo arquivo e escreve o texto
        with open(nome_arquivo, 'w', encoding='utf-8') as file_c:
            file_c.write(texto)

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

# Função para criar uma pasta se ela não existir
def criar_pasta(nome="caminho"):
    if not path.exists(nome):
        makedirs(nome)

# Função para criar um arquivo JSON com um conteúdo específico
def criar_arquivo_json(caminho='Resultado', nome_do_arquivo='Novo.json', conteudo=None):
    if conteudo is None:
        conteudo = {}
    if not path.exists(f'{caminho}\\{nome_do_arquivo}'):
        with open(f'{caminho}\\{nome_do_arquivo}', 'w') as arquivo:
            json.dump({}, arquivo)
    with open(f'{caminho}\\{nome_do_arquivo}', 'w') as json_file:
        json.dump(conteudo, json_file, indent=4)

# Função para ler o conteúdo de um arquivo JSON e retornar a lista de URLs
def lendo_json(arquivo):
    try:
        with open(arquivo, 'r') as arc:
            conteudo = json.load(arc)
        return conteudo['urls']
    except FileNotFoundError:
        return []

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

# Função principal
def main_2():
    generos = ['dublado', 'legendado']
    # Usando Playwright para abrir um navegador
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for genero in generos:
            c = 0
            criar_pasta(f'Resultado\\{genero}\\Animes')
            lista_completa_de_url = []
            if len(lista_completa_de_url) == 0:
                lista_completa_de_url = list(lendo_json(f'Resultado\\{genero}\\Animes_{genero}.json'))
            dic = {}
            for anime in lista_completa_de_url:
                anime_capiturados = ler_arquivo_de_texto(f"Resultado\\{genero}\\Animes-capiturados.txt")

                if anime not in anime_capiturados:
                    try:
                        c += 1
                        lista_de_ep = []
                        page.goto(url=anime, timeout=50000, wait_until="domcontentloaded")
                        nome = str(page.text_content('xpath=//*[@id="single"]/div[1]/div[1]/div[2]/h1')
                                   ).lower().replace('todos os episodios online', '').strip().title()
                        nome = str(sub(r'[^\w\s]', '', nome))
                        dic['nome'] = str(nome)
                        nome_do_arquivo = str(unidecode(nome))

                        descricao = str(page.text_content('xpath=//*[@id="single"]/div[1]/div[3]/div/p'))
                        dic['descricao'] = str(unidecode(descricao))

                        div_sgeneros = page.query_selector(".sgeneros")
                        generos = div_sgeneros.query_selector_all("a")

                        lista = []
                        for link in generos:
                            glist = str(link.inner_text())
                            lista.append(unidecode(glist))
                        dic['generos'] = lista

                        del lista

                        # Obtendo o link da imagem
                        elemento_da_imagem = page.query_selector('xpath=//*[@id="single"]/div[1]/div[1]/div[1]')
                        imagem = elemento_da_imagem.query_selector('img')
                        link_imagem = imagem.get_attribute('src')
                        dic['imagem'] = str(link_imagem)

                        temporadas = page.query_selector_all('div.se-c')
                        dados_temporadas = {}

                        for temporada in temporadas:
                            numero_temporada = temporada.query_selector('span.se-t').inner_text()
                            titulo_temporada = temporada.query_selector('span.title').inner_text()

                            episodios = []
                            episodios_lista = temporada.query_selector_all('div.episodiotitle a')

                            if len(episodios_lista) != 0:
                                for episodio in episodios_lista:
                                    url_episodio = episodio.get_attribute('href')
                                    episodios.append(url_episodio)

                                dados_temporadas[titulo_temporada] = {
                                    'numero': numero_temporada,
                                    'episodios': episodios
                                }
                        dic['temporadas_episodios'] = dados_temporadas

                        criar_pasta(f"Resultado\\{genero}\\Animes\\{nome_do_arquivo}")
                        criar_arquivo_json(caminho=f'Resultado\\{genero}\\Animes\\{nome_do_arquivo}',
                                           nome_do_arquivo=f'{nome_do_arquivo}.json', conteudo=dic)
                        registrar_progresso(nome_arquivo=f"Resultado\\{genero}\\Animes-capiturados.txt",
                                            texto=str(anime))
                        print(f'{c}/{len(lista_completa_de_url)} {genero}: {nome}')
                    except:
                        import traceback
                        traceback_str = str(traceback.format_exc())
                        registrar_erro(nome_arquivo=r"Erros.txt", texto=str(traceback_str + anime))
                        print(traceback_str)
                else:
                    c += 1

        browser.close()
        print("Concluido!!")

if __name__ == "__main__":
    main_2()
