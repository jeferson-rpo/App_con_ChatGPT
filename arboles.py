import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
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

def graficar_mapa_de_calor_colombia(gdf):
    """
    Muestra el mapa de calor de los volúmenes movilizados sobre el mapa de Colombia.
    
    Los puntos en el mapa tienen colores y tamaños ajustados según el volumen movilizado (VOLUMEN M3).
    
    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada con geolocalización.
    """
    # Cargar el archivo GeoJSON de países y filtrar solo Colombia
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    mundo_dataframe = gpd.read_file(ruta_0)
    colombia_dataframe = mundo_dataframe[mundo_dataframe['NAME'] == 'Colombia']

    # Crear un GeoDataFrame a partir de los datos de madera movilizada
    gdf['geometry'] = gpd.points_from_xy(gdf['LONGITUD'], gdf['LATITUD'])
    gdf = gpd.GeoDataFrame(gdf, geometry='geometry')

    # Asegurarse de que los valores de VOLUMEN M3 sean numéricos y manejar valores no numéricos
    gdf['VOLUMEN M3'] = pd.to_numeric(gdf['VOLUMEN M3'], errors='coerce')  # Convertir a numérico, valores no válidos se convierten en NaN
    gdf = gdf.dropna(subset=['VOLUMEN M3'])  # Eliminar filas con NaN en la columna 'VOLUMEN M3'

    # Crear un gráfico del mapa de Colombia
    fig, ax = plt.subplots(figsize=(10, 10))
    colombia_dataframe.plot(ax=ax, color='lightgray')

    # Superponer el mapa de calor con los puntos de los municipios
    gdf.plot(ax=ax, marker='o', column='VOLUMEN M3', cmap='YlOrRd', markersize=gdf['VOLUMEN M3'] / 100, alpha=0.5, legend=True)

    # Añadir título y mostrar el mapa
    ax.set_title('Mapa de Calor de Madera Movilizada en Colombia', fontsize=15)
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
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

    # Gráfico de barras: Top 10 especies con mayor volumen
    st.markdown("---")
    st.markdown("## Gráfico Top 10 Especies con Mayor Volumen Movilizado")
    st.markdown("---")
    graficar_top_10_especies(especies_pais)

    # Seleccionar un departamento para el análisis
    depto_seleccionado = st.selectbox("Selecciona un departamento", gdf['DPTO'].unique())

    # Filtrar datos por departamento seleccionado
    especies_depto = gdf[gdf['DPTO'] == depto_seleccionado]
    especies_depto = especies_depto.groupby(['ESPECIE', 'MUNICIPIO', 'LATITUD', 'LONGITUD'])['VOLUMEN M3'].sum().reset_index()
    especies_depto = especies_depto.sort_values(by='VOLUMEN M3', ascending=False)

    st.subheader(f"Especies de madera más comunes en {depto_seleccionado}")
    st.write(especies_depto)

    # Mostrar el mapa de calor de madera movilizada en el departamento seleccionado
    st.markdown("---")
    st.markdown(f"## Mapa de Calor de Madera Movilizada en {depto_seleccionado}")
    st.markdown("---")
    graficar_mapa_de_calor_colombia(especies_depto)

