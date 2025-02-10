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

    # Rellenar NaN en 'Edad' con el valor entero más cercano al promedio
    promedio_edad = gdf['Edad'].mean()
    valor_entero_edad = round(promedio_edad)
    gdf['Edad'] = gdf['Edad'].fillna(valor_entero_edad)

    # Rellenar NaN en 'Historial_Compras' con el valor entero más cercano al promedio
    promedio_historial = gdf['Historial_Compras'].mean()
    valor_entero_historial = round(promedio_historial)
    gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(valor_entero_historial)

    # Rellenar NaN en 'Latitud' utilizando la correlación con 'Ingreso_Anual_USD'
    correlation_latitud = gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_latitud)

    # Rellenar NaN en 'Longitud' utilizando la correlación con 'Ingreso_Anual_USD'
    correlation_longitud = gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_longitud)

    # Imputar 'Frecuencia_Compra' usando la relación con 'Edad'
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1)

    # Imputar 'Nombre' con el nombre más frecuente
    nombre_mas_frecuente = gdf['Nombre'].mode()[0]
    gdf['Nombre'] = gdf['Nombre'].fillna(nombre_mas_frecuente)

    # Imputar 'Género' con el género más frecuente
    genero_mas_frecuente = gdf['Género'].mode()[0]
    gdf['Género'] = gdf['Género'].fillna(genero_mas_frecuente)

    # Limpiar los valores de 'Frecuencia_Compra'
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map)
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(1)
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)

    # --- FUNCIONALIDAD SOLICITADA: Análisis de correlaciones ---

    # Correlación global entre 'Edad' e 'Ingreso_Anual_USD'
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write(f"Correlación global entre Edad e Ingreso Anual USD: {correlation_global:.2f}")

    # Correlación por Género
    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Género:")
    st.write(correlation_por_genero)

    # Correlación por Frecuencia de Compra
    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Frecuencia de Compra:")
    st.write(correlation_por_frecuencia)

    # --- VISUALIZACIÓN DE RESULTADOS ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # Correlación global
    ax.bar('Global', correlation_global, color='b', label='Global')

    # Correlación por género
    ax.bar(correlation_por_genero.index, correlation_por_genero.values, color='g', label='Por Género')

    # Correlación por frecuencia de compra
    ax.bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r', label='Por Frecuencia de Compra')

    ax.set_title("Correlación entre Edad e Ingreso Anual USD")
    ax.set_ylabel("Correlación")
    ax.legend(loc='best')
    st.pyplot(fig)
