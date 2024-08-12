# Web Scraping em site de anime

<a href="https://jrstevani.github.io/Web-Scraping-em-site-de-anime/index.html"><strong>Projeto detalhado</strong></a>

<strong>Descrição do Projeto:</strong>

<strong>Web Scraping de Animes:</strong> Captura de IDs de Episódios e Metadados

Este projeto tem como objetivo realizar web scraping em um site de animes para capturar os IDs dos episódios de todos os animes hospedados no site. Utilizando a biblioteca Playwright, o projeto automatiza a navegação no site para extrair informações detalhadas sobre cada anime, incluindo:

<strong>Nome do Anime:</strong> Capturado e normalizado (sem acentuação).
<strong>Descrição:</strong> Texto descritivo do anime.
<strong>Gêneros:</strong> Lista de gêneros associados ao anime.
<strong>Imagem:</strong> URL da imagem de capa do anime.
<strong>Temporadas e Episódios:</strong> Lista de temporadas e URLs de cada episódio.
As informações coletadas são organizadas e armazenadas em arquivos JSON, facilitando o acesso e manipulação dos dados. Além disso, o projeto mantém um registro de progresso e de erros em arquivos de texto, garantindo que o processo de scraping seja monitorado e que possíveis problemas sejam documentados.

<strong>Funcionalidades Principais:</strong>

<strong>Criação de Pastas e Arquivos:</strong>

Cria diretórios específicos para armazenar os resultados de cada gênero (dublado e legendado).
Gera arquivos JSON contendo os metadados dos animes e seus episódios.
<strong>Registro de Progresso e Erros:</strong>

Mantém um log do progresso em arquivos de texto.
Documenta erros ocorridos durante a execução, facilitando a depuração.
<strong>Leitura de Dados Existentes:</strong>

Lê URLs de animes a partir de arquivos JSON existentes.
Verifica se um anime já foi processado para evitar duplicidade.
<strong>Automação de Navegação:</strong>

Utiliza Playwright para navegar pelas páginas dos animes e extrair as informações desejadas.
Processa os dados coletados e os salva em arquivos estruturados.
Este projeto é ideal para aqueles que precisam extrair e organizar grandes volumes de dados de sites de forma eficiente e estruturada, oferecendo uma solução robusta para a captura e armazenamento de informações detalhadas sobre animes.