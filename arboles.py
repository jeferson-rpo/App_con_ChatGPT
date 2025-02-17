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

def graficar_mapa_calor(df):
    """
    Genera un mapa de calor para visualizar la distribución geográfica de las especies de madera movilizada
    según el departamento seleccionado.

    Args:
        df (pd.DataFrame): DataFrame con las especies de madera movilizada filtradas por departamento.
    """
    # Crear el mapa centrado en el centro de Colombia
    mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6)

    # Filtrar las columnas de latitud y longitud
    heat_data = df[['LATITUD', 'LONGITUD', 'VOLUMEN M3']].dropna()

    # Agregar el HeatMap al mapa
    HeatMap(data=heat_data[['LATITUD', 'LONGITUD', 'VOLUMEN M3']].values.tolist()).add_to(mapa)

    # Mostrar el mapa en Streamlit
    st.markdown("---")
    st.markdown("## Mapa de Calor: Distribución Geográfica de Especies")
    st.markdown("---")
    st.write(mapa)

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

    # Graficar mapa de calor para el departamento seleccionado
    graficar_mapa_calor(especies_depto)

st.title("Análisis de Madera Movilizada")

# Cargar datos
gdf = cargar_y_relacionar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Realizar el análisis automáticamente
    analizar_especies(gdf)
