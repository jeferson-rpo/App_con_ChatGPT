import streamlit as st
import pandas as pd
import geopandas as gpd
import requests
import zipfile
import io
import matplotlib.pyplot as plt

# Cargar el archivo CSV de madera movilizada
def cargar_datos_madera():
    """
    Carga el archivo CSV con los datos de madera movilizada.
    """
    # URL o archivo local con los datos
    archivo_madera = st.file_uploader("Sube tu archivo CSV de madera movilizada", type=["csv"])
    if archivo_madera:
        return pd.read_csv(archivo_madera)
    return None

# Cargar y filtrar el mapa de Colombia
def cargar_mapa_colombia():
    """
    Carga y filtra el mapa de Colombia desde el archivo proporcionado.
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

# Generar el mapa de calor usando GeoPandas
def generar_mapa_calor(gdf_madera, mapa_colombia):
    """
    Genera un mapa de calor utilizando las coordenadas de los municipios y el volumen de madera movilizada.
    
    Args:
        gdf_madera (GeoDataFrame): Datos de madera movilizada con coordenadas y volúmenes.
        mapa_colombia (GeoDataFrame): Mapa de Colombia.
    """
    # Crear un GeoDataFrame con las coordenadas de los municipios y el volumen
    gdf_madera = gpd.GeoDataFrame(
        gdf_madera, 
        geometry=gpd.points_from_xy(gdf_madera['LONGITUD'], gdf_madera['LATITUD']),
        crs="EPSG:4326"
    )
    
    # Establecer el CRS de Colombia y el de los municipios a uno común
    gdf_madera = gdf_madera.to_crs(mapa_colombia.crs)

    # Crear la figura y los ejes
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    # Dibujar el mapa de Colombia
    mapa_colombia.plot(ax=ax, color='lightblue', edgecolor='black')

    # Graficar los puntos de los municipios con el volumen como color
    gdf_madera.plot(ax=ax, marker='o', color=gdf_madera['VOLUMEN M3'], cmap='YlGnBu', markersize=50, legend=True)

    # Añadir título y etiquetas
    ax.set_title('Distribución de Volúmenes de Madera Movilizada por Municipio', fontsize=14)
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')

    # Mostrar el mapa
    st.pyplot(fig)

# Cargar datos
gdf_madera = cargar_datos_madera()

# Cargar el mapa de Colombia
mapa_colombia = cargar_mapa_colombia()

if gdf_madera is not None:
    # Generar el mapa de calor
    generar_mapa_calor(gdf_madera, mapa_colombia)
