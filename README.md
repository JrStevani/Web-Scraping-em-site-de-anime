# Web Scraping em site de anime

Descrição do Projeto:

Web Scraping de Animes: Captura de IDs de Episódios e Metadados

Este projeto tem como objetivo realizar web scraping em um site de animes para capturar os IDs dos episódios de todos os animes hospedados no site. Utilizando a biblioteca Playwright, o projeto automatiza a navegação no site para extrair informações detalhadas sobre cada anime, incluindo:

Nome do Anime: Capturado e normalizado (sem acentuação).
Descrição: Texto descritivo do anime.
Gêneros: Lista de gêneros associados ao anime.
Imagem: URL da imagem de capa do anime.
Temporadas e Episódios: Lista de temporadas e URLs de cada episódio.
As informações coletadas são organizadas e armazenadas em arquivos JSON, facilitando o acesso e manipulação dos dados. Além disso, o projeto mantém um registro de progresso e de erros em arquivos de texto, garantindo que o processo de scraping seja monitorado e que possíveis problemas sejam documentados.

Funcionalidades Principais:

Criação de Pastas e Arquivos:

Cria diretórios específicos para armazenar os resultados de cada gênero (dublado e legendado).
Gera arquivos JSON contendo os metadados dos animes e seus episódios.
Registro de Progresso e Erros:

Mantém um log do progresso em arquivos de texto.
Documenta erros ocorridos durante a execução, facilitando a depuração.
Leitura de Dados Existentes:

Lê URLs de animes a partir de arquivos JSON existentes.
Verifica se um anime já foi processado para evitar duplicidade.
Automação de Navegação:

Utiliza Playwright para navegar pelas páginas dos animes e extrair as informações desejadas.
Processa os dados coletados e os salva em arquivos estruturados.
Este projeto é ideal para aqueles que precisam extrair e organizar grandes volumes de dados de sites de forma eficiente e estruturada, oferecendo uma solução robusta para a captura e armazenamento de informações detalhadas sobre animes.