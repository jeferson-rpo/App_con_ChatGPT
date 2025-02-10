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

    # Correlaciones de 'Edad' y 'Ingreso_Anual_USD'
    correlation_edad_ingreso = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write(f"Correlación entre Edad e Ingreso_Anual_USD: {correlation_edad_ingreso}")

    # Umbral para determinar si la correlación es alta
    umbral_correlacion = 0.7  

    # Imputar 'Edad' según la correlación con 'Ingreso_Anual_USD' si la correlación es alta
    gdf['Edad'] = gdf.apply(
        lambda row: row['Ingreso_Anual_USD'] * correlation_edad_ingreso 
        if abs(correlation_edad_ingreso) > umbral_correlacion and pd.isna(row['Edad']) else row['Edad'], axis=1)

    # Imputar 'Latitud' y 'Longitud' si son NaN con su media
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Latitud'].mean())
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Longitud'].mean())

    # Imputar 'Frecuencia_Compra' utilizando el mapeo
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map)

    # Si hay valores fuera del rango esperado, se puede asignar un valor por defecto (por ejemplo, 'Media')
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(1)

    # Transformar los valores numéricos de vuelta a sus nombres correspondientes
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)

    # Correlación entre 'Edad' e 'Historial_Compras'
    correlation_edad_historial = gdf[['Edad', 'Historial_Compras']].corr().iloc[0, 1]
    st.write(f"Correlación entre Edad y Historial_Compras: {correlation_edad_historial}")

    # Crear una máscara para los NaN en 'Historial_Compras'
    nan_mask = gdf['Historial_Compras'].isna()

    # Si la correlación es alta, se calcula un valor para imputar 'Historial_Compras'
    if abs(correlation_edad_historial) > umbral_correlacion:
        # Multiplicamos la 'Edad' por la correlación y se asigna a los NaN
        gdf.loc[nan_mask, 'Historial_Compras'] = gdf.loc[nan_mask, 'Edad'] * correlation_edad_historial

    # Imputar 'Nombre' con el nombre más frecuente
    nombre_mas_frecuente = gdf['Nombre'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Nombre'] = gdf['Nombre'].fillna(nombre_mas_frecuente)

    # Imputar 'Género' con el género más frecuente
    genero_mas_frecuente = gdf['Género'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Género'] = gdf['Género'].fillna(genero_mas_frecuente)

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)
