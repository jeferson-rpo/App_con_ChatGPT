import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# =============================================================================
# Funciones
# =============================================================================

def cargar_datos():
    """
    Permite cargar los datos desde URL o subiendo un archivo CSV.
    """
    opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))
    if opcion == "Cargar archivo desde URL":
        url = st.text_input("Introduce la URL del archivo CSV",
                            "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
        if url:
            return pd.read_csv(url)
    elif opcion == "Subir archivo":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            return pd.read_csv(archivo)
    return None

def depurar_datos(gdf):
    """
    Limpia los datos imputando valores faltantes y transformando algunas columnas.
    """
    gdf = gdf.copy()
    gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean(), inplace=True)
    gdf['Edad'].fillna(round(gdf['Edad'].mean()), inplace=True)
    gdf['Historial_Compras'].fillna(round(gdf['Historial_Compras'].mean()), inplace=True)
    gdf['Latitud'].fillna(gdf['Latitud'].mean(), inplace=True)
    gdf['Longitud'].fillna(gdf['Longitud'].mean(), inplace=True)
    gdf['Frecuencia_Compra'].fillna("Media", inplace=True)
    gdf['Nombre'].fillna(gdf['Nombre'].mode()[0], inplace=True)
    gdf['Género'].fillna(gdf['Género'].mode()[0], inplace=True)
    return gdf

def mostrar_mapas(gdf):
    """
    Muestra tres mapas de ubicación de clientes:
      - Mapa global de clientes.
      - Mapa por Género (Femenino en rosa y Masculino en azul).
      - Mapa de calor de Frecuencia de Compra.
      
    Se utiliza el shapefile de Natural Earth ubicado en 'ruta_0'.
    """
    # Cargar el shapefile del mundo desde Natural Earth
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    world = gpd.read_file(ruta_0)

    # Convertir DataFrame en GeoDataFrame
    gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf["Longitud"], gdf["Latitud"]))
    
    # -------------------- Mapa Global --------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")
    gdf.plot(ax=ax, color="blue", markersize=10, alpha=0.7)
    ax.set_title("Mapa Global de Clientes")
    st.pyplot(fig)

    # -------------------- Mapa por Género --------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")
    gdf[gdf["Género"] == "Femenino"].plot(ax=ax, color="pink", markersize=10, alpha=0.7, label="Femenino")
    gdf[gdf["Género"] == "Masculino"].plot(ax=ax, color="blue", markersize=10, alpha=0.7, label="Masculino")
    ax.legend()
    ax.set_title("Mapa de Clientes por Género")
    st.pyplot(fig)

    # -------------------- Mapa de Calor de Frecuencia de Compra --------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")

    # Asignar colores por frecuencia de compra
    color_map = {"Baja": "green", "Media": "yellow", "Alta": "red"}
    for frecuencia, color in color_map.items():
        gdf[gdf["Frecuencia_Compra"] == frecuencia].plot(ax=ax, color=color, markersize=10, alpha=0.7, label=frecuencia)
    
    ax.legend()
    ax.set_title("Mapa de Calor de Frecuencia de Compra")
    st.pyplot(fig)

# =============================================================================
# Interfaz Principal
# =============================================================================

st.title("Análisis de Datos de Clientes")

# Cargar datos (sin mostrarlos inmediatamente en el área principal)
gdf = cargar_datos()
if gdf is not None:
    st.write("Archivo cargado exitosamente.")
    
    # Botones en la barra lateral
    if st.sidebar.button("Depurar Datos"):
        gdf_clean = depurar_datos(gdf)
        st.write("### Datos depurados:")
        st.write(gdf_clean)
        
    if st.sidebar.button("Mostrar Mapas"):
        gdf_clean = depurar_datos(gdf)
        mostrar_mapas(gdf_clean)
