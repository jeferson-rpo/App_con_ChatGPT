# importar librerias 
import numpy as np
import matplotlib.pyplot as plt

# Configurar la semilla para reproducibilidad
np.random.seed(1036678356)  # Sustituye con tu número de cédula

# Simular el lanzamiento de un dado 20 veces
lanzamientos = np.random.randint(1, 7, 20)  # Valores entre 1 y 6, como un dado

# Crear una tabla de resultados (datos en orden)
print("Resultados de los lanzamientos de un dado 20 veces:")
for i, resultado in enumerate(lanzamientos, 1):
    print(f"Lanzamiento {i}: {resultado}")

# Calcular estadísticas
media = np.mean(lanzamientos)
mediana = np.median(lanzamientos)
varianza = np.var(lanzamientos)
desviacion_estandar = np.std(lanzamientos)

# Calcular la moda
valores_unicos, conteo = np.unique(lanzamientos, return_counts=True)
moda = valores_unicos[np.argmax(conteo)]

# Calcular frecuencias de cada número de dado
frecuencias = np.bincount(lanzamientos)[1:]  # Contar frecuencia de cada número del 1 al 6

# Mostrar estadísticas y tabla de análisis de frecuencias
print("\nAnálisis estadístico de los resultados:")
print(f"Media: {media:.2f}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")
print(f"Varianza: {varianza:.2f}")
print(f"Desviación estándar: {desviacion_estandar:.2f}")

print("\nFrecuencias de cada número (1 a 6):")
print("Número | Frecuencia")
for i in range(1, 7):
    print(f"   {i}   |    {frecuencias[i - 1]}")





