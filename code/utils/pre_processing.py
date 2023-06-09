import spacy 
from bs4 import BeautifulSoup, SoupStrainer


nlp = spacy.load('pt_core_news_lg')  # spacy portuguese model
alfabeto_portugues = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ-")


def tokenizer(text, classes:list=['PNONU', 'NOUN', 'ADJ', 'VERB'], is_lemma:bool=True):
    doc = nlp(text)
    temp = []
    for token in doc:
        if len(token) > 1 and token.pos_ in classes and is_alpha(token.orth_):
            temp.append(token.lemma_ if is_lemma else token.orth_)
    return temp      


def is_alpha(palavra):
    return set(palavra).issubset(alfabeto_portugues)


def html_to_text(html_text):
    soup = BeautifulSoup(html_text, 'lxml', parse_only=SoupStrainer('div', attrs={'data-anchor': 'Text'}))

    # tags do título, citações, referências, equações, links, tabelas e figuras foram removidas.
    remover = soup.find_all('h1') + soup.find_all('span', attrs={'class': 'ref'}) + \
           soup.find_all('div', attrs={'class':'row formula'}) + soup.find_all('div', attrs={'class': 'row fig'}) + \
           soup.find_all('math') + soup.find_all('div', attrs={'class': 'row table'}) + soup.find_all('div', attrs={'class': 'ref-list'}) + \
           soup.find_all('a')

    for tag in remover:
          tag.decompose()
    
    texto = soup.text
    
    return ' '.join(texto.split())