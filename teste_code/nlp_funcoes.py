import os

import spacy
from nltk.corpus import stopwords
from spacy.lang.pt.stop_words import STOP_WORDS
from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel


nlp = spacy.load("pt_core_news_lg")
my = {'fig', 'p.', 'cm', 'et', 'al', 'of', 'the', 'eq', 'figura', 'pi',
      'ref', 'km', 'kg', 'ii', 'iii', 'iv', 'xix', 'mm', 'in', 'and'}
stop = set(stopwords.words('portuguese')).union(STOP_WORDS).union(my)


def token_lemma(texto):
    doc = nlp(texto)
    temp = []
    for token in doc:
        if not (token.orth_ in stop or token.lemma_ in stop) and token.is_alpha and len(token) > 1:
            temp.append(token.lemma_.lower())
    return temp


def add_bigram(documentos: list, min_count=5) -> None:
    bigram = Phrases(documentos, min_count=min_count)
    for idx in range(len(documentos)):
        for token in bigram[documentos[idx]]:
            if '_' in token:  # se for um n-gram, adiciona no documento
                documentos[idx].append(token)


def create_dictionary(documentos, no_below=30, no_above=0.5):
    dicio = Dictionary(documentos)
    dicio.filter_extremes(no_below=no_below, no_above=no_above)
    return dicio


def create_corpus(dicionario, documentos):
    return [dicionario.doc2bow(doc) for doc in documentos]


def calc_coherence(model, documents, dictionary, corpus, method='u_mass'):
    return CoherenceModel(model=model, texts=documents,
                          dictionary=dictionary, corpus=corpus,
                          coherence=method).get_coherence()


class ModelLDA:
    def __init__(self, corpus, id2word, chunksize=1000, iterations=400, passes=50, eval_every=None):
        self.corpus = corpus
        self.id2word = id2word
        
        self.chunksize = chunksize
        self.iterations = iterations
        self.passes = passes
        self.eval_every = eval_every
        
        self.SEED = 99
        
    def run(self, n_topic, alpha='auto', eta='auto'):
        return LdaModel(
                    corpus=self.corpus,
                    id2word=self.id2word,
                    chunksize=self.chunksize,
                    alpha=alpha,
                    eta=eta,
                    iterations=self.iterations,
                    num_topics=n_topic,
                    passes=self.passes,
                    eval_every=self.eval_every,
                    random_state=self.SEED
        )
