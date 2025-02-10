import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar y limpiar los datos
def cargar_y_limpiar_datos(url=None, archivo=None):
    if url:
        df = pd.read_csv(url)
    elif archivo:
        df = pd.read_csv(archivo)
    else:
        return None

    # Mostrar datos cargados
    st.write("### Datos cargados y depurados")
    
    # Rellenar NaN en 'Ingreso_Anual_USD'
    df['Ingreso_Anual_USD'].fillna(df['Ingreso_Anual_USD'].mean(), inplace=True)
    
    # Rellenar NaN en 'Edad'
    df['Edad'].fillna(round(df['Edad'].mean()), inplace=True)
    
    # Rellenar NaN en 'Historial_Compras'
    df['Historial_Compras'].fillna(round(df['Historial_Compras'].mean()), inplace=True)
    
    # Rellenar NaN en 'Latitud' y 'Longitud'
    df['Latitud'].fillna(df['Ingreso_Anual_USD'].corr(df['Latitud']) * df['Ingreso_Anual_USD'], inplace=True)
    df['Longitud'].fillna(df['Ingreso_Anual_USD'].corr(df['Longitud']) * df['Ingreso_Anual_USD'], inplace=True)
    
    # Rellenar NaN en 'Frecuencia_Compra' usando la relación con 'Edad'
    df['Frecuencia_Compra'].fillna(df['Edad'] * 0.1, inplace=True)
    
    # Imputar valores más frecuentes en 'Nombre' y 'Género'
    df['Nombre'].fillna(df['Nombre'].mode()[0], inplace=True)
    df['Género'].fillna(df['Género'].mode()[0], inplace=True)
    
    # Convertir 'Frecuencia_Compra' a categorías
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    df['Frecuencia_Compra'] = df['Frecuencia_Compra'].map(frec_map).fillna(1).map({0: "Baja", 1: "Media", 2: "Alta"})
    
    st.write(df)
    return df

# Función para graficar correlaciones
def graficar_correlaciones(df):
    st.write("### Análisis de Correlaciones")
    
    # Correlación global
    correlation_global = df[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    
    # Correlación por Género
    correlation_por_genero = df.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    
    # Correlación por Frecuencia de Compra
    correlation_por_frecuencia = df.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))
    
    # Gráfico global
    axs[0].bar(['Global'], [correlation_global], color='b')
    axs[0].set_title("Correlación Global")
    axs[0].set_ylabel("Correlación")
    
    # Gráfico por Género
    axs[1].bar(correlation_por_genero.index, correlation_por_genero.values, color='g')
    axs[1].set_title("Correlación por Género")
    axs[1].set_ylabel("Correlación")
    
    # Gráfico por Frecuencia de Compra
    axs[2].bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r')
    axs[2].set_title("Correlación por Frecuencia de Compra")
    axs[2].set_ylabel("Correlación")
    
    plt.tight_layout()
    st.pyplot(fig)

# Streamlit App
st.title("Análisis de Datos de Clientes")

# Opción para cargar archivo o URL
opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

gdf = None

if opcion == "Cargar archivo desde URL":
    url = st.text_input("Introduce la URL del archivo CSV",
                        "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
    if url:
        gdf = cargar_y_limpiar_datos(url=url)

if opcion == "Subir archivo":
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo:
        gdf = cargar_y_limpiar_datos(archivo=archivo)

# Barra lateral para mostrar correlaciones
if gdf is not None:
    if st.sidebar.button("Mostrar Análisis de Correlaciones"):
        graficar_correlaciones(gdf)
