import pandas as pd
import numpy as np
import streamlit as st

# Función para limpiar el archivo
def limpiar_archivo(gdf):
    # Identificar columnas de tipo numérico
    gdf_numéricas = gdf.select_dtypes(include=['float64', 'int64'])  # Columnas numéricas
    gdf_numéricas = gdf_numéricas.interpolate()  # Interpolación para numéricas

    # Identificar columnas de tipo fecha (convertir a datetime)
    gdf_fechas = gdf.select_dtypes(include=['object'])  # Se seleccionan columnas de fechas (de tipo objeto)
    gdf_fechas = gdf_fechas.apply(pd.to_datetime, errors='coerce')  # Convertir a datetime, manejando errores
    gdf_fechas = gdf_fechas.interpolate()  # Interpolación para fechas

    # Identificar columnas de texto
    gdf_texto = gdf.select_dtypes(include=['object'])  # Columnas de tipo texto
    frecuente = gdf_texto.mode().iloc[0]  # Obtener el valor más frecuente en cada columna de texto
    gdf_texto = gdf_texto.fillna(frecuente)  # Rellenar NaN con el valor más frecuente

    # Combinar todos los DataFrames
    gdf_limpio = pd.concat([gdf_numéricas, gdf_fechas, gdf_texto], axis=1)

    return gdf_limpio

# Función para cargar el archivo
def cargar_archivo():
    # Opción para cargar desde archivo local o desde URL
    opcion = st.radio("¿Cómo te gustaría cargar los datos?", ("Subir archivo", "Ingresar URL"))

    if opcion == "Subir archivo":
        archivo = st.file_uploader("Subir archivo CSV", type=["csv"])
        if archivo is not None:
            # Leer el archivo CSV
            gdf = pd.read_csv(archivo)
            return gdf

    elif opcion == "Ingresar URL":
        url = st.text_input("Ingresa la URL del archivo CSV")
        if url:
            # Leer el archivo desde la URL
            gdf = pd.read_csv(url)
            return gdf

    return None

# Cargar el archivo al inicio
gdf = cargar_archivo()

# Si se cargó el archivo, limpiar y mostrar
if gdf is not None:
    # Limpiar el DataFrame
    gdf_limpio = limpiar_archivo(gdf)
    # Mostrar el DataFrame limpio
    st.write("Archivo limpio:", gdf_limpio)
