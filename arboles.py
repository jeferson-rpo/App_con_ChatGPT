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

def graficar_top_10_especies(especies_depto):
    """
    Genera un gráfico de barras con las 10 especies de madera con mayor volumen movilizado.
    Cada barra tendrá un color diferente.

    Args:
        especies_depto (pd.DataFrame): DataFrame con las especies y su volumen total por departamento.
    """
    # Seleccionar las 10 especies con mayor volumen
    top_10_especies = especies_depto.head(10)

    # Crear una lista de colores para las barras
    colores = plt.cm.tab10.colors  # Usar la paleta de colores 'tab10'

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    barras = plt.bar(top_10_especies['ESPECIE'], top_10_especies['VOLUMEN M3'], color=colores)
    plt.xlabel('Especie')
    plt.ylabel('Volumen Movilizado (M3)')
    plt.title('Top 10 Especies con Mayor Volumen Movilizado')
    plt.xticks(rotation=45, ha='right')  # Rotar etiquetas para mejor visualización
    plt.tight_layout()  # Ajustar layout para que no se corten las etiquetas

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

def analizar_especies_antioquia(gdf):
    """
    Realiza el análisis de las especies más comunes en Antioquia, incluyendo los municipios y sus coordenadas.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Filtro por Antioquia
    gdf_antioquia = gdf[gdf['DPTO'] == 'Antioquia']

    # Análisis de especies más comunes en Antioquia
    especies_antioquia = gdf_antioquia.groupby('ESPECIE')['VOLUMEN M3'].sum().reset_index()
    especies_antioquia = especies_antioquia.sort_values(by='VOLUMEN M3', ascending=False)
    
    st.subheader("Especies de madera más comunes en Antioquia")
    st.write(especies_antioquia)
    
    # Gráfico de barras: Top 10 especies con mayor volumen
    st.markdown("---")
    st.markdown("## Gráfico Top 10 Especies con Mayor Volumen Movilizado en Antioquia")
    st.markdown("---")
    
    # Llamar a la función para graficar
    graficar_top_10_especies(especies_antioquia)

    # Mostrar los municipios y sus coordenadas asociadas en Antioquia
    st.markdown("### Municipios de Antioquia con sus Coordenadas")
    municipios_antioquia = gdf_antioquia[['MUNICIPIO', 'LATITUD', 'LONGITUD']].drop_duplicates()
    st.write(municipios_antioquia)

    # Opción de mostrar la posición de los municipios en el mapa (si lo deseas)
    st.markdown("#### Mapa de Municipios de Antioquia")
    mapa = folium.Map(location=[municipios_antioquia['LATITUD'].mean(), municipios_antioquia['LONGITUD'].mean()], zoom_start=8)

    for _, row in municipios_antioquia.iterrows():
        folium.Marker([row['LATITUD'], row['LONGITUD']], popup=row['MUNICIPIO']).add_to(mapa)

    st.map(mapa)

st.title("Análisis de Madera Movilizada en Antioquia")

# Cargar datos
gdf = cargar_y_relacionar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Realizar el análisis para Antioquia
    analizar_especies_antioquia(gdf)

