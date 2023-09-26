import os

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import ticker
import numpy as np

mpl.rcParams['axes.formatter.use_mathtext'] = True


def plot_frequent_words(dicionario, n=15, filename='', dpi=300):
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
    #ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    
    # adjust x-axis labels
    ax.tick_params(axis='x', labelrotation=45, labelsize=10)
    
    if filename != '':
        if not os.path.exists('plots'):
            os.mkdir('plots')
            
        path = os.path.join('plots', filename)
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
        
    plt.show()