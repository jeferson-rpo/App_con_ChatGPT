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

def graficar_correlaciones(gdf):
    """
    Grafica la correlación entre Edad e Ingreso Anual USD en tres niveles:
      - Global
      - Por Género
      - Por Frecuencia de Compra
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 12))
    
    # Correlación global
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    axes[0].bar(['Global'], [correlation_global], color='b')
    axes[0].set_title("Correlación Global entre Edad e Ingreso Anual USD")
    axes[0].set_ylabel("Correlación")
    
    # Correlación por Género
    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    axes[1].bar(correlation_por_genero.index, correlation_por_genero.values, color='g')
    axes[1].set_title("Correlación entre Edad e Ingreso Anual USD por Género")
    axes[1].set_ylabel("Correlación")
    
    # Correlación por Frecuencia de Compra
    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    axes[2].bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r')
    axes[2].set_title("Correlación entre Edad e Ingreso Anual USD por Frecuencia de Compra")
    axes[2].set_ylabel("Correlación")
    
    plt.tight_layout()
    st.pyplot(fig)

def mostrar_mapas(gdf):
    """
    Muestra mapas de ubicación de clientes enfocados en Centro y Sudamérica.
    """
    # Cargar el shapefile del mundo desde Natural Earth
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Filtrar solo los países de Centro y Sudamérica
    paises_latam = [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica", "Cuba", 
        "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras", 
        "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela"
    ]
    world = world[world["name"].isin(paises_latam)]

    # Convertir DataFrame en GeoDataFrame
    gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf["Longitud"], gdf["Latitud"]))

    # Ajustar los límites del mapa (aprox. latitudes y longitudes de la región)
    xlim = (-120, -30)
    ylim = (-60, 30)

    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")
    gdf.plot(ax=ax, color="blue", markersize=10, alpha=0.7)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title("Mapa de Clientes - Centro y Sudamérica")
    st.pyplot(fig)

def mostrar_mapa_deforestacion(gdf):
    """
    Muestra un mapa interactivo de deforestación con filtros de selección.
    """
    st.write("### Mapa Interactivo de Deforestación")

   

# =============================================================================
# Interfaz Principal
# =============================================================================

st.title("Análisis de Deforestación")

# Cargar los datos desde un CSV depurado (asegúrate de cambiarlo por el tuyo)


# =============================================================================
# Interfaz Principal
# =============================================================================

st.title("Análisis de Datos de Clientes y Deforestación")

# Cargar datos (sin mostrarlos inmediatamente en el área principal)
gdf = cargar_datos()
if gdf is not None:
    st.write("Archivo cargado exitosamente.")
    
    # Botones en la barra lateral
    if st.sidebar.button("Depurar Datos"):
        gdf_clean = depurar_datos(gdf)
        st.write("### Datos depurados:")
        st.write(gdf_clean)
        
    if st.sidebar.button("Mostrar Correlaciones"):
        gdf_clean = depurar_datos(gdf)
        graficar_correlaciones(gdf_clean)
        
    if st.sidebar.button("Mostrar Mapas de Clientes"):
        gdf_clean = depurar_datos(gdf)
        mostrar_mapas(gdf_clean) 

    if st.sidebar.button("Mostrar Mapa de Deforestación"):
        gdf_clean = depurar_datos(gdf)
        mostrar_mapa_deforestacion(gdf_clean)
