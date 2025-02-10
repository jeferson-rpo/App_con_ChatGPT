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

    # Calcular las correlaciones entre 'Ingreso_Anual_USD' y 'Latitud', 'Ingreso_Anual_USD' y 'Longitud'
    correlation_lat = gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    correlation_lon = gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]

    # Seleccionar la mayor correlación
    max_correlation = max(correlation_lat, correlation_lon)

    # Si la correlación más alta es mayor a 0.7, usamos la correlación para imputar 'Ingreso_Anual_USD'
    if max_correlation > 0.7:
        if correlation_lat == max_correlation:
            gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(
                gdf['Latitud'] * correlation_lat
            )
        else:
            gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(
                gdf['Longitud'] * correlation_lon
            )
    else:
        # Si la correlación no es suficiente, se imputa con la media
        gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean())

    # Imputar 'Nombre' con el nombre más frecuente
    nombre_mas_frecuente = gdf['Nombre'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Nombre'] = gdf['Nombre'].fillna(nombre_mas_frecuente)

    # Imputar 'Género' con el género más frecuente
    genero_mas_frecuente = gdf['Género'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Género'] = gdf['Género'].fillna(genero_mas_frecuente)

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)
