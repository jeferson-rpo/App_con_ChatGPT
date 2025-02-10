import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar para cargar datos
st.sidebar.title("Opciones de Carga de Datos")
opcion = st.sidebar.radio("Selecciona una opción", ("Cargar desde URL", "Subir archivo"))

gdf = None  # Inicializar DataFrame

if opcion == "Cargar desde URL":
    url = st.sidebar.text_input("Introduce la URL del CSV", "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
    if st.sidebar.button("Cargar Datos"):
        gdf = pd.read_csv(url)
        st.write("Datos cargados desde la URL:", gdf)

if opcion == "Subir archivo":
    archivo = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo and st.sidebar.button("Cargar Datos"):
        gdf = pd.read_csv(archivo)
        st.write("Datos cargados:", gdf)

if gdf is not None:
    if st.button("Depurar Datos"):
        # Identificar los NaN en el DataFrame
        st.write("NaN en las columnas:", gdf.isna().sum())

        # Rellenar NaN en 'Ingreso_Anual_USD' con el promedio de la columna
        gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean(), inplace=True)
        
        # Rellenar NaN en 'Edad' con el valor entero más cercano al promedio
        gdf['Edad'].fillna(round(gdf['Edad'].mean()), inplace=True)
        
        # Rellenar NaN en 'Historial_Compras' con el valor entero más cercano al promedio
        gdf['Historial_Compras'].fillna(round(gdf['Historial_Compras'].mean()), inplace=True)
        
        # Imputar 'Nombre' y 'Género' con los valores más frecuentes
        gdf['Nombre'].fillna(gdf['Nombre'].mode()[0], inplace=True)
        gdf['Género'].fillna(gdf['Género'].mode()[0], inplace=True)
        
        # Mostrar datos después de la limpieza
        st.write("Datos después de la depuración:", gdf)

    if st.button("Mostrar Correlaciones"):
        # Correlación global
        correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
        
        # Correlación por Género
        correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
        
        # Correlación por Frecuencia de Compra
        correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
        
        # Gráfico de correlación global
        fig1, ax1 = plt.subplots()
        ax1.bar(['Global'], [correlation_global], color='b')
        ax1.set_title("Correlación Global Edad vs. Ingreso Anual USD")
        ax1.set_ylabel("Correlación")
        st.pyplot(fig1)

        # Gráfico de correlación por género
        fig2, ax2 = plt.subplots()
        ax2.bar(correlation_por_genero.index, correlation_por_genero.values, color='g')
        ax2.set_title("Correlación por Género Edad vs. Ingreso Anual USD")
        ax2.set_ylabel("Correlación")
        st.pyplot(fig2)

        # Gráfico de correlación por frecuencia de compra
        fig3, ax3 = plt.subplots()
        ax3.bar(correlation_por_frecuencia.index, correlation_por_frecuencia.values, color='r')
        ax3.set_title("Correlación por Frecuencia de Compra Edad vs. Ingreso Anual USD")
        ax3.set_ylabel("Correlación")
        st.pyplot(fig3)
