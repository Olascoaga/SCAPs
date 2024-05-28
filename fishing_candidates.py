import pandas as pd
from random import choices
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Is in files directory
ffile = open("SCAPS21.txt", "r") 
scaps = ffile.readlines()
scaps = list(map(lambda s: s.strip(), scaps))

# Generated with distance_calculation script and the original knockdown.csv file
df = pd.read_csv('distance_correlation.csv') 
df = df[~df['perturbagen'].isin(scaps)]
genes = df['perturbagen'].tolist()
df = df.set_index(df['perturbagen'])

df = df.reindex(columns=scaps)
df['median'] = df.median(axis=1)
df = df.loc[df['median'] > 0.405]