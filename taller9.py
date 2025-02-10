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

    # Calcular la correlación entre 'Edad' e 'Ingreso_Anual_USD'
    correlation_edad_ingreso = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]

    # Rellenar NaN en 'Edad' utilizando la correlación con 'Ingreso_Anual_USD'
    gdf['Edad'] = gdf['Edad'].fillna(gdf['Ingreso_Anual_USD'] * correlation_edad_ingreso)

    # Calcular la correlación entre 'Latitud', 'Longitud' e 'Ingreso_Anual_USD'
    correlation_latitud = gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    correlation_longitud = gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]

    # Seleccionar la mayor correlación
    max_correlation = max(correlation_latitud, correlation_longitud)

    # Si la correlación más alta es mayor a 0.7, se usa esa correlación para imputar 'Ingreso_Anual_USD'
    if max_correlation > 0.7:
        if correlation_latitud == max_correlation:
            gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(
                gdf['Latitud'] * correlation_latitud
            )
        else:
            gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(
                gdf['Longitud'] * correlation_longitud
            )
    else:
        # Si la correlación no es suficiente, se imputa con la media
        gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean())

    # Imputar 'Frecuencia_Compra' usando la relación con 'Edad'
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1)

    # Imputar 'Historial_Compras' usando la relación entre 'Latitud', 'Longitud' e 'Ingreso_Anual_USD'
    correlation_latitud_historial = gdf[['Latitud', 'Historial_Compras']].corr().iloc[0, 1]
    correlation_longitud_historial = gdf[['Longitud', 'Historial_Compras']].corr().iloc[0, 1]
    
    # Rellenar NaN en 'Historial_Compras' utilizando las correlaciones con 'Latitud' y 'Longitud'
    gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(
        gdf['Latitud'] * correlation_latitud_historial + gdf['Longitud'] * correlation_longitud_historial
    )

    # Imputar 'Nombre' con el nombre más frecuente
    nombre_mas_frecuente = gdf['Nombre'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Nombre'] = gdf['Nombre'].fillna(nombre_mas_frecuente)

    # Imputar 'Género' con el género más frecuente
    genero_mas_frecuente = gdf['Género'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Género'] = gdf['Género'].fillna(genero_mas_frecuente)

    # Limpiar los valores de 'Frecuencia_Compra' asegurando que solo tenga valores válidos
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map)

    # Si hay valores fuera del rango esperado, se puede asignar un valor por defecto (por ejemplo, 'Media')
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(1)

    # Transformar los valores numéricos de vuelta a sus nombres correspondientes
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)
