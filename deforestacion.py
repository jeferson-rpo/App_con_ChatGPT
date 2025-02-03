import pandas as pd
import streamlit as st

# Cargar archivo CSV desde el usuario (usando Streamlit)
uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Leer el archivo CSV
    df = pd.read_csv(uploaded_file)

    # 1. Convertir columnas de fecha a formato datetime
    fechas = df.select_dtypes(include=['object'])  # Seleccionamos las columnas de tipo 'object' (posiblemente fechas)
    df[fechas.columns] = fechas.apply(pd.to_datetime, errors='coerce')  # Convertimos esas columnas a formato datetime

    # 2. Interpolación lineal para todas las columnas numéricas y de fechas
    df = df.apply(pd.to_numeric, errors='coerce')  # Convertimos todas las columnas posibles a tipo numérico
    df = df.interpolate()  # Realizamos la interpolación de los NaN para todas las columnas numéricas

    # 3. Rellenar NaN en columnas numéricas con la media de cada columna
    numericas = df.select_dtypes(include=['float64', 'int64'])  # Seleccionamos las columnas numéricas
    df[numericas.columns] = numericas.fillna(numericas.mean())  # Rellenamos los NaN con la media de cada columna numérica

    # 4. Rellenar NaN en columnas categóricas con el valor más frecuente
    categoricas = df.select_dtypes(include=['object'])  # Seleccionamos las columnas de tipo 'object' (categóricas)
    df[categoricas.columns] = categoricas.apply(lambda x: x.fillna(x.mode()[0]), axis=0)

    # Mostrar el DataFrame limpio
    st.write("Archivo limpio:", df)
