import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Opción para cargar datos
def cargar_datos():
    opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))
    if opcion == "Cargar archivo desde URL":
        url = st.text_input("Introduce la URL del archivo CSV",
                            "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
        if url:
            return pd.read_csv(url)
    elif opcion == "Subir archivo":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            return pd.read_csv(archivo)
    return None

# Función para depurar datos
def depurar_datos(gdf):
    gdf = gdf.copy()
    
    # Identificar y rellenar NaN
    gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean(), inplace=True)
    gdf['Edad'].fillna(round(gdf['Edad'].mean()), inplace=True)
    gdf['Historial_Compras'].fillna(round(gdf['Historial_Compras'].mean()), inplace=True)
    gdf['Latitud'].fillna(gdf['Ingreso_Anual_USD'] * gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1], inplace=True)
    gdf['Longitud'].fillna(gdf['Ingreso_Anual_USD'] * gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1], inplace=True)
    gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1, inplace=True)
    gdf['Nombre'].fillna(gdf['Nombre'].mode()[0], inplace=True)
    gdf['Género'].fillna(gdf['Género'].mode()[0], inplace=True)
    
    # Limpiar valores en 'Frecuencia_Compra'
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map).fillna(1).map(frec_map_inv)
    
    return gdf

# Función para graficar correlaciones
def graficar_correlaciones(gdf):
    fig, axes = plt.subplots(3, 1, figsize=(10, 12))
    
    # Correlación global
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    axes[0].bar('Global', correlation_global, color='b')
    axes[0].set_title("Correlación Global entre Edad e Ingreso Anual USD")
    
    # Correlación por Género
    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    axes[1].bar(correlation_por_genero.index, correlation_por_genero.values, color='g')
    axes[1].set_title("Correlación entre Edad e Ingreso Anual USD por Género")
    
    # Correlación por Frecuencia de Compra
    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    axes[2].bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r')
    axes[2].set_title("Correlación entre Edad e Ingreso Anual USD por Frecuencia de Compra")
    
    plt.tight_layout()
    st.pyplot(fig)

# Interfaz principal
gdf = cargar_datos()
if gdf is not None:
    st.write("Datos cargados correctamente.")
    
    # Barra lateral con opciones
    with st.sidebar:
        if st.button("Depurar Datos"):
            gdf = depurar_datos(gdf)
            st.write("### Datos después de la limpieza:")
            st.write(gdf)
        
        if st.button("Mostrar Correlaciones"):
            gdf = depurar_datos(gdf)
            graficar_correlaciones(gdf)
