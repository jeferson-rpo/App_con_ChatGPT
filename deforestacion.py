import streamlit as st
import pandas as pd

# Opción para que el usuario ingrese una URL o suba un archivo
opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

# Si elige "Cargar archivo desde URL"
if opcion == "Cargar archivo desde URL":
    url = st.text_input("Introduce la URL del archivo CSV", 
                       "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv")
    if url:
        gdf = pd.read_csv(url)  # Cargar el archivo CSV desde la URL
        st.write("Datos cargados desde la URL:", gdf)

# Si elige "Subir archivo"
if opcion == "Subir archivo":
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo:
        gdf = pd.read_csv(archivo)  # Cargar el archivo CSV
        st.write("Datos cargados:", gdf)

# Limpiar los datos si se cargaron
if 'gdf' in locals():  # Verificar si se cargaron datos
    # Identificar los NaN en el DataFrame
    st.write("NaN en las columnas:", gdf.isna().sum())

    # Limpiar las columnas numéricas: rellenar NaN con la media
    gdf_numéricas = gdf.select_dtypes(include=['float64', 'int64'])
    gdf[gdf_numéricas.columns] = gdf_numéricas.fillna(gdf_numéricas.mean())  # Reemplazar NaN con la media

    # Limpiar las columnas de fechas: convertir a datetime y rellenar NaT con una fecha por defecto
    gdf_fechas = gdf.select_dtypes(include=['object']).apply(pd.to_datetime, errors='coerce')
    gdf[gdf_fechas.columns] = gdf_fechas.fillna(pd.to_datetime('1970-01-01'))  # Fecha por defecto para NaT

    # Limpiar las columnas de texto: rellenar NaN con el valor más frecuente
    gdf_texto = gdf.select_dtypes(include=['object'])
    valores_frecuentes = gdf_texto.mode().iloc[0]
    gdf[gdf_texto.columns] = gdf_texto.fillna(valores_frecuentes)  # Rellenar NaN con el valor más frecuente

    # Asegurarse de que los tipos de datos sean coherentes después de la limpieza
    gdf = gdf.convert_dtypes()

    # Mostrar el DataFrame limpio
    st.write("Archivo limpio:", gdf)

