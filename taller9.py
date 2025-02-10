import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# =============================================================================
# Funciones
# =============================================================================

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
    Muestra un mapa de deforestación con los datos disponibles.
    """
    st.write("### Mapa de Deforestación")
    
    # Convertir DataFrame en GeoDataFrame si tiene coordenadas
    if 'Longitud' in gdf.columns and 'Latitud' in gdf.columns:
        gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf["Longitud"], gdf["Latitud"]))
    else:
        st.error("No se encontraron coordenadas en el dataset.")
        return

    # Cargar mapa base de Sudamérica
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    sudamerica = world[world.continent == "South America"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sudamerica.plot(ax=ax, color="lightgrey", edgecolor="black")

    # Graficar puntos de deforestación
    gdf.plot(ax=ax, color="green", markersize=5, alpha=0.6, label="Zonas de Deforestación")

    ax.set_title("Mapa de Deforestación en Sudamérica")
    ax.legend()
    st.pyplot(fig)

# =============================================================================
# Interfaz Principal
# =============================================================================

st.title("Análisis de Datos de Clientes y Deforestación")

# Cargar datos (debe estar preprocesado en la variable `gdf`)
if 'gdf' in locals() or 'gdf' in globals():
    st.write("Dataset cargado exitosamente.")
    gdf_clean = depurar_datos(gdf)
    
    # Botones en la barra lateral
    if st.sidebar.button("Mostrar Correlaciones"):
        graficar_correlaciones(gdf_clean)
        
    if st.sidebar.button("Mostrar Mapas de Clientes"):
        mostrar_mapas(gdf_clean) 

    if st.sidebar.button("Mostrar Mapa de Deforestación"):
        mostrar_mapa_deforestacion(gdf_clean)
else:
    st.error("No se encontró el dataset `gdf`. Asegúrate de cargarlo antes de ejecutar la aplicación.")
