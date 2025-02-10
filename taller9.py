import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Opción para que el usuario ingrese una URL o suba un archivo
opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

# Cargar archivo según opción seleccionada
if opcion == "Cargar archivo desde URL":
    url = st.text_input("Introduce la URL del archivo CSV",
                        "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
    if url:
        gdf = pd.read_csv(url)
        st.write("Datos cargados desde la URL:", gdf)

if opcion == "Subir archivo":
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo:
        gdf = pd.read_csv(archivo)
        st.write("Datos cargados:", gdf)

# Procesar y limpiar datos
if 'gdf' in locals():
    # Rellenar valores nulos en columnas relevantes
    gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean(), inplace=True)
    gdf['Edad'].fillna(round(gdf['Edad'].mean()), inplace=True)

    # Análisis de correlaciones
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    
    # --- VISUALIZACIÓN ---
    # Gráfica de correlación global
    fig_global, ax_global = plt.subplots()
    ax_global.bar(['Global'], [correlation_global], color='b')
    ax_global.set_title("Correlación Global entre Edad e Ingreso Anual USD")
    ax_global.set_ylabel("Correlación")
    st.pyplot(fig_global)

    # Gráfica de correlación por género
    fig_genero, ax_genero = plt.subplots()
    ax_genero.bar(correlation_por_genero.index, correlation_por_genero.values, color='g')
    ax_genero.set_title("Correlación entre Edad e Ingreso Anual USD por Género")
    ax_genero.set_ylabel("Correlación")
    st.pyplot(fig_genero)

    # Gráfica de correlación por frecuencia de compra
    fig_frecuencia, ax_frecuencia = plt.subplots()
    ax_frecuencia.bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r')
    ax_frecuencia.set_title("Correlación entre Edad e Ingreso Anual USD por Frecuencia de Compra")
    ax_frecuencia.set_ylabel("Correlación")
    st.pyplot(fig_frecuencia)
