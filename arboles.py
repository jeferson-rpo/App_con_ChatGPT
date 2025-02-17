import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

st.title("Análisis de Madera Movilizada")

# Cargar datos
gdf = cargar_y_relacionar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Realizar el análisis automáticamente
    analizar_especies(gdf)
