from gensim.corpora import Dictionary
from gensim.models import Phrases, LdaModel, LdaMulticore
from gensim.models.coherencemodel import CoherenceModel


def add_bigram(documentos: list, min_count=5) -> None:
    bigram = Phrases(documentos, min_count=min_count, threshold=5)
    for idx in range(len(documentos)):
        for token in bigram[documentos[idx]]:
            if '_' in token:  
                documentos[idx].append(token)
    
    
def create_dictionary(documentos, filtrar=True, n_abaixo=30, n_acima=0.5):
    dicio = Dictionary(documentos)
    if filtrar:
        dicio.filter_extremes(no_below=n_abaixo, no_above=n_acima)
    return dicio


def create_corpus(dicionario, documentos):
    return [dicionario.doc2bow(doc) for doc in documentos]


def calc_coherence(model, documents, dictionary, corpus, method='u_mass'):
    return CoherenceModel(model=model, texts=documents,
                          dictionary=dictionary, corpus=corpus,
                          coherence=method).get_coherence()


class ModelLDA:
    def __init__(self, corpus, id2word, chunksize=2000, iterations=100, passes=20):
        self.corpus = corpus
        self.id2word = id2word

        self.chunksize = chunksize
        self.iterations = iterations
        self.passes = passes

        self.SEED = 99  # 99 >> 42

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
                    random_state=self.SEED,
                    eval_every=None
                    
        )