# importar librerias 
import numpy as np
import streamlit as st

import numpy as np
import streamlit as st
import pandas as pd  # Importar pandas

# Configurar la semilla para reproducibilidad 
np.random.seed(1036678356)

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
st.title("Simulación de Lanzamiento de un Dado")
st.write("Resultados de los lanzamientos:")
st.write(lanzamientos)

st.write("Análisis estadístico:")
st.write(f"Media: {media:.2f}")
st.write(f"Mediana: {mediana}")
st.write(f"Moda: {moda}")
st.write(f"Varianza: {varianza:.2f}")
st.write(f"Desviación estándar: {desviacion_estandar:.2f}")

# Mostrar tabla de análisis de frecuencias con pandas
st.write("Frecuencias de cada número:")
tabla_frecuencias = pd.DataFrame({
    'Número de Dado': np.arange(1, 7),
    'Frecuencia': frecuencias
})
st.table(tabla_frecuencias)




