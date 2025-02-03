import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Ruta
ruta="https://raw.githubusercontent.com/gabrielawad/programacion-para-\
ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.\
csv"

# Cargar el dataset
df = pd.read_csv(ruta)

# Convertir la columna Fecha a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Aplicar interpolación lineal a la fecha
df['Fecha'] = df['Fecha'].interpolate()

# Interpolación lineal para datos continuos (fecha, latitud, longitud, altitud, precipitación)
df[['Latitud', 'Longitud', 'Altitud', 'Precipitacion']] =\
 df[['Latitud', 'Longitud', 'Altitud', 'Precipitacion']].interpolate()

# Rellenar datos numéricos con la media
columnas_numericas = ['Superficie_Deforestada', 'Tasa_Deforestacion', 'Pendiente', 'Distancia_Carretera', 'Temperatura']
df[columnas_numericas] = df[columnas_numericas].fillna(df[columnas_numericas].mean())

# Rellenar la columna categórica con el valor más frecuente
df['Tipo_Vegetacion'] = df['Tipo_Vegetacion'].fillna(df['Tipo_Vegetacion'].mode()[0])

# Rellenar los valores nulos en la columna 'Altitud' con 0
df['Altitud'] = df['Altitud'].fillna(0)

# Convertir el DataFrame de deforestación en un GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitud'], df['Latitud']))

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
    gdf_filtrado.plot(ax=ax, marker='x', color='red', markersize=10, alpha=0.7, label='Áreas Deforestadas')
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
tipo_vegetacion_filtro = st.selectbox("Seleccionar tipo de vegetación", df['Tipo_Vegetacion'].unique())

# Ahora usando valores corregidos para la altitud
altitud_min = st.slider("Seleccionar altitud mínima", min_value=df['Altitud'].min(), max_value=df['Altitud'].max(), value=0)
altitud_max = st.slider("Seleccionar altitud máxima", min_value=df['Altitud'].min(), max_value=df['Altitud'].max(), value=df['Altitud'].max())

# Filtros para precipitación
precipitacion_min = st.slider("Seleccionar precipitación mínima", min_value=df['Precipitacion'].min(), max_value=df['Precipitacion'].max(), value=df['Precipitacion'].min())
precipitacion_max = st.slider("Seleccionar precipitación máxima", min_value=df['Precipitacion'].min(), max_value=df['Precipitacion'].max(), value=df['Precipitacion'].max())

# Filtrar los datos según los filtros seleccionados
gdf_filtrado = gdf[
    (gdf['Tipo_Vegetacion'] == tipo_vegetacion_filtro) &
    (gdf['Altitud'] >= altitud_min) & 
    (gdf['Altitud'] <= altitud_max) &
    (gdf['Precipitacion'] >= precipitacion_min) & 
    (gdf['Precipitacion'] <= precipitacion_max)
]

# Mostrar el mapa de las zonas deforestadas filtradas
graficar_mapa(gdf_filtrado)

# Análisis de superficie deforestada y tasas
superficie_deforestada = gdf_filtrado['Superficie_Deforestada'].sum()
tasa_deforestacion = gdf_filtrado['Tasa_Deforestacion'].mean()

# Mostrar los análisis de datos
st.subheader("Análisis de datos")
st.write(f"Superficie deforestada total (en hectáreas): {superficie_deforestada}")
st.write(f"Tasa de deforestación promedio: {tasa_deforestacion:.2f} %")

# Mostrar estadísticas de los puntos filtrados
st.subheader("Estadísticas de las áreas deforestadas filtradas")
st.write(gdf_filtrado[['Latitud', 'Longitud']].describe())




