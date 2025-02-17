import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import zipfile
import io
import requests
from unidecode import unidecode

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
    Carga el archivo de municipios directamente desde la URL proporcionada.

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

def cargar_y_relacionar_datos():
    """
    Carga los datos de madera movilizada y los relaciona con los municipios.
    
    Returns:
        pd.DataFrame: DataFrame con los datos relacionados.
    """
    # Cargar el archivo de madera movilizada desde la URL o mediante carga manual
    df_madera = cargar_datos()
    
    # Cargar los datos de los municipios desde la URL
    df_municipios = cargar_datos_municipios()

    # Normalizar los nombres de los municipios (quitar tildes y convertir a minúsculas) en df_madera usando vectorización
    df_madera['MUNICIPIO'] = df_madera['MUNICIPIO'].str.lower().apply(unidecode)

    # Relacionar los datos de madera movilizada con los municipios sin duplicar columnas
    df_relacionado = df_madera.merge(df_municipios, how="left", left_on="MUNICIPIO", right_on="NOM_MPIO").drop(columns=["NOM_MPIO"])

    # Interpolación de los valores NaN en las columnas relevantes
    df_relacionado[['LATITUD', 'LONGITUD', 'VOLUMEN M3']] = df_relacionado[['LATITUD', 'LONGITUD', 'VOLUMEN M3']].interpolate(method='linear', axis=0)

    # Convertir a GeoDataFrame para usar geometría
    gdf = gpd.GeoDataFrame(df_relacionado, geometry=gpd.points_from_xy(df_relacionado['LONGITUD'], df_relacionado['LATITUD']))
    
    return gdf

def cargar_mapa_mundial():
    """
    Carga el archivo de mapa mundial de países desde la URL proporcionada.
    
    Returns:
        GeoDataFrame: GeoDataFrame con los límites de los países.
    """
    # Cargar el archivo zip desde la URL
    url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall("mapa")
    
    # Cargar el shapefile del mapa de países
    mapa = gpd.read_file("mapa/ne_50m_admin_0_countries.shp")
    
    return mapa

def generar_mapa_calor(gdf, mapa):
    """
    Genera un mapa de calor que muestra la distribución de volúmenes de madera por departamento.
    
    Args:
        gdf (GeoDataFrame): GeoDataFrame con los datos de madera movilizada.
        mapa (GeoDataFrame): GeoDataFrame con los límites de los países.
    """
    # Crear el mapa base centrado en el centro geográfico del mapa mundial
    mapa_base = folium.Map(location=[0, 0], zoom_start=2)
    
    # Agregar el mapa de países de fondo
    folium.GeoJson(mapa).add_to(mapa_base)
    
    # Preparar los datos para el mapa de calor: cada punto será un municipio con su volumen
    puntos = gdf[['LATITUD', 'LONGITUD', 'VOLUMEN M3']].values

    # Crear el mapa de calor
    heat_data = [[point[0], point[1], point[2]] for point in puntos]
    HeatMap(heat_data).add_to(mapa_base)

    # Mostrar el mapa en Streamlit
    st.write("### Mapa de Calor de Volúmenes de Madera por Departamento")
    st.components.v1.html(mapa_base._repr_html_(), height=600)

# Cargar datos
gdf = cargar_y_relacionar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Cargar el mapa de países
    mapa_mundial = cargar_mapa_mundial()

    # Llamar a la función de generación de mapa de calor
    generar_mapa_calor(gdf, mapa_mundial)
