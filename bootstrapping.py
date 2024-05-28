import pandas as pd
from random import choices
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(context='paper', style='whitegrid', palette='deep', font='Arial', font_scale=1.5, color_codes=True, rc=None)

df = pd.read_csv('distance_correlation.csv')
genes = df['perturbagen'].tolist()
df = df.set_index(df['perturbagen'])

simulations = 1000000
reference_correlation =  0.305
means = []
for i in range(simulations):
    random_genes = choices(genes, k = 22)
    random_sample = df.reindex(index=random_genes, columns=random_genes) #.abs()
    #means.append(random_sample.values[np.triu_indices_from(random_sample.values,1)].mean())
    means.append(np.median(random_sample.values[np.triu_indices_from(random_sample.values,1)]))

means = np.asarray(means, dtype=float)    
p = ((means >= reference_correlation).sum() / simulations)
print(p)

sns.set_style("white")
sns.despine()
#sns.distplot(degree_list, kde=False, rug=False)
sns.histplot(means, log_scale=False, fill=False, color='k', bins=23)
sns.despine()
plt.ylabel("Frequency")
plt.xlabel("Mean correlation")
plt.title("Mean correlation")