import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Cargar el dataset
ruta = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
df = pd.read_csv(ruta)

# Convertir la columna Fecha a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Aplicar interpolación lineal a la fecha
df['Fecha'] = df['Fecha'].interpolate()

# Interpolación lineal para datos continuos
df[['Latitud', 'Longitud', 'Altitud', 'Precipitacion']] = df[['Latitud', 'Longitud', 'Altitud', 'Precipitacion']].interpolate()

# Rellenar datos numéricos con la media
columnas_numericas = ['Superficie_Deforestada', 'Tasa_Deforestacion', 'Pendiente', 'Distancia_Carretera', 'Temperatura']
df[columnas_numericas] = df[columnas_numericas].fillna(df[columnas_numericas].mean())

# Rellenar la columna categórica con el valor más frecuente
df['Tipo_Vegetacion'] = df['Tipo_Vegetacion'].fillna(df['Tipo_Vegetacion'].mode()[0])

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
altitud_slider = st.slider("Seleccionar altitud", min_value=int(df['Altitud'].min()), max_value=int(df['Altitud'].max()), value=(int(df['Altitud'].min()), int(df['Altitud'].max())))
precipitacion_slider = st.slider("Seleccionar precipitación", min_value=int(df['Precipitacion'].min()), max_value=int(df['Precipitacion'].max()), value=(int(df['Precipitacion'].min()), int(df['Precipitacion'].max())))

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


