from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer

from utils.request import Request


sbf_url = lambda x: urljoin('https://www.sbfisica.org.br/rbef/', x)  # Função geradora de urls
request = Request()


def volumes_por_ano() -> dict[int:list]:
    """
        Função que pega o link de cada volume da revista por ano.

    Returns:
        dict: Dicionário onde as chaves é o ano e os valores os links dos volumes do respectivo ano.
    """
    req = request.get(sbf_url('edicoes.shtml'))
    soup = BeautifulSoup(req.text, 'html.parser',
                         parse_only=SoupStrainer('table', attrs={'id': 'AutoNumber2'}))
    row = soup.find_all('tr')[3:]  # hardcode 3

    links = {}

    for item in row:
        col = item.find_all('td')
        ano = int(col[0].text.strip())
        
        urls = []
        for i in col[2:]:
            a_tag = i.a
            
            if a_tag:
                urls.append(sbf_url(a_tag['href']))
            
        links[int(ano)] = urls
        
    return links


def artigos_por_volume(url: str) -> list[tuple[str,str]]:
    """
        Função que coleta o link de todos os artigos presentes no volume.

    Args:
        url (str): url do volume

    Returns:
        list: Lista com os links dos artigos deste volume.
    """
    req = request.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    return [(a.text.strip(), sbf_url(a['href'])) for a in soup.find_all('a')]