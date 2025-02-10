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

def mostrar_mapa_deforestacion():
    """
    Muestra un mapa de deforestación basado en variables de tipo de vegetación, altitud y precipitación.
    """
    """
    Muestra un mapa filtrado según las selecciones del usuario.
    Permite elegir hasta cuatro variables con su respectivo rango o categoría.
    """
    st.sidebar.write("### Selecciona los filtros para el mapa")

    # Filtros para Género y Frecuencia de Compra (listas de selección)
    generos_seleccionados = st.sidebar.multiselect("Selecciona Género", gdf["Género"].unique(), default=gdf["Género"].unique())
    frecuencia_seleccionada = st.sidebar.multiselect("Selecciona Frecuencia de Compra", gdf["Frecuencia_Compra"].unique(), default=gdf["Frecuencia_Compra"].unique())

    # Filtros de rango para Edad e Ingreso Anual
    min_edad, max_edad = st.sidebar.slider("Rango de Edad", int(gdf["Edad"].min()), int(gdf["Edad"].max()), (int(gdf["Edad"].min()), int(gdf["Edad"].max())))
    min_ingreso, max_ingreso = st.sidebar.slider("Rango de Ingreso Anual (USD)", int(gdf["Ingreso_Anual_USD"].min()), int(gdf["Ingreso_Anual_USD"].max()), (int(gdf["Ingreso_Anual_USD"].min()), int(gdf["Ingreso_Anual_USD"].max())))

    # Aplicar filtros
    gdf_filtrado = gdf[
        (gdf["Género"].isin(generos_seleccionados)) &
        (gdf["Frecuencia_Compra"].isin(frecuencia_seleccionada)) &
        (gdf["Edad"].between(min_edad, max_edad)) &
        (gdf["Ingreso_Anual_USD"].between(min_ingreso, max_ingreso))
    ]

    if gdf_filtrado.empty:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")
        return

    # Convertir a GeoDataFrame
    gdf_filtrado = gpd.GeoDataFrame(gdf_filtrado, geometry=gpd.points_from_xy(gdf_filtrado["Longitud"], gdf_filtrado["Latitud"]))

    # Graficar mapa
    fig, ax = plt.subplots(figsize=(10, 6))
    gdf_filtrado.plot(ax=ax, marker="o", color="blue", markersize=10, alpha=0.6)
    ax.set_xlim(gdf["Longitud"].min() - 1, gdf["Longitud"].max() + 1)
    ax.set_ylim(gdf["Latitud"].min() - 1, gdf["Latitud"].max() + 1)
    ax.set_title("Mapa de Clientes - Filtros Aplicados")

    st.pyplot(fig)


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
        gdf_clean = depurar_datos(gdf)  # Asegurar que los datos estén depurados
        mostrar_mapa_deforestacion(gdf_clean)  # Pasar gdf_clean como argumento
