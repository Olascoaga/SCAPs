# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:39:41 2024

@author: olask
"""

import pandas as pd
import numpy as np

nombre_archivo = 'Elderly.sort' 
punto_de_corte = 0.131 # Ajusta esto al punto de corte deseado

# Leer el archivo
datos = pd.read_csv(nombre_archivo, sep='\t', header=None)

# Identificar todos los identificadores únicos
ids_unicos = np.unique(datos[[0, 1]].values.ravel())

# Crear una matriz cuadrada vacía
matriz_cuadrada = pd.DataFrame(index=ids_unicos, columns=ids_unicos).fillna(0)

# Llenar la matriz cuadrada
for _, fila in datos.iterrows():
    i, j, valor = fila[0], fila[1], fila[2]
    if valor < punto_de_corte:
        pass
    else:
        matriz_cuadrada.at[i, j] = valor # Asigna el valor al triángulo superior
        matriz_cuadrada.at[j, i] = valor # Asigna el mismo valor al triángulo inferior

# Guardar los datos modificados
matriz_cuadrada.to_csv('Elderly_razor.csv', sep='\t', index=True, header=False)