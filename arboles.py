import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from unidecode import unidecode

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

st.title("Análisis de Distribución de Madera Movilizada en Colombia")

# Realizar el análisis de madera movilizada
analizar_madera_movilizada()

