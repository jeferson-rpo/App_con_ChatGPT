import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from unidecode import unidecode
import folium

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
    
    return df_relacionado

def mostrar_datos_antioquia(gdf):
    """
    Filtra los datos por Antioquia y muestra los datos relevantes: municipio, latitud, longitud y volumen.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Filtrar los datos por departamento (Antioquia)
    gdf_antioquia = gdf[gdf['DPTO'] == 'Antioquia']

    # Mostrar los datos relevantes: municipio, latitud, longitud y volumen
    st.subheader("Datos de Madera Movilizada en Antioquia")
    st.write(gdf_antioquia[['MUNICIPIO', 'LATITUD', 'LONGITUD', 'VOLUMEN M3']])

    # Opción de mostrar la posición de los municipios en el mapa
    st.markdown("### Mapa de Municipios de Antioquia con sus Coordenadas")
    mapa = folium.Map(location=[gdf_antioquia['LATITUD'].mean(), gdf_antioquia['LONGITUD'].mean()], zoom_start=8)

    for _, row in gdf_antioquia.iterrows():
        folium.Marker([row['LATITUD'], row['LONGITUD']], popup=f"{row['MUNICIPIO']} - Volumen: {row['VOLUMEN M3']}").add_to(mapa)

    st.map(mapa)

st.title("Análisis de Madera Movilizada en Antioquia")

# Cargar datos
gdf = cargar_y_relacionar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Mostrar los datos filtrados para Antioquia
    mostrar_datos_antioquia(gdf)
