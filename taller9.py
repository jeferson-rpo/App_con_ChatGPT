import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar los datos
def cargar_datos():
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

# Función para depurar/limpiar los datos
def depurar_datos(gdf):
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

# Función para graficar las correlaciones
def graficar_correlaciones(gdf):
    # Preparar tres gráficos en una figura
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

# ------------------ Interfaz principal ------------------

st.title("Análisis de Datos de Clientes")

# Cargar datos (sin mostrar nada en el área principal)
gdf = cargar_datos()

if gdf is not None:
    # Los botones se ubican en la barra lateral
    btn_depurar = st.sidebar.button("Depurar Datos")
    btn_correlacion = st.sidebar.button("Mostrar Correlaciones")
    
    # Si se presiona "Depurar Datos", se muestran solo los datos depurados
    if btn_depurar:
        gdf_clean = depurar_datos(gdf)
        st.write("### Datos después de la limpieza:")
        st.write(gdf_clean)
    
    # Si se presiona "Mostrar Correlaciones", se muestran solo los gráficos de correlación
    if btn_correlacion:
        gdf_clean = depurar_datos(gdf)
        graficar_correlaciones(gdf_clean)
