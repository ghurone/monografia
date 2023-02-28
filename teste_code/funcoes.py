from bs4 import BeautifulSoup, SoupStrainer


def limpa_html(text_html) -> str:
    soup = BeautifulSoup(text_html, 'lxml', parse_only=SoupStrainer('div', attrs={'data-anchor': 'Text'}))

    # tags do título, citações, referências, equações e figuras foram removidas.
    remover = soup.find_all('h1') + soup.find_all('span', attrs={'class': 'ref'}) + \
           soup.find_all('div', attrs={'class':'row formula'}) + soup.find_all('div', attrs={'class': 'row fig'}) + \
           soup.find_all('math')
    for tag in remover:
          tag.decompose()

    return ' '.join(soup.text.lower().split())


