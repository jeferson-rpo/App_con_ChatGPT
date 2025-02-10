import seaborn as sns

# Crear un DataFrame con las correlaciones
correlation_df = pd.DataFrame({
    "Categoría": ["Global"] + list(correlation_por_genero.index) + list(correlation_por_frecuencia.index),
    "Correlación": [correlation_global] + list(correlation_por_genero.values) + list(correlation_por_frecuencia.values)
})

# Crear un mapa de colores para diferenciar las categorías
palette = ["blue"] + ["green"] * len(correlation_por_genero) + ["red"] * len(correlation_por_frecuencia)

# Crear la visualización mejorada
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Categoría", y="Correlación", data=correlation_df, palette=palette, ax=ax)

# Ajustar el título y etiquetas
ax.set_title("Correlación entre Edad e Ingreso Anual USD", fontsize=14)
ax.set_ylabel("Coeficiente de Correlación", fontsize=12)
ax.set_xlabel("Segmentación", fontsize=12)
ax.axhline(0, color='black', linestyle='dashed', linewidth=1)  # Línea en 0 para referencia

# Rotar etiquetas del eje X si hay muchas categorías
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Mostrar la gráfica en Streamlit
st.pyplot(fig)
