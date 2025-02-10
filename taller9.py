import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import geopandas as gpd

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
    # Rellenar NaN en 'Ingreso_Anual_USD' con el promedio
    gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean(), inplace=True)
    # Rellenar NaN en 'Edad' con el valor entero más cercano al promedio
    gdf['Edad'].fillna(round(gdf['Edad'].mean()), inplace=True)
    # Rellenar NaN en 'Historial_Compras' con el valor entero más cercano al promedio
    gdf['Historial_Compras'].fillna(round(gdf['Historial_Compras'].mean()), inplace=True)
    # Rellenar NaN en 'Latitud' y 'Longitud' utilizando la correlación con 'Ingreso_Anual_USD'
    gdf['Latitud'].fillna(gdf['Ingreso_Anual_USD'] * gdf[['Latitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1], inplace=True)
    gdf['Longitud'].fillna(gdf['Ingreso_Anual_USD'] * gdf[['Longitud', 'Ingreso_Anual_USD']].corr().iloc[0, 1], inplace=True)
    # Rellenar NaN en 'Frecuencia_Compra' usando la relación con 'Edad'
    gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1, inplace=True)
    # Imputar 'Nombre' y 'Género' con los valores más frecuentes
    gdf['Nombre'].fillna(gdf['Nombre'].mode()[0], inplace=True)
    gdf['Género'].fillna(gdf['Género'].mode()[0], inplace=True)
    # Convertir 'Frecuencia_Compra' a categorías
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map).fillna(1).map(frec_map_inv)
    return gdf

def graficar_correlaciones(gdf):
    """
    Muestra tres gráficos de correlación:
      - Global entre Edad e Ingreso Anual USD.
      - Segmentado por Género.
      - Segmentado por Frecuencia de Compra.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 12))
    
    # Correlación global
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    axes[0].bar(['Global'], [correlation_global], color='b')
    axes[0].set_title("Correlación Global: Edad vs. Ingreso Anual USD")
    axes[0].set_ylabel("Correlación")
    
    # Correlación por Género
    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    axes[1].bar(correlation_por_genero.index, correlation_por_genero.values, color='g')
    axes[1].set_title("Correlación por Género: Edad vs. Ingreso Anual USD")
    axes[1].set_ylabel("Correlación")
    
    # Correlación por Frecuencia de Compra
    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    axes[2].bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r')
    axes[2].set_title("Correlación por Frecuencia de Compra: Edad vs. Ingreso Anual USD")
    axes[2].set_ylabel("Correlación")
    
    plt.tight_layout()
    st.pyplot(fig)

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
    world_geojson = world.to_json()
    
    # Crear capa base con límites de países
    layer_world = pdk.Layer(
        "GeoJsonLayer",
        data=world_geojson,
        opacity=0.5,
        stroked=True,
        filled=True,
        get_fill_color="[200, 200, 200, 50]",
        get_line_color=[255, 255, 255],
        pickable=True,
    )
    
    # Definir la vista inicial centrada en los datos
    view_state = pdk.ViewState(
        latitude=gdf["Latitud"].mean(),
        longitude=gdf["Longitud"].mean(),
        zoom=2,
        pitch=0
    )
    
    # -------------------- Mapa Global --------------------
    # Capa de dispersión de todos los clientes
    layer_global = pdk.Layer(
        "ScatterplotLayer",
        data=gdf,
        get_position=["Longitud", "Latitud"],
        get_color="[0, 0, 255]",
        get_radius=50000,
        radiusMinPixels=5,
    )
    st.subheader("Mapa Global de Clientes")
    r_global = pdk.Deck(layers=[layer_world, layer_global], initial_view_state=view_state)
    st.pydeck_chart(r_global)
    
    # -------------------- Mapa por Género --------------------
    # Separar datos por género (se espera que 'Género' tenga valores 'Femenino' y 'Masculino')
    gdf_f = gdf[gdf["Género"].str.lower() == "femenino"]
    gdf_m = gdf[gdf["Género"].str.lower() == "masculino"]
    
    layer_f = pdk.Layer(
        "ScatterplotLayer",
        data=gdf_f,
        get_position=["Longitud", "Latitud"],
        get_color="[255, 105, 180]",  # Rosa para femenino
        get_radius=50000,
        radiusMinPixels=5,
    )
    layer_m = pdk.Layer(
        "ScatterplotLayer",
        data=gdf_m,
        get_position=["Longitud", "Latitud"],
        get_color="[65, 105, 225]",   # Azul para masculino
        get_radius=50000,
        radiusMinPixels=5,
    )
    st.subheader("Mapa de Clientes por Género")
    r_gender = pdk.Deck(layers=[layer_world, layer_f, layer_m], initial_view_state=view_state)
    st.pydeck_chart(r_gender)
    
    # -------------------- Mapa de Calor de Frecuencia de Compra --------------------
    # Para el heatmap, asignamos un peso numérico basado en la frecuencia de compra:
    # Baja=1, Media=2, Alta=3
    gdf["Frec_weight"] = gdf["Frecuencia_Compra"].map({"Baja": 1, "Media": 2, "Alta": 3})
    
    layer_heat = pdk.Layer(
        "HeatmapLayer",
        data=gdf,
        get_position=["Longitud", "Latitud"],
        get_weight="Frec_weight",
        radius_pixels=50,
    )
    st.subheader("Mapa de Calor de Frecuencia de Compra")
    r_heat = pdk.Deck(layers=[layer_world, layer_heat], initial_view_state=view_state)
    st.pydeck_chart(r_heat)

# =============================================================================
# Interfaz Principal
# =============================================================================

st.title("Análisis de Datos de Clientes")

# Cargar datos (sin mostrarlos inmediatamente en el área principal)
gdf = cargar_datos()
if gdf is not None:
    st.write("Archivo cargado exitosamente.")
    
    # Botones en la barra lateral (cada uno muestra únicamente su salida)
    if st.sidebar.button("Depurar Datos"):
        gdf_clean = depurar_datos(gdf)
        st.write("### Datos depurados:")
        st.write(gdf_clean)
        
    if st.sidebar.button("Mostrar Correlaciones"):
        gdf_clean = depurar_datos(gdf)
        graficar_correlaciones(gdf_clean)
        
    if st.sidebar.button("Mostrar Mapas"):
        gdf_clean = depurar_datos(gdf)
        mostrar_mapas(gdf_clean)
