def mostrar_mapas(gdf):
    """
    Muestra mapas de ubicación de clientes enfocados en Centro y Sudamérica.
    """
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

    # Convertir DataFrame en GeoDataFrame
    gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf["Longitud"], gdf["Latitud"]))

    # Ajustar los límites del mapa (aprox. latitudes y longitudes de la región)
    xlim = (-120, -30)
    ylim = (-60, 30)

    # -------------------- Mapa Global de Clientes --------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")
    gdf.plot(ax=ax, color="blue", markersize=10, alpha=0.7)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title("Mapa de Clientes - Centro y Sudamérica")
    st.pyplot(fig)

    # -------------------- Mapa por Género --------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")
    gdf[gdf["Género"] == "Femenino"].plot(ax=ax, color="pink", markersize=10, alpha=0.7, label="Femenino")
    gdf[gdf["Género"] == "Masculino"].plot(ax=ax, color="blue", markersize=10, alpha=0.7, label="Masculino")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.legend()
    ax.set_title("Mapa de Clientes por Género - Centro y Sudamérica")
    st.pyplot(fig)

    # -------------------- Mapa de Calor de Frecuencia de Compra --------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color="lightgrey", edgecolor="black")

    # Aplicar colores sin for
    gdf_baja = gdf[gdf["Frecuencia_Compra"] == "Baja"]
    gdf_media = gdf[gdf["Frecuencia_Compra"] == "Media"]
    gdf_alta = gdf[gdf["Frecuencia_Compra"] == "Alta"]

    gdf_baja.plot(ax=ax, color="green", markersize=10, alpha=0.7, label="Baja")
    gdf_media.plot(ax=ax, color="yellow", markersize=10, alpha=0.7, label="Media")
    gdf_alta.plot(ax=ax, color="red", markersize=10, alpha=0.7, label="Alta")
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.legend()
    ax.set_title("Mapa de Calor de Frecuencia de Compra - Centro y Sudamérica")
    st.pyplot(fig)
