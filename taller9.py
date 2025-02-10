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

def mostrar_mapa_interactivo(gdf_filtrado, world):
    """
    Genera un mapa de clientes en Centro y Sudamérica con los datos filtrados.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Dibujar el mapa de países
    world.plot(ax=ax, color="lightgrey", edgecolor="black")

    # Aplicar colores según la frecuencia de compra
    colores = gdf_filtrado["Frecuencia_Compra"].map({"Baja": "green", "Media": "yellow", "Alta": "red"})

    # Graficar los clientes filtrados
    gdf_filtrado.plot(ax=ax, color=colores, markersize=10, alpha=0.7)

    ax.set_xlim(-120, -30)
    ax.set_ylim(-60, 30)
    ax.set_title("Mapa de Clientes - Centro y Sudamérica")

    # Mostrar en Streamlit
    st.pyplot(fig)


# =============================================================================
# Cargar Datos
# =============================================================================
gdf = cargar_datos()

if gdf is not None:
    st.write("Archivo cargado exitosamente.")

    # Limpiar los datos
    gdf = depurar_datos(gdf)

    # Cargar shapefile de países
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    world = gpd.read_file(ruta_0)

    # Filtrar solo los países de Centro y Sudamérica
    paises_latam = [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica", "Cuba", 
        "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras", 
        "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela"
    ]
    world = world[world["NAME"].isin(paises_latam)]

    # =============================================================================
    # Filtros Interactivos
    # =============================================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        genero_seleccionado = st.radio("Género", ["Todos"] + gdf["Género"].unique().tolist())
    with col2:
        frecuencia_seleccionada = st.radio("Frecuencia de Compra", ["Todos"] + gdf["Frecuencia_Compra"].unique().tolist())
    with col3:
        edad_min, edad_max = st.slider("Edad", int(gdf["Edad"].min()), int(gdf["Edad"].max()), 
                                       (int(gdf["Edad"].min()), int(gdf["Edad"].max())))
    with col4:
        ingreso_min, ingreso_max = st.slider("Ingreso Anual (USD)", int(gdf["Ingreso_Anual_USD"].min()), 
                                             int(gdf["Ingreso_Anual_USD"].max()), 
                                             (int(gdf["Ingreso_Anual_USD"].min()), int(gdf["Ingreso_Anual_USD"].max())))

    # Aplicar filtros vectorizados
    mask = ((gdf["Edad"] >= edad_min) & (gdf["Edad"] <= edad_max) & 
            (gdf["Ingreso_Anual_USD"] >= ingreso_min) & (gdf["Ingreso_Anual_USD"] <= ingreso_max))

    if genero_seleccionado != "Todos":
        mask &= gdf["Género"] == genero_seleccionado

    if frecuencia_seleccionada != "Todos":
        mask &= gdf["Frecuencia_Compra"] == frecuencia_seleccionada

    # Filtrar los datos sin modificar la geometría
    gdf_filtrado = gdf[mask]

    # Mostrar Mapa
    mostrar_mapa_interactivo(gdf_filtrado, world)
