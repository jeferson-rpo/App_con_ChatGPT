import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

def cargar_datos():
    """
    Carga un archivo CSV con datos geográficos.
    """
    archivo = st.file_uploader("Sube un archivo CSV", type="csv")
    
    if archivo is not None:
        df = pd.read_csv(archivo)
        return df
    
    return None

def preparar_geodataframe(df):
    """
    Convierte un DataFrame en un GeoDataFrame usando Latitud y Longitud.
    """
    if 'Latitud' not in df.columns or 'Longitud' not in df.columns:
        st.error("Las columnas 'Latitud' y 'Longitud' no están en los datos.")
        return None

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitud, df.Latitud))
    gdf.set_crs(epsg=4326, inplace=True)  # Coordenadas WGS84
    
    return gdf

def mostrar_mapas(gdf):
    """
    Muestra mapas de ubicación de clientes en Centro y Sudamérica.
    """
    # Cargar shapefile del mundo
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    world = gpd.read_file(ruta_0)

    # Filtrar países de Centro y Sudamérica
    paises_latam = [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica", "Cuba", 
        "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras", 
        "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela"
    ]
    world = world[world["NAME"].isin(paises_latam)]

    # Límites geográficos de Centro y Sudamérica
    xlim = (-120, -30)
    ylim = (-60, 30)

    # ---------- Mapa General ----------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")
    gdf.plot(ax=ax, color="blue", markersize=10, alpha=0.7)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title("Mapa de Clientes - Centro y Sudamérica")
    st.pyplot(fig)

    # ---------- Mapa por Género ----------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")
    gdf[gdf["Género"] == "Femenino"].plot(ax=ax, color="pink", markersize=10, alpha=0.7, label="Femenino")
    gdf[gdf["Género"] == "Masculino"].plot(ax=ax, color="blue", markersize=10, alpha=0.7, label="Masculino")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.legend()
    ax.set_title("Mapa de Clientes por Género - Centro y Sudamérica")
    st.pyplot(fig)

    # ---------- Mapa de Frecuencia de Compra ----------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")

    gdf[gdf["Frecuencia_Compra"] == "Baja"].plot(ax=ax, color="green", markersize=10, alpha=0.7, label="Baja")
    gdf[gdf["Frecuencia_Compra"] == "Media"].plot(ax=ax, color="yellow", markersize=10, alpha=0.7, label="Media")
    gdf[gdf["Frecuencia_Compra"] == "Alta"].plot(ax=ax, color="red", markersize=10, alpha=0.7, label="Alta")

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.legend()
    ax.set_title("Mapa de Frecuencia de Compra - Centro y Sudamérica")
    st.pyplot(fig)

def mostrar_mapa_interactivo(gdf):
    """
    Muestra un mapa interactivo con puntos de clientes usando Folium.
    """
    st.subheader("Mapa Interactivo")

    # Centro del mapa en Sudamérica
    mapa = folium.Map(location=[-15, -60], zoom_start=4)

    # Agregar puntos al mapa
    for _, row in gdf.iterrows():
        folium.Marker(
            location=[row["Latitud"], row["Longitud"]],
            popup=f"Cliente: {row['Género']} - Frecuencia: {row['Frecuencia_Compra']}",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(mapa)

    folium_static(mapa)

# ---------- MAIN STREAMLIT APP ----------
st.title("Análisis de Deforestación")

df = cargar_datos()

if df is not None:
    gdf = preparar_geodataframe(df)
    
    if gdf is not None:
        st.write("Archivo cargado exitosamente.")

        # Mostrar mapa estático
        mostrar_mapas(gdf)

        # Mostrar mapa interactivo
        mostrar_mapa_interactivo(gdf)
