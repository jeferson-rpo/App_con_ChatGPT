# importar librerias 
import numpy as np
import streamlit as st
import pandas as pd  # Importar pandas

# Configurar la semilla para reproducibilidad (sustituye '123456789' por tu número de cédula)
np.random.seed(123456789)

# Simular el lanzamiento de un dado 20 veces
lanzamientos = np.random.randint(1, 7, 20)  # Valores entre 1 y 6, como un dado

# Calcular estadísticas
media = np.mean(lanzamientos)
mediana = np.median(lanzamientos)
varianza = np.var(lanzamientos)
desviacion_estandar = np.std(lanzamientos)

# Calcular la moda (la moda es el número más frecuente en un array)
valores_unicos, conteo = np.unique(lanzamientos, return_counts=True)
moda = valores_unicos[np.argmax(conteo)]

# Análisis de frecuencias
frecuencias = np.bincount(lanzamientos)[1:]  # Contar la frecuencia de cada número del 1 al 6

# Mostrar los resultados en Streamlit
st.title("Simulación de Lanzamiento de un Dado por Jeferson orley restrepo bedoya ")
st.write("Resultados de los lanzamientos de un dado 20 veces :")
st.write(f"<h3 style='font-size: 24px;'>Lanzamientos realizados:</h3>", unsafe_allow_html=True)
st.write(f"<h2 style='font-size: 28px;'>{lanzamientos}</h2>", unsafe_allow_html=True)

# Mostrar análisis estadístico con formato
st.write("<h3 style='font-size: 24px;'>Análisis estadístico de los lanzamientos:</h3>", unsafe_allow_html=True)
st.write(f"<h4 style='font-size: 20px;'>Media: {media:.2f}</h4>", unsafe_allow_html=True)
st.write(f"<h4 style='font-size: 20px;'>Mediana: {mediana}</h4>", unsafe_allow_html=True)
st.write(f"<h4 style='font-size: 20px;'>Moda: {moda}</h4>", unsafe_allow_html=True)
st.write(f"<h4 style='font-size: 20px;'>Varianza: {varianza:.2f}</h4>", unsafe_allow_html=True)
st.write(f"<h4 style='font-size: 20px;'>Desviación estándar: {desviacion_estandar:.2f}</h4>", unsafe_allow_html=True)

# Mostrar tabla de análisis de frecuencias con pandas
st.write("<h3 style='font-size: 24px;'>Frecuencias de cada número:</h3>", unsafe_allow_html=True)
tabla_frecuencias = pd.DataFrame({
    'Número de Dado': np.arange(1, 7),
    'Frecuencia': frecuencias
})
st.table(tabla_frecuencias)

# Instrucciones para correr la app en Streamlit
st.write("<h3 style='font-size: 18px;'>Instrucciones:</h3>", unsafe_allow_html=True)
st.write("Para ejecutar esta aplicación en Streamlit, guarda este archivo como `app.py` y usa el comando `streamlit run app.py` en tu terminal.")


