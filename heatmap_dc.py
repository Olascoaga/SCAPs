import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt 
import numpy as np
import dcor
from itertools import combinations_with_replacement

sns.set_theme(context='paper', style='whitegrid', palette='deep', font='Arial', font_scale=1.8, color_codes=True, rc=None)

# Use files from the knockdown folder
df = pd.read_csv('scaps_39_knockdown.csv', index_col=0)
df = df.T

pairwise_combinations = list(combinations_with_replacement(df.columns, 2))
corrMatrix = pd.DataFrame(columns = df.columns, index = df.columns)
for i in pairwise_combinations:
    a, b = df.loc[:, i]
    corrMatrix[a][b] = dcor.distance_correlation(df[a], df[b])
corrMatrix= corrMatrix.apply(pd.to_numeric, errors='coerce')
corrMatrix = corrMatrix.fillna(corrMatrix.T)

g = sns.clustermap(corrMatrix, 
                         #metric='correlation',
                         method='average',
                         xticklabels=True, yticklabels=True, 
                         cmap='coolwarm', annot=False, fmt=".2f",
                         vmin=0.061, vmax=0.579,
                         #annot_kws={'size':6}, square=False,
                         dendrogram_ratio=(.1, .2),
                         cbar_pos=(1, .2, .03, .4))

triangle = corrMatrix.values[np.triu_indices_from(corrMatrix.values,1)]
median = np.median(triangle)
print(median)

g.savefig('clustermap.png', format='png', dpi=1200)