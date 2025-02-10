from streamlit_folium import folium_static
import geopandas as gpd

def cargar_datos():
    """Carga el archivo CSV desde una URL o un archivo subido."""
    opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))
    
    if opcion == "Cargar archivo desde URL":
        url = st.text_input("Introduce la URL del archivo CSV",
                            "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
        if url:
            return pd.read_csv(url)
    
    if opcion == "Subir archivo":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            return pd.read_csv(archivo)
    
    return None

def limpiar_datos(gdf):
    """Limpia y completa los datos faltantes en el DataFrame."""
    if gdf is None:
        return None

    st.write("NaN en las columnas antes de la limpieza:", gdf.isna().sum())

    gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean())
    gdf['Edad'] = gdf['Edad'].fillna(round(gdf['Edad'].mean()))
    gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(round(gdf['Historial_Compras'].mean()))

    correlation_latitud = gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_latitud)

    correlation_longitud = gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Ingreso_Anual_USD'] * correlation_longitud)

    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1)

    gdf['Nombre'] = gdf['Nombre'].fillna(gdf['Nombre'].mode()[0])
    gdf['Género'] = gdf['Género'].fillna(gdf['Género'].mode()[0])

    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map)
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(1)
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)

    st.write("Datos después de la limpieza:", gdf)
    return gdf

def analizar_correlaciones(gdf):
    """Calcula y muestra las correlaciones entre Edad e Ingreso Anual USD."""
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write(f"Correlación global entre Edad e Ingreso Anual USD: {correlation_global:.2f}")

    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Género:")
    st.write(correlation_por_genero)

    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Frecuencia de Compra:")
    st.write(correlation_por_frecuencia)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar('Global', correlation_global, color='b', label='Global')
    ax.bar(correlation_por_genero.index, correlation_por_genero.values, color='g', label='Por Género')
    ax.bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r', label='Por Frecuencia de Compra')

    ax.set_title("Correlación entre Edad e Ingreso Anual USD")
    ax.set_ylabel("Correlación")
    ax.legend(loc='best')
    st.pyplot(fig)

def mostrar_mapa_interactivo(gdf):
    """Genera y muestra un mapa interactivo con los puntos del dataset."""
    if gdf is None or 'Latitud' not in gdf.columns or 'Longitud' not in gdf.columns:
        st.write("No hay datos de coordenadas para mostrar el mapa.")
        return
    
    st.write("Mapa interactivo de ubicaciones")
    
    # Convertir el DataFrame en un GeoDataFrame
    gdf_geo = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf['Longitud'], gdf['Latitud']))

    # Crear el mapa centrado en el promedio de las coordenadas
    centro_mapa = [gdf['Latitud'].mean(), gdf['Longitud'].mean()]
    mapa = folium.Map(location=centro_mapa, zoom_start=6)

    # Agregar puntos al mapa
    for _, row in gdf_geo.iterrows():
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=f"{row['Nombre']} - {row['Ingreso_Anual_USD']}$"
        ).add_to(mapa)

    folium_static(mapa)

# --- EJECUCIÓN DEL PROGRAMA ---

gdf = cargar_datos()
if gdf is not None:
    gdf = limpiar_datos(gdf)
    analizar_correlaciones(gdf)
    mostrar_mapa_interactivo(gdf)
