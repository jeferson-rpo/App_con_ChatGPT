import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from unidecode import unidecode

# Cargar los datos de madera movilizada y municipios
def cargar_datos_madera():
    """
    Permite al usuario cargar un archivo CSV con los datos de madera movilizada.
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
    df_madera = cargar_datos_madera()
    
    # Cargar los datos de los municipios desde la URL
    df_municipios = cargar_datos_municipios()

    # Normalizar los nombres de los municipios (quitar tildes y convertir a minúsculas) en df_madera usando vectorización
    df_madera['MUNICIPIO'] = df_madera['MUNICIPIO'].str.lower().apply(unidecode)

    # Relacionar los datos de madera movilizada con los municipios sin duplicar columnas
    df_relacionado = df_madera.merge(df_municipios, how="left", left_on="MUNICIPIO", right_on="NOM_MPIO").drop(columns=["NOM_MPIO"])
    
    return df_relacionado

def generar_mapa_calor(gdf):
    """
    Genera un mapa de calor de los municipios según el volumen de madera movilizada.
    
    Args:
        gdf (GeoDataFrame): DataFrame con los datos relacionados y coordenadas geográficas.
    """
    # Cargar el mapa de Colombia
    url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    colombia = gpd.read_file(url)
    colombia = colombia[colombia['NAME'] == 'Colombia']

    # Crear un GeoDataFrame con las coordenadas de los municipios y el volumen
    gdf_madera = gpd.GeoDataFrame(
        gdf, 
        geometry=gpd.points_from_xy(gdf['LONGITUD'], gdf['LATITUD']),
        crs="EPSG:4326"
    )

    # Establecer el CRS de Colombia y el de los municipios a uno común
    gdf_madera = gdf_madera.to_crs(colombia.crs)

    # Crear la figura y los ejes
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))

    # Dibujar el mapa de Colombia
    colombia.plot(ax=ax, color='lightgray', edgecolor='black')

    # Graficar los puntos de los municipios con el volumen como color
    gdf_madera.plot(ax=ax, marker='o', color=gdf_madera['VOLUMEN M3'], cmap='YlOrRd', markersize=50, legend=True)

    # Añadir título y etiquetas
    ax.set_title('Mapa de Calor: Volumen de Madera Movilizada por Municipio', fontsize=16)
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')

    # Mostrar el mapa
    st.pyplot(fig)

# Cargar y procesar los datos
gdf = cargar_y_relacionar_datos()

# Generar el mapa de calor si los datos fueron cargados correctamente
if gdf is not None:
    generar_mapa_calor(gdf)

