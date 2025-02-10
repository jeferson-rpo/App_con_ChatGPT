import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

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

def depurar_datos(df):
    """
    Limpia los datos imputando valores faltantes y transformando algunas columnas.
    """
    df = df.copy()
    df['Ingreso_Anual_USD'].fillna(df['Ingreso_Anual_USD'].mean(), inplace=True)
    df['Edad'].fillna(round(df['Edad'].mean()), inplace=True)
    df['Historial_Compras'].fillna(round(df['Historial_Compras'].mean()), inplace=True)
    df['Latitud'].fillna(df['Latitud'].mean(), inplace=True)
    df['Longitud'].fillna(df['Longitud'].mean(), inplace=True)
    df['Frecuencia_Compra'].fillna("Media", inplace=True)
    df['Nombre'].fillna(df['Nombre'].mode()[0], inplace=True)
    df['Género'].fillna(df['Género'].mode()[0], inplace=True)
    return df

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

def mostrar_correlacion(df):
    """
    Muestra una matriz de correlación de las variables numéricas en el dataset.
    """
    # Seleccionar solo las columnas numéricas
    df_num = df.select_dtypes(include=['number'])
    
    # Generar la matriz de correlación
    corr = df_num.corr()

    # Graficar el mapa de calor
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Matriz de Correlación")
    st.pyplot(fig)

# =============================================================================
# Interfaz Principal
# =============================================================================

st.title("Análisis de Datos de Clientes")

# Cargar datos (sin mostrarlos inmediatamente en el área principal)
df = cargar_datos()
if df is not None:
    st.write("Archivo cargado exitosamente.")
    
    # Botones en la barra lateral
    if st.sidebar.button("Depurar Datos"):
        df_clean = depurar_datos(df)
        st.write("### Datos depurados:")
        st.write(df_clean)
        
    if st.sidebar.button("Mostrar Mapas"):
        df_clean = depurar_datos(df)
        mostrar_mapas(df_clean)

    if st.sidebar.button("Mostrar Correlación"):
        df_clean = depurar_datos(df)
        mostrar_correlacion(df_clean)
