import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import Normalize

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

def generar_mapa_calor(gdf):
    """
    Genera un mapa de calor que muestra la distribución de volúmenes de madera por departamento.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Agrupar los datos por departamento y sumar el volumen
    volumen_por_depto = gdf.groupby('DPTO')['VOLUMEN M3'].sum().reset_index()

    # Cargar el archivo GeoJSON de países y filtrar solo Colombia
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    mundo_dataframe = gpd.read_file(ruta_0)
    colombia_dataframe = mundo_dataframe[mundo_dataframe['NAME'] == 'Colombia']

    # Unir los datos de volumen con el GeoDataFrame de Colombia
    # Nota: Asegúrate de que los nombres de los departamentos coincidan con los del GeoJSON.
    colombia_dataframe = colombia_dataframe.merge(volumen_por_depto, left_on='NAME', right_on='DPTO', how='left')

    # Crear el mapa de calor
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    colombia_dataframe.plot(column='VOLUMEN M3', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True,
                            missing_kwds={"color": "lightgrey", "label": "Sin datos"})
    plt.title('Distribución de Volúmenes de Madera por Departamento en Colombia')
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

    # Gráfico de barras: Top 10 especies con mayor volumen
    st.markdown("---")
    st.markdown("## Gráfico de Barras: Top 10 Especies con Mayor Volumen Movilizado")
    st.markdown("---")
    graficar_top_10_especies(especies_pais)

    # Mapa de calor: Distribución de volúmenes por departamento en Colombia
    st.markdown("---")
    st.markdown("## Mapa de Calor: Distribución de Volúmenes por Departamento en Colombia")
    st.markdown("---")
    generar_mapa_calor(gdf)

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
