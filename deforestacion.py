import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Opción para que el usuario ingrese una URL o suba un archivo
opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

# Si elige "Cargar archivo desde URL"
if opcion == "Cargar archivo desde URL":
    url = st.text_input("Introduce la URL del archivo CSV", 
                       "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv")
    if url:
        gdf = pd.read_csv(url)  # Cargar el archivo CSV desde la URL
        st.write("Datos cargados desde la URL:", gdf)

# Si elige "Subir archivo"
if opcion == "Subir archivo":
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo:
        gdf = pd.read_csv(archivo)  # Cargar el archivo CSV
        st.write("Datos cargados:", gdf)

# Limpiar los datos si se cargaron
if 'gdf' in locals():  # Verificar si se cargaron datos
    # Identificar los NaN en el DataFrame
    st.write("NaN en las columnas:", gdf.isna().sum())

    # Limpiar las columnas numéricas
    gdf_numéricas = gdf.select_dtypes(include=['float64', 'int64'])
    if not gdf_numéricas.empty:
        gdf[gdf_numéricas.columns] = gdf_numéricas.fillna(gdf_numéricas.mean())  # Rellenar NaN con la media

    # Limpiar las columnas de fechas (solo las de tipo datetime)
    gdf_fechas = gdf.select_dtypes(include=['datetime64'])
    if not gdf_fechas.empty:
        fecha_promedio = gdf_fechas.mean(axis=0)  # Calcular el promedio de las fechas
        gdf[gdf_fechas.columns] = gdf_fechas.fillna(fecha_promedio)  # Rellenar NaT con el promedio

    # Limpiar las columnas de texto (tipo object)
    gdf_texto = gdf.select_dtypes(include=['object'])
    if not gdf_texto.empty:
        valor_frecuente = gdf_texto.mode(axis=0).iloc[0]  # Obtener el valor más frecuente por columna
        gdf[gdf_texto.columns] = gdf_texto.fillna(valor_frecuente)  # Rellenar NaN con el valor más frecuente

    # Asegurarse de que los tipos de datos sean coherentes
    gdf = gdf.convert_dtypes()

    # Mostrar el DataFrame limpio
    st.write("Datos limpiados:", gdf)

    # Convertir las columnas de Latitud y Longitud a numéricas, si es necesario
    gdf['Longitud'] = pd.to_numeric(gdf['Longitud'], errors='coerce')
    gdf['Latitud'] = pd.to_numeric(gdf['Latitud'], errors='coerce')

    # Convertir el DataFrame de deforestación en un GeoDataFrame
    gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf['Longitud'], gdf['Latitud']))

    # Definir sistema de coordenadas (WGS84)
    gdf.set_crs(epsg=4326, inplace=True)

# Cargar los datos del mapa de los países
ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
mundo_dataframe = gpd.read_file(ruta_0)
amazonas_dataframe = mundo_dataframe[mundo_dataframe['NAME'].isin(['Brazil', 'Colombia', 'Peru', 'Ecuador', 'Venezuela'])]

# Función para graficar el mapa
def graficar_mapa(gdf_filtrado):
    fig, ax = plt.subplots(figsize=(12, 10))
    amazonas_dataframe.boundary.plot(ax=ax, linewidth=2, color='black')
    gdf_filtrado.plot(ax=ax, marker='x', color='red', markersize=30, alpha=0.7, label='Áreas Deforestadas')  # Aumenté el tamaño de las "x"
    ax.set_xlim(-80, -34)
    ax.set_ylim(-20, 10)
    ax.set_title("Zonas Deforestadas Filtradas")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.legend()
    st.pyplot(fig)

# Título y descripción de la app
st.title("Análisis de la Deforestación")
st.markdown("""
Este análisis permite visualizar las áreas deforestadas en el Amazonas y aplicar filtros por tipo de vegetación, altitud y precipitación. 
También podrás ver estadísticas de la deforestación.
""")

# Filtros interactivos
tipo_vegetacion_filtro = st.selectbox("Seleccionar tipo de vegetación", gdf['Tipo_Vegetacion'].unique())
altitud_slider = st.slider("Seleccionar altitud", min_value=int(gdf['Altitud'].min()), max_value=int(gdf['Altitud'].max()), value=(int(gdf['Altitud'].min()), int(gdf['Altitud'].max())))
precipitacion_slider = st.slider("Seleccionar precipitación", min_value=int(gdf['Precipitacion'].min()), max_value=int(gdf['Precipitacion'].max()), value=(int(gdf['Precipitacion'].min()), int(gdf['Precipitacion'].max())))

# Filtrar los datos según los filtros seleccionados
gdf_filtrado = gdf[
    (gdf['Tipo_Vegetacion'] == tipo_vegetacion_filtro) &
    (gdf['Altitud'] >= altitud_slider[0]) & 
    (gdf['Altitud'] <= altitud_slider[1]) &
    (gdf['Precipitacion'] >= precipitacion_slider[0]) & 
    (gdf['Precipitacion'] <= precipitacion_slider[1])
]

# Mostrar el mapa de las zonas deforestadas filtradas
graficar_mapa(gdf_filtrado)

# Análisis de superficie deforestada y tasas
superficie_deforestada = gdf_filtrado['Superficie_Deforestada'].sum()
tasa_deforestacion = gdf_filtrado['Tasa_Deforestacion'].mean()

# Promedio de Superficie Deforestada por Tipo de Vegetación
promedio_superficie_por_vegetacion = gdf_filtrado.groupby('Tipo_Vegetacion')['Superficie_Deforestada'].mean()

# Correlación entre Precipitación y Superficie Deforestada
correlacion_precipitacion_superficie = gdf_filtrado[['Precipitacion', 'Superficie_Deforestada']].corr().iloc[0, 1]

# Promedio de Temperatura por Tipo de Vegetación
promedio_temperatura_por_vegetacion = gdf_filtrado.groupby('Tipo_Vegetacion')['Temperatura'].mean()

# Mostrar los análisis de datos
st.subheader("Análisis de datos")
st.write(f"Superficie deforestada total (en hectáreas): {superficie_deforestada}")
st.write(f"Tasa de deforestación promedio: {tasa_deforestacion:.2f} %")

# Estadísticas de la Tasa de Deforestación
st.subheader("Estadísticas de la Tasa de Deforestación")
st.write(gdf_filtrado['Tasa_Deforestacion'].describe())

# Mostrar Promedio de Superficie Deforestada por Tipo de Vegetación
st.subheader("Promedio de Superficie Deforestada por Tipo de Vegetación")
st.write(promedio_superficie_por_vegetacion)

# Correlación entre Precipitación y Superficie Deforestada
st.subheader("Correlación entre Precipitación y Superficie Deforestada")
st.write(f"Correlación entre Precipitación y Superficie Deforestada: {correlacion_precipitacion_superficie:.2f}")

# Mostrar Promedio de Temperatura por Tipo de Vegetación
st.subheader("Promedio de Temperatura por Tipo de Vegetación")
st.write(promedio_temperatura_por_vegetacion)

# Mostrar estadísticas de los puntos filtrados
st.subheader("Estadísticas de las áreas deforestadas filtradas")
st.write(gdf_filtrado[['Latitud', 'Longitud']].describe())
