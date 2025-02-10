import streamlit as st
import pandas as pd
import numpy as np
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

    # Imputar 'Ingreso_Anual_USD' con el promedio si tiene NaN
    ingreso_promedio = gdf['Ingreso_Anual_USD'].mean()
    gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(ingreso_promedio)

    # Imputar 'Edad' con la mediana si tiene NaN (más robusto que la correlación)
    edad_mediana = gdf['Edad'].median()
    gdf['Edad'] = gdf['Edad'].fillna(edad_mediana)

    # Correlaciones de 'Edad' y 'Ingreso_Anual_USD'
    correlation_edad_ingreso = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write(f"Correlación entre Edad e Ingreso_Anual_USD: {correlation_edad_ingreso}")

    # Imputar 'Edad' según la correlación con 'Ingreso_Anual_USD'
    umbral_correlacion = 0.7  # Umbral para determinar si la correlación es alta
    gdf['Edad'] = gdf.apply(lambda row: row['Ingreso_Anual_USD'] * correlation_edad_ingreso if abs(correlation_edad_ingreso) > umbral_correlacion and pd.isna(row['Edad']) else row['Edad'], axis=1)

    # Imputar 'Latitud' y 'Longitud' si son NaN con su media
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Latitud'].mean())
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Longitud'].mean())

    # Correlación entre 'Edad' y 'Historial_Compras'
    correlation_edad_historial = gdf[['Edad', 'Historial_Compras']].corr().iloc[0, 1]
    st.write(f"Correlación entre Edad y Historial_Compras: {correlation_edad_historial}")

    # Definir umbral para la correlación
    umbral_historial = 0.7

    # Rellenar NaN en 'Historial_Compras' utilizando la correlación con 'Edad' si la correlación es alta
    if abs(correlation_edad_historial) > umbral_historial:
        # Vectorizamos la imputación de valores de 'Historial_Compras' basándonos en la correlación con 'Edad'
        gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(gdf['Edad'] * correlation_edad_historial)

    # Imputar 'Frecuencia_Compra' utilizando el mapeo
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map)

    # Si hay valores fuera del rango esperado, se puede asignar un valor por defecto (por ejemplo, 'Media')
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(1)

    # Transformar los valores numéricos de vuelta a sus nombres correspondientes
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)
