import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Opción para que el usuario ingrese una URL o suba un archivo
opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

# Si elige "Cargar archivo desde URL"
if opcion == "Cargar archivo desde URL":
    url = st.text_input("Introduce la URL del archivo CSV",
                       "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
    
    if url:
        gdf = pd.read_csv(url)
        st.write("Datos cargados desde la URL:", gdf)

# Si elige "Subir archivo"
if opcion == "Subir archivo":
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo:
        gdf = pd.read_csv(archivo)
        st.write("Datos cargados:", gdf)

# Limpiar los datos si se cargaron
if 'gdf' in locals():
    # Identificar los NaN en el DataFrame
    st.write("NaN en las columnas:", gdf.isna().sum()) 

    # Correlacionar Edad con Ingreso_Anual_USD
    correlation_edad = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Edad'] = gdf['Edad'].fillna(gdf['Ingreso_Anual_USD'] * correlation_edad)

    # Correlacionar Ingreso_Anual_USD con Latitud y Longitud
    correlation_latitud = gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    correlation_longitud = gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_latitud)
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_longitud)

    # Rellenar 'Frecuencia_Compra' con el valor más frecuente
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(gdf['Frecuencia_Compra'].mode()[0])

    # Rellenar 'Nombre' con el valor más frecuente
    gdf['Nombre'] = gdf['Nombre'].fillna(gdf['Nombre'].mode()[0])

    # Rellenar 'Sexo' con el valor más frecuente
    gdf['Sexo'] = gdf['Sexo'].fillna(gdf['Sexo'].mode()[0])

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)

    st.write("NaN en las columnas:", gdf.isna().sum())
