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

    # Limpiar las columnas numéricas
    gdf_numéricas = gdf.select_dtypes(include=['float64', 'int64'])
    if not gdf_numéricas.empty:
        gdf[gdf_numéricas.columns] = gdf_numéricas.fillna(gdf_numéricas.mean())  # Rellenar NaN con la media

    # Limpiar las columnas de fechas
    gdf_fechas = gdf.select_dtypes(include=['object'])
    gdf_fechas = gdf_fechas.apply(pd.to_datetime, errors='coerce')  # Convertir a datetime, forzando errores a NaT
    if not gdf_fechas.empty:
        gdf[gdf_fechas.columns] = gdf_fechas.fillna(pd.to_datetime('1970-01-01'))  # Rellenar con fecha por defecto

    # Limpiar las columnas de texto sin usar lambda ni ciclos for
    gdf_texto = gdf.select_dtypes(include=['object'])
    if not gdf_texto.empty:
        # Obtener el valor más frecuente por cada columna de texto
        valores_frecuentes = gdf_texto.mode().iloc[0]
        gdf[gdf_texto.columns] = gdf_texto.fillna(valores_frecuentes)  # Rellenar NaN con el valor más frecuente

    # Asegurarse de que los tipos de datos sean coherentes
    gdf = gdf.convert_dtypes()

    # Mostrar el DataFrame limpio
    st.write("Archivo limpio:", gdf)
