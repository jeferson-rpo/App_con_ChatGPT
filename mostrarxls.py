import pandas as pd
#codigo realizado por geminis
#importar librerias 
import streamlit as st
import re

# Función para extraer la información de una línea
def extraer_info(linea):
    # ... (tu código de extracción de información)

# Función para cargar los datos desde el CSV
def cargar_datos(archivo_csv):
    datos = []
    with open(archivo_csv, "r") as f:
        lineas = f.readlines()
        for linea in lineas:
            datos.append(extraer_info(linea))
    df = pd.DataFrame(datos, columns=["Nombre", "Email", "Teléfono", "Fecha", "Valor"])
    return df

# Crear la aplicación Streamlit
def app():
    st.title("Explorador de Datos de Productos")

    # Cargar los datos
    df = cargar_datos("tu_archivo.csv")

    # Crear un selector para filtrar por nombre de producto
    producto = st.selectbox("Selecciona un producto", df['Nombre'].unique())
    df_filtrado = df[df['Nombre'] == producto]

    # Mostrar los datos filtrados en una tabla
    st.dataframe(df_filtrado)

    # Crear un gráfico de línea del valor
    st.line_chart(df_filtrado['Valor'])

# Ejecutar la aplicación
if __name__ == '__main__':
    app()
