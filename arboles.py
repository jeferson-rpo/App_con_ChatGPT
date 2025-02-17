import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from unidecode import unidecode
import numpy as np
from matplotlib import cm

def cargar_datos():
    """
    Permite al usuario cargar un archivo CSV desde una URL o mediante carga manual.
    """
    opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

    if opcion == "Cargar archivo desde URL":
        url = st.text_input("Ingresa la URL del archivo CSV")
        if url:
            return pd.read_csv(url)

    elif opcion == "Subir archivo":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            return pd.read_csv(archivo)

def cargar_datos_municipios():
    """
    Carga el archivo de municipios directamente desde la URL proporcionada.
    """
    url_municipios = "https://raw.githubusercontent.com/jeferson-rpo/App_con_ChatGPT/refs/heads/main/DIVIPOLA-_C_digos_municipios_geolocalizados_20250217.csv"
    df_municipios = pd.read_csv(url_municipios)

    # Normalizar los nombres de los municipios (quitar tildes y convertir a minúsculas)
    df_municipios['NOM_MPIO'] = df_municipios['NOM_MPIO'].str.lower().apply(unidecode)
    
    # Seleccionar solo las columnas necesarias
    df_municipios = df_municipios[['NOM_MPIO', 'LATITUD', 'LONGITUD', 'Geo Municipio']]
    
    return df_municipios

def cargar_y_relacionar_datos():
    """
    Carga los datos de madera movilizada y los relaciona con los municipios.
    """
    df_madera = cargar_datos()
    df_municipios = cargar_datos_municipios()

    # Normalizar los nombres de los municipios (quitar tildes y convertir a minúsculas) en df_madera usando vectorización
    df_madera['MUNICIPIO'] = df_madera['MUNICIPIO'].str.lower().apply(unidecode)

    # Relacionar los datos de madera movilizada con los municipios
    df_relacionado = df_madera.merge(df_municipios, how="left", left_on="MUNICIPIO", right_on="NOM_MPIO").drop(columns=["NOM_MPIO"])
    
    return df_relacionado

def graficar_mapa_calor(gdf):
    """
    Genera un mapa de calor de la madera movilizada basado en el volumen por municipio.

    Args:
        gdf (pd.DataFrame): DataFrame con las coordenadas y el volumen de madera movilizada.
    """
    # Usar un mapa de calor para representar el volumen de madera movilizada
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Normalizar el volumen de madera movilizada entre 0 y 1 para la coloración
    gdf['VOLUMEN NORM'] = np.log1p(gdf['VOLUMEN M3'])  # Usamos log1p para evitar problemas con valores pequeños
    
    # Crear el mapa de calor usando los colores del mapa 'YlOrRd'
    sc = ax.scatter(gdf['LONGITUD'], gdf['LATITUD'], c=gdf['VOLUMEN NORM'], cmap='YlOrRd', s=50, alpha=0.75)
    
    # Agregar título
    ax.set_title('Mapa de Calor de Madera Movilizada', fontsize=15)
    
    # Agregar una barra de color
    fig.colorbar(sc, ax=ax, label='Volumen Madera Movilizada (Log)')
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

st.title("Análisis de Madera Movilizada")

# Cargar datos
gdf = cargar_y_relacionar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Graficar mapa de calor
    graficar_mapa_calor(gdf)
