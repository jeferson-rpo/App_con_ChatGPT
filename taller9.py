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

    # Ahora, con 'Ingreso_Anual_USD' imputado, calcular la correlación de 'Edad' con 'Ingreso_Anual_USD'
    correlation_edad_ingreso = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    
    # Establecer un umbral para imputar según la correlación
    umbral_correlacion = 0.7  # Puedes ajustar este umbral a tu criterio
    
    # Imputar 'Edad' según la correlación con 'Ingreso_Anual_USD'
    gdf['Edad'] = gdf.apply(lambda row: row['Ingreso_Anual_USD'] * correlation_edad_ingreso if abs(correlation_edad_ingreso) > umbral_correlacion and pd.isna(row['Edad']) else row['Edad'], axis=1)

    # Imputar 'Latitud' y 'Longitud' si son NaN con su media
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Latitud'].mean())
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Longitud'].mean())

    # Imputar 'Frecuencia_Compra' con la mediana si tiene NaN
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map)
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(1)

    # Transformar los valores numéricos de vuelta a sus nombres correspondientes
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)

    # Calcular correlación de 'Historial_Compras' con 'Latitud' y 'Longitud'
    correlation_latitud_historial = gdf[['Latitud', 'Historial_Compras']].corr().iloc[0, 1]
    correlation_longitud_historial = gdf[['Longitud', 'Historial_Compras']].corr().iloc[0, 1]
    
    # Establecer un umbral para imputar según la correlación
    umbral_historial = 0.7  # Ajusta este umbral según tus necesidades

    # Imputar 'Historial_Compras' según la correlación con 'Latitud' y 'Longitud'
    gdf['Historial_Compras'] = gdf.apply(lambda row: row['Latitud'] * correlation_latitud_historial + row['Longitud'] * correlation_longitud_historial if abs(correlation_latitud_historial) > umbral_historial and pd.isna(row['Historial_Compras']) else row['Historial_Compras'], axis=1)

    # Imputar 'Nombre' con el nombre más frecuente
    nombre_mas_frecuente = gdf['Nombre'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Nombre'] = gdf['Nombre'].fillna(nombre_mas_frecuente)

    # Imputar 'Género' con el género más frecuente
    genero_mas_frecuente = gdf['Género'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Género'] = gdf['Género'].fillna(genero_mas_frecuente)

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)
