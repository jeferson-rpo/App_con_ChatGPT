# Realizar el análisis de correlación segmentado por 'Género'
correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Género:")
st.write(correlation_por_genero)

# Para extraer los valores de la correlación por género de manera correcta:
# En lugar de agrupar por 'Género', extraemos la correlación directamente
correlation_por_genero_values = correlation_por_genero.reset_index(level=0, drop=True)

# Realizar el análisis de correlación segmentado por 'Frecuencia_Compra'
correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Frecuencia de Compra:")
st.write(correlation_por_frecuencia)

# Para extraer los valores de la correlación por frecuencia de compra de manera correcta:
correlation_por_frecuencia_values = correlation_por_frecuencia.reset_index(level=0, drop=True)

# Visualización de los resultados
fig, ax = plt.subplots(figsize=(10, 6))

# Correlación global
ax.bar('Global', correlation_global, color='b', label='Global')

# Correlación por género
ax.bar(correlation_por_genero_values.index, correlation_por_genero_values, color='g', label='Por Género')

# Correlación por frecuencia de compra
ax.bar(correlation_por_frecuencia_values.index, correlation_por_frecuencia_values, color='r', label='Por Frecuencia de Compra')

ax.set_title("Correlación entre Edad e Ingreso Anual USD")
ax.set_ylabel("Correlación")
ax.legend(loc='best')
st.pyplot(fig)
