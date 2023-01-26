from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry


class Request:
    def __init__(self, n_retry: int = 10, timeout: float = 5):
        self.retries = Retry(total=n_retry, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.adapter = HTTPAdapter(max_retries=self.retries)
        self.http = requests.Session()
        self.http.mount("https://", self.adapter)

        self.timeout = timeout

    def do_request(self, url: str, params: dict = None) -> str:
        if params is None:
            params = {}

        resp = self.http.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()

        return resp.text


class SciELO:
    def __init__(self):
        self.req = Request()

    def get_volume_by_year(self) -> dict:
        html_text = self.req.do_request('https://www.scielo.br/j/rbef/grid')

        soup = BeautifulSoup(html_text, 'html.parser')
        table = soup.table.tbody

        links = {}
        for linha in table.find_all('tr'):
            ano = linha.td.text.strip()
            links[ano] = [urljoin('https://www.scielo.br', a['href']) for a in linha.find_all('a')]

        return links

    def get_articles(self, url: str, formato: str = 'html', idioma: str = 'pt') -> list:
        languages = {'pt': 'Português', 'en': 'Inglês', 'es': 'Espanhol'}
        formatos = {'html': '/?lang=', 'pdf': '/?format=pdf&'}

        lang = languages.get(str(idioma).lower(), None)
        if not lang:
            raise ValueError('Idioma inválido!')

        form = formatos.get(str(formato).lower(), None)
        if not form:
            raise ValueError('Formato inválido!')

        html_text = self.req.do_request(url)  # rise spot

        soup = BeautifulSoup(html_text, 'html.parser')
        ul = soup.find_all('ul', attrs={'class': 'links'})

        links = []
        for li in ul:
            a_tag = li.find_all('a', attrs={'title': lang})
            for a in a_tag:
                href = a['href']
                if 'abstract' not in href:
                    if form in href:
                        links.append(urljoin('https://www.scielo.br', href))

        return links

    def get_article_texts(self, article_url: str):
        html_text = self.req.do_request(article_url)
        soup = BeautifulSoup(html_text, 'html.parser')
        artigo = soup.find('article', attrs={'id': 'articleText'})

        # resumo = artigo.find('div', attrs={'class': None})  # primeira div contem o resumo.
        texto = artigo.find('div', attrs={'class': 'articleSection', 'data-anchor': 'Text'})

        # remove formulas
        for formula_tag in texto.find_all('div', attrs={'class': 'row formula'}):
            formula_tag.decompose()

        # remove figuras
        for figura_tag in texto.find_all('div', attrs={'class': 'row fig'}):
            figura_tag.decompose()

        # remove notas de rodapé
        for span_tag in texto.find_all('span', attrs={'class':  'ref footnote'}):
            span_tag.decompose()

        # remove citações
        for span_tag in texto.find_all('span', attrs={'class':  'ref'}):
            span_tag.decompose()

        # remove equaçoes inline
        for svg_tag in texto.find_all('span', attrs={'class': 'MathJax_SVG'}):
            svg_tag.decompose()

        return texto.text

