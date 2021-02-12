import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

params = ['mc', 'pl', 'pm', 'po', 'rm']

for par in params:

    #dane = pd.read_csv("wyniki_" + par + "_umarli.txt", header = None, sep = " ")
    dane = pd.read_csv("wyniki_" + par + "_chorzy.txt", header = None, sep = " ")
    dane = dane.iloc[:, :4]
    
    dane.columns = ['0.2', '0.4', '0.6', '0.8']
    print(dane)

    sns.violinplot(data=dane)
    plt.xlabel("Value of parameter", fontsize=14)
    plt.ylabel("Individuals", fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()
