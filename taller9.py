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

    # Correlación entre 'Edad' y 'Historial_Compras'
    correlation_edad_historial = gdf[['Edad', 'Historial_Compras']].corr().iloc[0, 1]
    st.write(f"Correlación entre Edad y Historial_Compras: {correlation_edad_historial}")

    # Si la correlación es alta, rellenamos los NaN de 'Historial_Compras' basándonos en la Edad
    umbral_correlacion = 0.7  # Umbral para determinar si la correlación es alta

    # Solo realizamos la imputación si la correlación supera el umbral
    if abs(correlation_edad_historial) > umbral_correlacion:
        # Crear una máscara para las filas con NaN en 'Historial_Compras'
        mask_na = gdf['Historial_Compras'].isna()

        # Crear un DataFrame temporal solo con las filas que no tienen NaN en 'Historial_Compras'
        gdf_no_na = gdf.dropna(subset=['Historial_Compras'])

        # Establecer un rango de edad dentro del cual buscar las filas más cercanas (±5 años)
        rango_edad = 5

        # Calcular la diferencia absoluta de edad entre todas las filas
        dif_edad = np.abs(gdf['Edad'].values[:, None] - gdf_no_na['Edad'].values)

        # Filtrar solo las filas donde la diferencia de edad sea menor o igual a 5 años
        mask_rango = dif_edad <= rango_edad

        # Usar la máscara para encontrar el valor de 'Historial_Compras' más cercano
        # Reemplazar los NaN en 'Historial_Compras' con el valor de la fila más cercana en el rango de ±5 años
        valores_historial_compras = np.array([gdf_no_na['Historial_Compras'].values] * len(gdf))
        valores_historial_compras[~mask_rango] = np.nan  # Establecer en NaN los valores que no cumplen el rango

        # Tomar el valor más cercano para cada fila con NaN
        gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(pd.Series(np.nanmin(valores_historial_compras, axis=1)))

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
