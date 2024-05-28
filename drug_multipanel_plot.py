#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 12:22:51 2023

@author: samael
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración estética para gráficos
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 24
plt.rcParams['axes.labelsize'] = 26
plt.rcParams['axes.titlesize'] = 26
sns.set_style('white')

# Definir etiquetas específicas para cada fármaco
etiquetas_farmacos = {
    'PF-00562271': [1, 2.5, 5],
    'Fluorouracil': [10, 12.5, 15]
}

# Nombres de las filas y otros parámetros iniciales
filas = ['PF-00562271']
Controles = ['Control', 'DMSO', 'D+Q']
colores = {'Control': '#b5b5b5', 'senescente': '#fdb4bf'}

# Obtén la lista de todos los archivos CSV en el directorio actual
archivos = [f for f in os.listdir('.') if f.endswith('.csv')]

# Identificar todos los fármacos únicos
farmacos = set()
for archivo in archivos:
    nombre_farmaco = archivo.split('_')[0]
    farmacos.add(nombre_farmaco)

# Crear un panel de 2 figuras (1x2)
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes = axes.flatten()  # Convierte la matriz de ejes en un array plano para facilitar el acceso

farmaco_idx = 0  # Índice para iterar sobre los fármacos

for farmaco in farmacos:
    if farmaco_idx >= 2:
        break  # Salir del bucle si ya hemos procesado 4 fármacos

    # Filtrar archivos por fármaco
    archivos_farmaco = [f for f in archivos if f.startswith(f'{farmaco}_')]
    archivos_Control = [f for f in archivos_farmaco if 'Control' in f]
    archivos_senescente = [f for f in archivos_farmaco if 'senescente' in f]

    grupos_archivos = {'Control': archivos_Control, 'senescente': archivos_senescente}

    # Generar las posiciones de las barras en el eje x
    etiquetas = etiquetas_farmacos[farmaco]  # Obtener etiquetas específicas para el fármaco actual
    x = np.arange(len(Controles + [f"{conc}" for conc in etiquetas]))

    for nombre_grupo, archivos_grupo in grupos_archivos.items():
        # Lista para almacenar los resultados de cada experimento
        resultados_experiments = []

        # Procesa cada archivo
        for archivo in archivos_grupo:
            datos = pd.read_csv(archivo, header=None)
            resultados = []
            for i, Control in enumerate(Controles):
                media = datos.iloc[0, i*3:i*3+3].mean()
                resultados.append({'Archivo': archivo, 'Grupo': Control, 'Media': media})

            for i, fila in enumerate(filas):
                for j, conc in enumerate(etiquetas):
                    media = datos.iloc[i + 1, j*3:j*3+3].mean()
                    grupo = f"{conc}"
                    resultados.append({'Archivo': archivo, 'Grupo': grupo, 'Media': media})

            resultados_experiments.append(pd.DataFrame(resultados))

        # Concatena todos los dataframes
        df_resultados = pd.concat(resultados_experiments)

        # Calcular la media y desviación estándar para cada grupo
        df_final = df_resultados.groupby('Grupo').agg({'Media': ['mean', 'std']})

        # Normalizar 'Control' a 1
        media_Control = df_final.loc['Control', ('Media', 'mean')]

        df_final[('DOR', '')] = df_final[('Media', 'mean')] / media_Control

        # Calcular SEM de 'DOR' y añadirlo al dataframe
        df_final[('DOR', 'sem')] = df_final[('Media', 'std')] / np.sqrt(df_resultados.groupby('Grupo').size())

        # Crear un orden para los grupos
        grupos_ordenados = Controles + [f"{conc}" for conc in etiquetas]

        # Convertir la columna 'Grupo' en una categoría y especificar el orden de las categorías
        df_final.reset_index(inplace=True)
        df_final['Grupo'] = pd.Categorical(df_final['Grupo'], categories=grupos_ordenados, ordered=True)

        # Ordenar los valores de acuerdo a la categoría
        df_final.sort_values('Grupo', inplace=True)

        # Crear un gráfico de barras en el subplot correspondiente
        ax = axes[farmaco_idx]
        barras = ax.bar(x - 0.2 + 0.4 * list(grupos_archivos.keys()).index(nombre_grupo), df_final[('DOR', '')], yerr=df_final[('DOR', 'sem')], color=colores[nombre_grupo], width=0.4, capsize=3)
        for barra in barras:
            #barra.set_edgecolor('black')
            pass

        # Configuración del subplot
        sns.despine(ax=ax)
        #ax.set_title(f'{farmaco}')
        ax.axhline(1, color='black', linestyle='--')
        ax.set_ylabel("Cell viability (% of Control)")

        # Establecer etiquetas para las barras
        ax.set_xticks(x)
        ax.set_xticklabels(grupos_ordenados, rotation=45, size=20)
        ax.tick_params(axis='y', labelsize=22)  # Aumentar el tamaño de la fuente de la graduación del eje y


    farmaco_idx += 1

# Ajustar el layout y guardar/mostrar el gráfico
plt.tight_layout()
plt.savefig('panel_farmacos_RS.png', dpi=900) 
