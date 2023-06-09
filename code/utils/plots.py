import os

import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

def plot_coerencias(coerencias, n_topicos):
    fig, ax = plt.subplots(nrows=1, ncols=len(coerencias),
                           figsize=(5*len(coerencias), 5))

    for i, k in enumerate(coerencias):
        y = coerencias[k]

        ax[i].set_title(k)
        ax[i].set_xlabel('Número de tópicos')

        ax[i].scatter(n_topicos, y, s=16, c='black')
        ax[i].plot(n_topicos, y, c='black', ls='--')

    fig.tight_layout()
    plt.show()
    

def plot_med_coerencias(norm_coerencias, n_topicos, n=3):
    medias = sum(norm_coerencias.values()) / len(norm_coerencias)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    dx = (max(n_topicos) - min(n_topicos)) / n
    for i in range(1, n):
        scale = min(n_topicos) + i*dx            
        ax.axvline(scale, ls='--', c='gray', lw=1.5)
        
    ax.set_xlabel('Número de tópicos')
    for i, k in enumerate(norm_coerencias):
        y = norm_coerencias[k]
        ax.scatter(n_topicos, y, s=20)
        ax.plot(n_topicos, y, label=k)

    ax.plot(n_topicos, medias, label='Média', c='k', lw=3, ls='--')

    ax.set_xticks(n_topicos)
    ax.legend()
    fig.tight_layout()
    plt.show()
    

def print_med_coerencias(coerencias, n_topicos):
    medias = sum(coerencias.values()) / len(coerencias)
    for i in medias.argsort()[::-1]:
        print(f'{str(n_topicos[i]).rjust(2, "0")} tópicos | {medias[i]:.2f}')
        

def plot_frequent_words(dicionario, n=15, filename='', dpi=250):
    word_counts = dicionario.cfs
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # get the top 10 frequent words and their counts
    top = sorted_counts[:n]
    words = [dicionario[i[0]] for i in top]
    counts = np.array([i[1] for i in top])
    
    # plot the bar chart
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(words, counts)
    ax.set_title(f'Top {n} palavras frequentes ({len(dicionario)} palavras)', weight='bold')
    ax.set_ylabel('Frequência', weight='bold')
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    
    # adjust x-axis labels
    ax.tick_params(axis='x', labelrotation=45, labelsize=10)
    
    if filename != '':
        if not os.path.exists('plots'):
            os.mkdir('plots')
            
        path = os.path.join('plots', filename)
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
        
    plt.show()