def graficar_mapa_de_calor_top_10_municipios(gdf):
    """
    Muestra el mapa de calor de los 10 municipios con mayor volumen movilizado,
    sobre el mapa de Colombia.

    Los puntos en el mapa tienen colores y tamaños ajustados según el volumen movilizado (VOLUMEN M3).

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada con geolocalización.
    """
    
    # Título antes de mostrar el mapa
    st.markdown("---")
    st.markdown("## Mapa de Calor de Madera Movilizada en Colombia")
    st.markdown("---")
    # Asegurarse de que los valores de VOLUMEN M3 sean numéricos y manejar valores no numéricos
    gdf['VOLUMEN M3'] = pd.to_numeric(gdf['VOLUMEN M3'], errors='coerce')  # Convertir a numérico, valores no válidos se convierten en NaN
    gdf = gdf.dropna(subset=['VOLUMEN M3'])  # Eliminar filas con NaN en la columna 'VOLUMEN M3'

    # Agrupar los datos por municipio y sumar el volumen de madera movilizada
    top_10_municipios = gdf.groupby('MUNICIPIO')['VOLUMEN M3'].sum().reset_index()

    # Ordenar por el volumen y seleccionar los 10 municipios con mayor volumen
    top_10_municipios = top_10_municipios.sort_values(by='VOLUMEN M3', ascending=False).head(10)

    # Filtrar gdf para incluir solo los datos de los 10 municipios seleccionados
    gdf_top_10 = gdf[gdf['MUNICIPIO'].isin(top_10_municipios['MUNICIPIO'])]

    # Cargar el archivo GeoJSON de países y filtrar solo Colombia
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    mundo_dataframe = gpd.read_file(ruta_0)
    colombia_dataframe = mundo_dataframe[mundo_dataframe['NAME'] == 'Colombia']

    # Crear un GeoDataFrame a partir de los datos de madera movilizada
    gdf_top_10['geometry'] = gpd.points_from_xy(gdf_top_10['LONGITUD'], gdf_top_10['LATITUD'])
    gdf_top_10 = gpd.GeoDataFrame(gdf_top_10, geometry='geometry')

    # Crear un gráfico del mapa de Colombia
    fig, ax = plt.subplots(figsize=(10, 10))
    colombia_dataframe.plot(ax=ax, color='lightgray')

    # Superponer el mapa de calor con los puntos de los 10 municipios seleccionados
    gdf_top_10.plot(ax=ax, marker='o', column='VOLUMEN M3', cmap='YlOrRd', markersize=gdf_top_10['VOLUMEN M3'] / 100, alpha=0.7, legend=True)

    # Añadir título y mostrar el mapa
    ax.set_title('Mapa de Calor de los 10 Municipios con Mayor Volumen Movilizado', fontsize=15)
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

def analizar_evolucion_temporal(gdf):
    """
    Analiza la evolución temporal del volumen de madera movilizada por especie y tipo de producto.
    
    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Título para la sección
    st.markdown("---")
    st.markdown("## Análisis de la Evolución Temporal del Volumen de Madera Movilizada")
    st.markdown("---")

    # Agrupar los datos por AÑO, ESPECIE, TIPO PRODUCTO y VOLUMEN M3
    df_evolucion = gdf.groupby(['AÑO', 'ESPECIE', 'TIPO PRODUCTO'])['VOLUMEN M3'].sum().reset_index()

    # Filtrar una especie y tipo de producto para graficar (esto se puede modificar según preferencia)
    especie_seleccionada = st.selectbox("Selecciona una especie", df_evolucion['ESPECIE'].unique())
    tipo_producto_seleccionado = st.selectbox("Selecciona un tipo de producto", df_evolucion['TIPO PRODUCTO'].unique())

    # Filtrar los datos seleccionados
    df_filtrado = df_evolucion[(df_evolucion['ESPECIE'] == especie_seleccionada) & 
                               (df_evolucion['TIPO PRODUCTO'] == tipo_producto_seleccionado)]

    # Gráfico de evolución temporal
    plt.figure(figsize=(10, 6))
    plt.plot(df_filtrado['AÑO'], df_filtrado['VOLUMEN M3'], marker='o', color='b', linestyle='-', markersize=6)
    plt.xlabel('Año')
    plt.ylabel('Volumen Movilizado (M3)')
    plt.title(f'Evolución Temporal del Volumen de Madera Movilizada: {especie_seleccionada} ({tipo_producto_seleccionado})')
    plt.grid(True)
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

def analizar_outliers(gdf):
    """
    Realiza un análisis estadístico para identificar outliers en los volúmenes de madera movilizada.
    
    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Título para la sección
    st.markdown("---")
    st.markdown("## Análisis Estadístico de Outliers en el Volumen de Madera Movilizada")
    st.markdown("---")

    # Calcular los cuartiles (Q1, Q3) y el IQR (Rango Intercuartílico)
    Q1 = gdf['VOLUMEN M3'].quantile(0.25)
    Q3 = gdf['VOLUMEN M3'].quantile(0.75)
    IQR = Q3 - Q1

    # Calcular los límites para los outliers
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    # Filtrar los outliers
    outliers = gdf[(gdf['VOLUMEN M3'] < limite_inferior) | (gdf['VOLUMEN M3'] > limite_superior)]

    # Mostrar estadísticas y los outliers detectados
    st.write("Rango Intercuartílico (IQR):", IQR)
    st.write(f"Límite inferior: {limite_inferior}")
    st.write(f"Límite superior: {limite_superior}")
    
    st.write(f"Se han detectado {outliers.shape[0]} outliers en los datos.")
    
    # Mostrar los outliers en una tabla
    st.write("Outliers detectados:", outliers)

    # Mostrar un gráfico de caja (boxplot) para visualizar los outliers
    plt.figure(figsize=(10, 6))
    plt.boxplot(gdf['VOLUMEN M3'], vert=False)
    plt.xlabel('Volumen Movilizado (M3)')
    plt.title('Gráfico de Caja para Identificar Outliers en Volúmenes de Madera Movilizada')
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

