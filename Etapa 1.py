from playwright.sync_api import sync_playwright
from os import path, makedirs
import json

# Função para criar uma pasta, se ela não existir
def criar_pasta(nome="Resultado"):
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

def main():
    generos = ['dublado', 'legendado']  # Gêneros de animes a serem processados
    criar_pasta("Resultado")  # Cria a pasta principal para armazenar os resultados
    lista_completa_de_url = []  # Lista para armazenar todas as URLs coletadas
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Inicia o navegador em modo headless
        page = browser.new_page()  # Abre uma nova página no navegador
        for genero in generos:
            criar_pasta(f'Resultado\\{genero}')  # Cria uma pasta para cada gênero
            # Navega para a página inicial do gênero
            page.goto(url=f'https://animesonlinecc.to/genero/{genero}', timeout=50000, wait_until="domcontentloaded")
            # Obtém o número total de páginas para o gênero
            total_de_paginas = int(str(page.text_content(
                'xpath=//*[@id="contenedor"]/div[2]/div/div[3]/span[1]')).split()[-1]) + 1
            for pagina in range(1, total_de_paginas):
                # Navega para cada página do gênero
                page.goto(url=f'https://animesonlinecc.to/genero/{genero}/page/{pagina}', timeout=50000,
                          wait_until="domcontentloaded")
                # Seleciona o elemento pai que contém os links dos animes
                elemento_pai = page.query_selector('xpath=//*[@id="contenedor"]/div[2]/div/div[2]')
                links = elemento_pai.query_selector_all('a')

                # Extrai os URLs dos links encontrados e adiciona à lista completa de URLs
                lista_de_url = set([link.get_attribute('href') for link in links])
                for url in lista_de_url:
                    if url not in lista_completa_de_url:
                        lista_completa_de_url.append(url)
                print(f'{genero} - Pagina: {pagina}/ {total_de_paginas - 1}')
            # Cria um dicionário com as URLs coletadas e salva em um arquivo JSON
            dic = {}
            dic['urls'] = lista_completa_de_url
            criar_arquivo_json(caminho=f'Resultado\\{genero}', nome_do_arquivo=f'Animes_{genero}.json', conteudo=dic)
        browser.close()  # Fecha o navegador

if __name__ == "__main__":
    main()  # Executa a função principal
