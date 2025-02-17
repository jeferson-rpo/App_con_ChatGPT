import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from unidecode import unidecode

def cargar_datos_madera():
    """
    Carga los datos de madera movilizada desde el CSV.

    Returns:
        pd.DataFrame: DataFrame con los datos de madera movilizada.
    """
    url = "https://raw.githubusercontent.com/jeferson-rpo/App_con_ChatGPT/refs/heads/main/madera_movilizada.csv"
    df_madera = pd.read_csv(url)

    # Eliminar tildes y convertir a minúsculas
    df_madera['DPTO'] = df_madera['DPTO'].str.lower().apply(unidecode)
    df_madera['MUNICIPIO'] = df_madera['MUNICIPIO'].str.lower().apply(unidecode)
    df_madera['ESPECIE'] = df_madera['ESPECIE'].str.lower().apply(unidecode)

    return df_madera

def cargar_datos_municipios():
    """
    Carga los datos de municipios y sus coordenadas desde el CSV.

    Returns:
        pd.DataFrame: DataFrame con los datos de municipios.
    """
    url = "https://raw.githubusercontent.com/jeferson-rpo/App_con_ChatGPT/refs/heads/main/DIVIPOLA-_C_digos_municipios_geolocalizados_20250217.csv"
    df_municipios = pd.read_csv(url)

    # Eliminar tildes y convertir a minúsculas
    df_municipios['NOM_MPIO'] = df_municipios['NOM_MPIO'].str.lower().apply(unidecode)

    return df_municipios

def cargar_mapa_colombia():
    """
    Carga el mapa de los países desde la URL y filtra solo Colombia.

    Returns:
        gpd.GeoDataFrame: Mapa de Colombia.
    """
    # Cargar los datos del mapa de países
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    mundo = gpd.read_file(ruta_0)

    # Filtrar solo Colombia
    colombia = mundo[mundo['NAME'] == 'Colombia']
    return colombia

def cargar_y_relacionar_datos():
    """
    Carga y relaciona los datos de madera movilizada con los datos de municipios.
    
    Returns:
        pd.DataFrame: DataFrame con los datos de madera movilizada relacionados con los municipios.
    """
    # Cargar los datos
    df_madera = cargar_datos_madera()
    df_municipios = cargar_datos_municipios()

    # Realizar el merge para agregar las coordenadas
    df_madera['MUNICIPIO'] = df_madera['MUNICIPIO'].apply(unidecode)
    df_municipios['NOM_MPIO'] = df_municipios['NOM_MPIO'].apply(unidecode)

    df_relacionado = df_madera.merge(df_municipios[['NOM_MPIO', 'LATITUD', 'LONGITUD']], how="left", left_on="MUNICIPIO", right_on="NOM_MPIO")
    df_relacionado = df_relacionado.drop(columns=['NOM_MPIO'])

    return df_relacionado

def graficar_top_10_especies(especies_pais):
    """
    Genera un gráfico de barras con las 10 especies de madera con mayor volumen movilizado.
    Cada barra tendrá un color diferente.

    Args:
        especies_pais (pd.DataFrame): DataFrame con las especies y su volumen total.
    """
    # Seleccionar las 10 especies con mayor volumen
    top_10_especies = especies_pais.head(10)

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

def graficar_mapa_calor(df, mapa_colombia):
    """
    Genera un mapa de calor mostrando la distribución de volúmenes de madera movilizada por departamento en Colombia.
    
    Args:
        df (pd.DataFrame): DataFrame con los volúmenes de madera movilizada por departamento.
        mapa_colombia (gpd.GeoDataFrame): Mapa de Colombia para la visualización.
    """
    # Unir los datos de madera movilizada con el mapa de Colombia
    df_departamento = df.groupby('DPTO')['VOLUMEN M3'].sum().reset_index()

    # Normalizar los nombres de los departamentos para evitar problemas con acentos
    df_departamento['DPTO'] = df_departamento['DPTO'].str.lower().apply(unidecode)

    # Asegurarse de que los departamentos del mapa coincidan con los del DataFrame
    mapa_colombia = mapa_colombia.set_index('NAME')
    mapa_colombia = mapa_colombia[mapa_colombia.index == 'Colombia']

    # Unir los datos de volumen con el mapa de Colombia
    mapa_colombia = mapa_colombia.merge(df_departamento, how='left', left_on='NAME', right_on='DPTO')

    # Crear el mapa de calor
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    mapa_colombia.plot(column='VOLUMEN M3', ax=ax, legend=True,
                       legend_kwds={'label': "Volumen de Madera Movilizada por Departamento",
                                    'orientation': "horizontal"})
    ax.set_title('Distribución de Volúmenes de Madera por Departamento en Colombia')
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
    
    # Gráfico de barras: Top 10 especies con mayor volumen
    st.markdown("---")
    st.markdown("## Gráfico Top 10 Especies con Mayor Volumen Movilizado")
    st.markdown("---")

    # Llamar a la función para graficar
    graficar_top_10_especies(especies_pais)

    # Seleccionar un departamento para el análisis
    depto_seleccionado = st.selectbox("Selecciona un departamento", gdf['DPTO'].unique())

    # Filtrar datos por departamento seleccionado
    especies_depto = gdf[gdf['DPTO'] == depto_seleccionado]
    especies_depto = especies_depto.groupby('ESPECIE')['VOLUMEN M3'].sum().reset_index()
    especies_depto = especies_depto.sort_values(by='VOLUMEN M3', ascending=False)

    st.subheader(f"Especies de madera más comunes en {depto_seleccionado}")
    st.write(especies_depto)

def analizar_madera_movilizada():
    """
    Realiza el análisis de los volúmenes de madera movilizada por departamento y genera el mapa de calor.
    """
    # Cargar los datos de madera movilizada
    gdf = cargar_y_relacionar_datos()

    if gdf is not None:
        st.write("Datos cargados:", gdf)
        
        # Filtrar solo los datos correspondientes a Colombia
        mapa_colombia = cargar_mapa_colombia()

        # Graficar el mapa de calor de volúmenes de madera
        graficar_mapa_calor(gdf, mapa_colombia)

st.title("Análisis de Madera Movilizada en Colombia")

# Realizar el análisis de madera movilizada
analizar_madera_movilizada()
