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
        gdf = pd.read_csv(archivo)  # Cargar el archivo CSV desde el archivo subido
        st.write("Datos cargados desde el archivo:", gdf)

# Procedemos con la limpieza de datos después de cargar el archivo
if 'gdf' in locals():  # Verificar si se cargaron datos
    # Identificar tipo de datos
    tipos_columnas = gdf.dtypes

    # Limpiar el DataFrame
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

    # Combinar todos los DataFrames limpios
    gdf_limpio = gdf_numéricas.join(gdf_fechas).join(gdf_texto)

    # Mostrar el DataFrame limpio
    st.write("Archivo limpio:", gdf_limpio)
