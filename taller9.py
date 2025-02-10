import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def mostrar_mapa_deforestacion(gdf_clean):
    """
    Muestra un mapa interactivo de deforestación basado en los datos depurados.
    """
    st.write("### Mapa Interactivo de Deforestación")

    if gdf_clean is not None:
        # Convertimos el DataFrame en un GeoDataFrame si aún no lo es
        if not isinstance(gdf_clean, gpd.GeoDataFrame):
            gdf_clean = gpd.GeoDataFrame(gdf_clean, geometry=gpd.points_from_xy(gdf_clean["Longitud"], gdf_clean["Latitud"]))
        
        # Cargar el shapefile del mundo desde Natural Earth
        ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
        world = gpd.read_file(ruta_0)

        # Filtrar solo los países de Centro y Sudamérica
        paises_latam = [
            "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica", "Cuba", 
            "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras", 
            "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela"
        ]
        world = world[world["NAME"].isin(paises_latam)]

        # Ajustar los límites del mapa (aprox. latitudes y longitudes de la región)
        xlim = (-120, -30)
        ylim = (-60, 30)

        # Crear figura y ejes
        fig, ax = plt.subplots(figsize=(10, 6))
        world.plot(ax=ax, color="lightgrey", edgecolor="black")

        # Graficar los puntos de deforestación con color rojo
        gdf_clean.plot(ax=ax, color="red", markersize=10, alpha=0.7, label="Deforestación")

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title("Mapa Interactivo de Deforestación - Centro y Sudamérica")
        ax.legend()

        st.pyplot(fig)
    else:
        st.warning("No hay datos disponibles para mostrar el mapa.")

# Agregar el botón en la barra lateral
if st.sidebar.button("Mostrar Mapa Interactivo de Deforestación"):
    mostrar_mapa_deforestacion(gdf_clean)
