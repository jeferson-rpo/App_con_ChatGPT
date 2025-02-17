import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

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

    return None

def cargar_coordenadas_municipios():
    """
    Carga un dataset con las coordenadas de los municipios de Colombia.

    Returns:
        pd.DataFrame: DataFrame con las coordenadas de los municipios.
    """
    # Cargar un dataset con las coordenadas de los municipios de Colombia
    # Este es un ejemplo, puedes reemplazarlo con tu propio dataset
    coordenadas_url = "https://raw.githubusercontent.com/jdvelasq/datalabs/master/datasets/divipola/municipios.csv"
    coordenadas = pd.read_csv(coordenadas_url, sep=";")

    # Seleccionar columnas relevantes (nombre del municipio, latitud, longitud)
    coordenadas = coordenadas[['municipio', 'latitud', 'longitud']]
    coordenadas.rename(columns={'municipio': 'MUNICIPIO'}, inplace=True)

    return coordenadas

def generar_mapa_municipios(gdf):
    """
    Genera un mapa que muestra la ubicación de los municipios con sus volúmenes de madera.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada y coordenadas.
    """
    # Crear un GeoDataFrame con las coordenadas de los municipios
    gdf = gpd.GeoDataFrame(
        gdf, geometry=gpd.points_from_xy(gdf.longitud, gdf.latitud)
    
    # Crear el mapa
    fig, ax = plt.subplots(figsize=(10, 8))
    mundo = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    mundo[mundo.name == "Colombia"].plot(ax=ax, color='lightgrey')  # Fondo de Colombia
    gdf.plot(column='VOLUMEN M3', cmap='OrRd', markersize=50, ax=ax, legend=True,
             legend_kwds={'label': "Volumen de Madera (M3)"})
    plt.title('Volumen de Madera Movilizada por Municipio en Colombia')
    plt.axis('off')  # Ocultar ejes

    # Mostrar el mapa en Streamlit
    st.pyplot(fig)

def analizar_especies(gdf):
    """
    Realiza el análisis de las especies más comunes a nivel país y por departamento.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Título grande para el análisis
    st.markdown("---")
    st.markdown("## Análisis de Especies de Madera Movilizada")
    st.markdown("---")

    # Análisis de especies más comunes a nivel país
    especies_pais = gdf.groupby('ESPECIE')['VOLUMEN M3'].sum().reset_index()
    especies_pais = especies_pais.sort_values(by='VOLUMEN M3', ascending=False)

    st.subheader("Especies de madera más comunes a nivel país")
    st.write(especies_pais)

    # Cargar coordenadas de los municipios
    coordenadas = cargar_coordenadas_municipios()

    # Unir los datos de volúmenes con las coordenadas de los municipios
    gdf_con_coordenadas = gdf.merge(coordenadas, on='MUNICIPIO', how='left')

    # Mostrar el mapa de municipios con volúmenes
    st.markdown("---")
    st.markdown("## Mapa de Volúmenes de Madera por Municipio")
    st.markdown("---")
    generar_mapa_municipios(gdf_con_coordenadas)

    # Seleccionar un departamento para el análisis
    depto_seleccionado = st.selectbox("Selecciona un departamento", gdf['DPTO'].unique())

    # Filtrar datos por departamento seleccionado
    especies_depto = gdf[gdf['DPTO'] == depto_seleccionado]
    especies_depto = especies_depto.groupby('ESPECIE')['VOLUMEN M3'].sum().reset_index()
    especies_depto = especies_depto.sort_values(by='VOLUMEN M3', ascending=False)

    st.subheader(f"Especies de madera más comunes en {depto_seleccionado}")
    st.write(especies_depto)

st.title("Análisis de Madera Movilizada")

# Cargar datos
gdf = cargar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Realizar el análisis automáticamente
    analizar_especies(gdf)
