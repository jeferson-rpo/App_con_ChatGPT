import streamlit as st
import pandas as pd
import numpy as np

# Solicitar al usuario si desea subir un archivo o proporcionar una URL
opcion = st.selectbox("¿Cómo te gustaría cargar los datos?", ["Subir archivo", "Ingresar URL"])

# Cargar el archivo según la opción seleccionada
if opcion == "Subir archivo":
    archivo = st.file_uploader("Sube tu archivo CSV", type="csv")
    if archivo is not None:
        gdf = pd.read_csv(archivo)
        st.write("Datos cargados:", gdf)

elif opcion == "Ingresar URL":
    url = st.text_input("Ingresa la URL del archivo CSV")
    if url:
        gdf = pd.read_csv(url)
        st.write("Datos cargados desde la URL:", gdf)

# Limpiar los datos según el tipo de columna
def limpiar_datos(gdf):
    # Identificar tipos de datos de cada columna
    column_types = gdf.dtypes

    # Interpolación para columnas numéricas (Latitudes y Longitudes)
    gdf[['Latitud', 'Longitud']] = gdf[['Latitud', 'Longitud']].apply(pd.to_numeric, errors='coerce')
    gdf[['Latitud', 'Longitud']] = gdf[['Latitud', 'Longitud']].apply(lambda col: col.interpolate())

    # Promedio para columnas numéricas
    numerical_columns = gdf.select_dtypes(include=[np.number]).columns
    gdf[numerical_columns] = gdf[numerical_columns].apply(lambda col: col.fillna(col.mean()))

    # Interpolación para columnas de fecha
    gdf['Fecha'] = pd.to_datetime(gdf['Fecha'], errors='coerce')
    gdf['Fecha'] = gdf['Fecha'].interpolate()

    # Sustituir valores NaN de texto por el valor más frecuente
    text_columns = gdf.select_dtypes(include=[object]).columns
    gdf[text_columns] = gdf[text_columns].apply(lambda col: col.fillna(col.mode()[0]))

    return gdf

# Limpiar los datos una vez cargados
if 'gdf' in locals():
    gdf_limpio = limpiar_datos(gdf)
    st.write("Datos limpios:", gdf_limpio)


