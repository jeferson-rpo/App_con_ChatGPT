import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import zipfile
import requests
import io

# Cargar el archivo CSV de madera movilizada (código previamente mencionado)
def cargar_datos():
    """
    Permite al usuario cargar un archivo CSV desde una URL o mediante carga manual.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.
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
    Carga el archivo de municipios desde la URL proporcionada.

    Returns:
        pd.DataFrame: DataFrame con los datos de municipios.
    """
    url_municipios = "https://raw.githubusercontent.com/jeferson-rpo/App_con_ChatGPT/refs/heads/main/DIVIPOLA-_C_digos_municipios_geolocalizados_20250217.csv"
    df_municipios = pd.read_csv(url_municipios)

    # Normalizar los nombres de los municipios (quitar tildes y convertir a minúsculas)
    df_municipios['NOM_MPIO'] = df_municipios['NOM_MPIO'].str.lower().apply(unidecode)
    
    # Seleccionar solo las columnas necesarias
    df_municipios = df_municipios[['NOM_MPIO', 'LATITUD', 'LONGITUD', 'Geo Municipio']]
    
    return df_municipios

def cargar_mapa_colombia():
    """
    Carga y filtra el mapa de Colombia desde el archivo proporcionado.

    Returns:
        geopandas.GeoDataFrame: Mapa de Colombia.
    """
    # URL del mapa de países
    url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"

    # Descargar y descomprimir el archivo
    with requests.get(url) as r:
        with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
            # Extraer el archivo de países
            zip_ref.extractall("/tmp/")

    # Cargar el shapefile de países
    shapefile_path = "/tmp/ne_50m_admin_0_countries.shp"
    world = gpd.read_file(shapefile_path)

    # Filtrar el GeoDataFrame para solo incluir Colombia
    colombia = world[world['NAME'] == 'Colombia']

    return colombia

def generar_mapa_calor(gdf, mapa_colombia):
    """
    Genera un mapa de calor sobre el mapa de Colombia, usando las coordenadas de los municipios y el volumen de madera movilizada.
    
    Args:
        gdf (GeoDataFrame): Datos de madera movilizada.
        mapa_colombia (GeoDataFrame): Mapa de Colombia.
    """
    # Crear el mapa base centrado en Colombia
    mapa_base = folium.Map(location=[4.5709, -74.2973], zoom_start=6)

    # Agregar el mapa de Colombia al mapa base
    folium.GeoJson(mapa_colombia).add_to(mapa_base)

    # Preparar los datos para el mapa de calor
    heat_data = [
        [row['LATITUD'], row['LONGITUD'], row['VOLUMEN M3']] 
        for idx, row in gdf.iterrows()
        if pd.notna(row['LATITUD']) and pd.notna(row['LONGITUD']) and pd.notna(row['VOLUMEN M3'])
    ]

    # Agregar el mapa de calor
    HeatMap(heat_data).add_to(mapa_base)

    # Mostrar el mapa en Streamlit
    st.write("Mapa de Calor de Madera Movilizada en Colombia")
    folium_static(mapa_base)

# Cargar datos
gdf = cargar_y_relacionar_datos()
mapa_colombia = cargar_mapa_colombia()

if gdf is not None:
    st.write("Datos cargados con éxito")

    # Generar el mapa de calor
    generar_mapa_calor(gdf, mapa_colombia)
