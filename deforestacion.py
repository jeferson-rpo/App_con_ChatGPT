import streamlit as st
import pandas as pd

# Título de la app
st.title("Análisis de la Deforestación")
st.markdown("Este análisis permite visualizar las áreas deforestadas en el Amazonas.")

# Subir el archivo CSV
archivo = st.file_uploader("Sube un archivo CSV", type=["csv"])

# Intentar cargar el archivo y asignar un DataFrame vacío si no se ha cargado un archivo
try:
    gdf = pd.read_csv(archivo)
except:
    gdf = pd.DataFrame()



# Mostrar los primeros registros para verificar la carga de datos
st.write(gdf.head())

import pandas as pd

# Cargar el archivo CSV
gdf = pd.read_csv(archivo)  # archivo cargado previamente

# Identificar tipo de datos
tipos_columnas = gdf.dtypes

# Interpolación para columnas numéricas (como latitudes y fechas)
gdf_numéricas = gdf.select_dtypes(include=['float64', 'int64'])  # Columnas numéricas
gdf_numéricas = gdf_numéricas.interpolate()  # Interpolación para numéricas

# Interpolación para fechas
gdf_fechas = gdf.select_dtypes(include=['object'])  # Se seleccionan columnas de fechas (de tipo objeto)
gdf_fechas = gdf_fechas.apply(pd.to_datetime, errors='coerce')  # Convertir a datetime, manejando errores
gdf_fechas = gdf_fechas.interpolate()  # Interpolación para fechas

# Rellenar NaN en texto con el valor más frecuente
gdf_texto = gdf.select_dtypes(include=['object'])  # Columnas de tipo texto
frecuente = gdf_texto.mode().iloc[0]  # Obtener el valor más frecuente en cada columna de texto
gdf_texto = gdf_texto.fillna(frecuente)  # Rellenar NaN con el valor más frecuente

# Combinar todos los DataFrames
gdf_limpio = gdf_numéricas.join(gdf_fechas).join(gdf_texto)

# Mostrar el DataFrame limpio
print(gdf_limpio)

