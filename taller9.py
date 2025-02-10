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

    # Rellenar NaN en 'Ingreso_Anual_USD' con el promedio de la columna
    promedio_ingreso = gdf['Ingreso_Anual_USD'].mean()
    gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(promedio_ingreso)

    # Rellenar NaN en 'Historial_Compras' con el valor entero más cercano al promedio
    promedio_historial = gdf['Historial_Compras'].mean()
    valor_entero_historial = round(promedio_historial)  # Redondear al entero más cercano
    gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(valor_entero_historial)

    # Rellenar NaN en 'Edad' utilizando la correlación con 'Ingreso_Anual_USD'
    correlation_edad_ingreso = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Edad'] = gdf['Edad'].fillna(gdf['Ingreso_Anual_USD'] * correlation_edad_ingreso)

    # Rellenar NaN en 'Latitud' utilizando la correlación con 'Ingreso_Anual_USD'
    correlation_latitud = gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_latitud)

    # Rellenar NaN en 'Longitud' utilizando la correlación con 'Ingreso_Anual_USD'
    correlation_longitud = gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_longitud)

    # Imputar 'Frecuencia_Compra' usando la relación con 'Edad'
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1)

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
