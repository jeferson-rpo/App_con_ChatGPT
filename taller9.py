import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def cargar_datos():
    """
    Carga y depuración de datos desde un archivo CSV o URL.
    """
    opcion = st.sidebar.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))
    gdf = None
    if opcion == "Cargar archivo desde URL":
        url = st.sidebar.text_input("Introduce la URL del archivo CSV",
                                   "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
        if url:
            gdf = pd.read_csv(url)
    elif opcion == "Subir archivo":
        archivo = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            gdf = pd.read_csv(archivo)
    
    if gdf is not None:
        st.write("Datos cargados:", gdf.head())
        return depurar_datos(gdf)
    return None

def depurar_datos(gdf):
    """
    Limpia los datos imputando valores faltantes.
    """
    st.write("NaN en las columnas antes de la limpieza:", gdf.isna().sum())
    
    gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean())
    gdf['Edad'] = gdf['Edad'].fillna(round(gdf['Edad'].mean()))
    gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(round(gdf['Historial_Compras'].mean()))
    
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1)
    gdf['Nombre'] = gdf['Nombre'].fillna(gdf['Nombre'].mode()[0])
    gdf['Género'] = gdf['Género'].fillna(gdf['Género'].mode()[0])
    
    # Mapear valores de frecuencia de compra
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map).fillna(1)
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)
    
    st.write("Datos después de la limpieza:", gdf.head())
    return gdf

def mostrar_correlaciones(gdf):
    """
    Muestra gráficos de correlaciones global y segmentadas.
    """
    st.sidebar.subheader("Análisis de Correlaciones")
    opcion = st.sidebar.radio("Selecciona el tipo de análisis", ["Global", "Por Género", "Por Frecuencia de Compra"])
    
    if opcion == "Global":
        correlation = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
        fig, ax = plt.subplots()
        ax.bar("Global", correlation, color='b')
        ax.set_title("Correlación Global: Edad vs Ingreso Anual")
        ax.set_ylabel("Correlación")
        st.pyplot(fig)
    
    elif opcion == "Por Género":
        correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
        fig, ax = plt.subplots()
        ax.bar(correlation_por_genero.index, correlation_por_genero.values, color='g')
        ax.set_title("Correlación por Género: Edad vs Ingreso Anual")
        ax.set_ylabel("Correlación")
        st.pyplot(fig)
    
    elif opcion == "Por Frecuencia de Compra":
        correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
        fig, ax = plt.subplots()
        ax.bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r')
        ax.set_title("Correlación por Frecuencia de Compra")
        ax.set_ylabel("Correlación")
        st.pyplot(fig)

# Interfaz principal
gdf = cargar_datos()
if gdf is not None:
    mostrar_correlaciones(gdf)