def agrupar_por_municipio(gdf):
    """
    Agrupa los datos por municipio y calcula el volumen total de madera movilizada en cada uno.
    
    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Título para la sección
    st.markdown("---")
    st.markdown("## Volumen Total de Madera Movilizada por Municipio")
    st.markdown("---")

    # Agrupar los datos por municipio y calcular el volumen total de madera movilizada
    volumen_por_municipio = gdf.groupby('MUNICIPIO')['VOLUMEN M3'].sum().reset_index()

    # Ordenar por el volumen total de mayor a menor
    volumen_por_municipio = volumen_por_municipio.sort_values(by='VOLUMEN M3', ascending=False)

    # Mostrar la tabla con el volumen total por municipio
    st.write(volumen_por_municipio)
import folium
from folium.plugins import MarkerCluster

def analizar_especies_con_menor_volumen(gdf):
    """
    Identifica las especies de madera con menor volumen movilizado y analiza su distribución geográfica.
    
    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Título para la sección
    st.markdown("---")
    st.markdown("## Especies con Menor Volumen Movilizado y su Distribución Geográfica")
    st.markdown("---")

    # Agrupar por especie y calcular el volumen total de madera movilizada
    especies_volumen = gdf.groupby('ESPECIE')['VOLUMEN M3'].sum().reset_index()

    # Ordenar por volumen de menor a mayor
    especies_volumen = especies_volumen.sort_values(by='VOLUMEN M3', ascending=True)

    # Seleccionar las 10 especies con menor volumen movilizado
    especies_menor_volumen = especies_volumen.head(10)

    # Mostrar la tabla con las especies, su volumen y la posición en el ranking
    st.write("### Ranking de Especies con Menor Volumen Movilizado")
    especies_menor_volumen['Posición'] = range(1, len(especies_menor_volumen) + 1)
    st.write(especies_menor_volumen[['Posición', 'ESPECIE', 'VOLUMEN M3']])

    # Filtrar los datos de gdf para incluir solo las especies con menor volumen
    gdf_menor_volumen = gdf[gdf['ESPECIE'].isin(especies_menor_volumen['ESPECIE'])]

    # Crear el mapa de Folium centrado en un punto medio de Colombia
    mapa = folium.Map(location=[4.7110, -74.0721], zoom_start=6)

    # Agrupar por especie y calcular el volumen total de madera movilizada
    marker_cluster = MarkerCluster().add_to(mapa)

    # Agregar marcadores por cada fila de gdf_menor_volumen
    for idx, row in gdf_menor_volumen.iterrows():
        folium.Marker(
            location=[row['LATITUD'], row['LONGITUD']],
            popup=f"Especie: {row['ESPECIE']}<br>Volumen: {row['VOLUMEN M3']} m3",
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)

    # Mostrar el mapa
    st.write("### Distribución Geográfica de las Especies con Menor Volumen Movilizado")
    st.markdown("El mapa muestra la distribución geográfica de las especies con menor volumen movilizado.")
    st_folium(mapa, width=700, height=500)






# Cargar datos
gdf = cargar_y_relacionar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Realizar el análisis automáticamente
    analizar_especies(gdf)
    graficar_mapa_de_calor_top_10_municipios(gdf)
    # Llamada a la función de análisis (suponiendo que gdf ya está cargado)
    analizar_evolucion_temporal(gdf)
    # Llamada a la función de análisis (suponiendo que gdf ya está cargado)
    analizar_outliers(gdf)
    # Llamada a la función de agrupamiento (suponiendo que gdf ya está cargado)
    agrupar_por_municipio(gdf)
    # Llamada a la función de análisis (suponiendo que gdf ya está cargado)
    analizar_especies_con_menor_volumen(gdf)
