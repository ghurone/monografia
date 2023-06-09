from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer

from utils.request import Request


scielo_url = lambda x: urljoin('https://www.scielo.br', x)  # Função geradora de urls
request = Request()

def volumes_por_ano() -> dict[int:list]:
    """
        Função que pega o link de cada volume da revista por ano.

    Returns:
        dict: Dicionário onde as chaves é o ano e os valores os links dos volumes do respectivo ano.
    """
    req = request.get(scielo_url('j/rbef/grid'))
    soup = BeautifulSoup(req.text, 'lxml', parse_only=SoupStrainer('tbody'))

    links = {int(linha.td.text): [scielo_url(a['href']) for a in linha.find_all('a')] for linha in soup.find_all('tr')}
    
    return links


def artigos_por_volume(url: str, formato: str = 'html', idioma: str = 'pt') -> list[str]:
    """
        Função que coleta o link de todos os artigos presentes no volume.

    Args:
        url (str): url do volume
        formato (str, optional): Formato dos artigos. Defaults to 'html'.
        idioma (str, optional): Idioma dos artigos. Defaults to 'pt'.

    Returns:
        list: Lista com os links dos artigos deste volume.
    """
    languages = {'pt': 'Português', 'en': 'Inglês', 'es': 'Espanhol'}
    formatos = {'html': '/?lang=', 'pdf': '/?format=pdf&'}

    lang = languages.get(idioma.lower())
    form = formatos.get(formato.lower())

    req = request.get(url)

    soup = BeautifulSoup(req.text, 'lxml', parse_only=SoupStrainer('a', attrs={'title': lang}))

    return [scielo_url(a['href']) for a in soup.find_all('a') if 'abstract' not in a['href'] and form in a['href']]


def html_do_artigo(url: str) -> BeautifulSoup:
    """
        Função que recebe uma url de um artigo e retorna uma string do seu html.

    Args:
        url (str): Url do artigo

    Returns:
        str: Retorna uma string do html da página do artigo.
    """
    req = request.get(url)
    
    strainer = SoupStrainer('div', attrs={'class': 'articleTxt'})
    
    return BeautifulSoup(req.text, 'lxml', parse_only=strainer).prettify()