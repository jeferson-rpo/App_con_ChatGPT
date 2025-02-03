import streamlit as st
import pandas as pd

# Preguntar al usuario si desea subir un archivo o cargar desde URL
opcion = st.radio("¿Cómo quieres cargar los datos?", ('Subir archivo', 'Cargar desde URL'))

if opcion == 'Subir archivo':
    archivo = st.file_uploader("Sube un archivo CSV", type=["csv"])
    if archivo is not None:
        # Leer el archivo
        gdf = pd.read_csv(archivo)
        st.write("Archivo cargado correctamente.")
elif opcion == 'Cargar desde URL':
    url = st.text_input("Introduce la URL del archivo CSV")
    if url:
        # Leer el archivo desde la URL
        gdf = pd.read_csv(url)
        st.write("Archivo cargado desde URL correctamente.")


