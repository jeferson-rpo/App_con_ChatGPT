import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Título de la app
st.title("Análisis de la Deforestación")
st.markdown("Este análisis permite visualizar las áreas deforestadas en el Amazonas.")

# Subir el archivo CSV
archivo = st.file_uploader("Sube un archivo CSV", type=["csv"])

# Cargar el archivo CSV directamente al DataFrame
gdf = pd.read_csv(archivo)  # No hay necesidad de if

# Realizar la interpolación en las columnas de interés
gdf[['Latitud', 'Longitud', 'Altitud', 'Precipitacion']] = gdf[['Latitud', 'Longitud', 'Altitud', 'Precipitacion']].interpolate()

# Mostrar los primeros registros para verificar la carga de datos
st.write(gdf.head())



