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
    Carga un dataset con las coordenadas de los municipios de Colombia desde la URL proporcionada.

    Returns:
        pd.DataFrame: DataFrame con las coordenadas de los municipios.
    """
    try:
        # URL proporcionada con los datos de municipios
        url_municipios = "https://raw.githubusercontent.com/jeferson-rpo/App_con_ChatGPT/refs/heads/main/DIVIPOLA-_C_digos_municipios_geolocalizados_20250217.csv"
        df_municipios = pd.read_csv(url_municipios)

        # Normalizar los nombres de los municipios (quitar tildes y convertir a minúsculas)
        df_municipios['NOM_MPIO'] = df_municipios['NOM_MPIO'].str.lower().apply(unidecode)
        
        # Seleccionar solo las columnas necesarias
        df_municipios = df_municipios[['NOM_MPIO', 'LATITUD', 'LONGITUD']]
        
        return df_municipios
    except Exception as e:
        st.error(f"Error al cargar las coordenadas: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

def agregar_coordenadas_al_dataset(gdf):
    """
    Agrega las coordenadas de los municipios al dataset de madera movilizada.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.

    Returns:
        pd.DataFrame: DataFrame con las coordenadas agregadas.
    """
    # Cargar coordenadas de los municipios
    coordenadas = cargar_coordenadas_municipios()

    # Normalizar los nombres de los municipios en el dataset de madera
    gdf['MUNICIPIO'] = gdf['MUNICIPIO'].str.lower().apply(unidecode)

    # Unir los datos de volúmenes con las coordenadas de los municipios
    gdf_con_coordenadas = gdf.merge(coordenadas, how="left", left_on="MUNICIPIO", right_on="NOM_MPIO").drop(columns=["NOM_MPIO"])

    return gdf_con_coordenadas

def generar_mapa_municipios(gdf):
    """
    Genera un mapa que muestra la ubicación de los municipios con sus volúmenes de madera.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada y coordenadas.
    """
    # Crear un GeoDataFrame con las coordenadas de los municipios
    gdf = gpd.GeoDataFrame(
        gdf, geometry=gpd.points_from_xy(gdf.LONGITUD, gdf.LATITUD)
    )

    # Cargar un archivo GeoJSON con los límites de Colombia
    url_geojson_colombia = "https://raw.githubusercontent.com/CodeForSocialGood/colombia-geojson/master/colombia.geojson"
    colombia = gpd.read_file(url_geojson_colombia)

    # Crear el mapa
    fig, ax = plt.subplots(figsize=(10, 8))
    colombia.plot(ax=ax, color='lightgrey')  # Fondo de Colombia
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

    # Agregar coordenadas al dataset
    gdf_con_coordenadas = agregar_coordenadas_al_dataset(gdf)

    # Mostrar el mapa de municipios con volúmenes
    st.markdown("---")
    st.markdown("## Mapa de Volúmenes de Madera por Municipio")
    st.markdown("---")
    generar_mapa_municipios(gdf_con_coordenadas)

    # Seleccionar un departamento para el análisis
    depto_seleccionado = st.selectbox("Selecciona un departamento", gdf['DPTO'].unique())

    # Filtrar datos por departamento seleccionado
    especies_depto = gdf[gdf['DPTO'] == depto_seleccionado]
    especies_depto = especies_depto.groupby(['ESPECIE', 'MUNICIPIO', 'LATITUD', 'LONGITUD'])['VOLUMEN M3'].sum().reset_index()
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
