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
