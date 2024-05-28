import pandas as pd
from scipy.spatial.distance import squareform, pdist

"""
# The kockdown file can be obtain from the original source: 
https://github.com/dhimmel/lincs/blob/b36dfd82b6b1aa0b0c45ec905cb2548ddf7dc53e/data/consensi/consensi-knockdown.tsv.gz
"""
df = pd.read_csv('knockdown.csv')
distances = pd.DataFrame(squareform(pdist(df.iloc[:, 1:])), columns=df.perturbagen.unique(), index=df.perturbagen.unique())

distances.to_csv('knockdown_distances.csv', index=False)