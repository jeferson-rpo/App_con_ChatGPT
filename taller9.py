import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Opción para que el usuario ingrese una URL o suba un archivo
opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

# Si elige "Cargar archivo desde URL"
if opcion == "Cargar archivo desde URL":
    url = st.text_input("Introduce la URL del archivo CSV",
                        "https://github.com/gabrielawad/programacion-para-ingenieria/raw/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv")
    if url:
        gdf = pd.read_csv(url)
        st.write("Datos cargados desde la URL:", gdf)

# Si elige "Subir archivo"
if opcion == "Subir archivo":
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo:
        gdf = pd.read_csv(archivo)
        st.write("Datos cargados:", gdf)

# Limpiar los datos si se cargaron
if 'gdf' in locals():
    st.write("NaN en las columnas:", gdf.isna().sum())

    # Rellenar NaN en 'Ingreso_Anual_USD' con el promedio
    gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(gdf['Ingreso_Anual_USD'].mean())

    # Rellenar NaN en 'Edad' con el valor entero más cercano al promedio
    gdf['Edad'] = gdf['Edad'].fillna(round(gdf['Edad'].mean()))

    # Rellenar NaN en 'Historial_Compras' con el valor entero más cercano al promedio
    gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(round(gdf['Historial_Compras'].mean()))

    # Rellenar NaN en 'Latitud' y 'Longitud' usando la correlación con 'Ingreso_Anual_USD'
    gdf['Latitud'] = gdf['Latitud'].fillna(gdf['Ingreso_Anual_USD'].corr(gdf['Latitud']) * gdf['Ingreso_Anual_USD'])
    gdf['Longitud'] = gdf['Longitud'].fillna(gdf['Ingreso_Anual_USD'].corr(gdf['Longitud']) * gdf['Ingreso_Anual_USD'])

    # Imputar 'Frecuencia_Compra' usando la relación con 'Edad'
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].fillna(gdf['Edad'] * 0.1)

    # Imputar 'Nombre' y 'Género' con los valores más frecuentes
    gdf['Nombre'] = gdf['Nombre'].fillna(gdf['Nombre'].mode()[0])
    gdf['Género'] = gdf['Género'].fillna(gdf['Género'].mode()[0])

    # Convertir 'Frecuencia_Compra' a valores numéricos y luego de regreso a etiquetas
    frec_map = {"Baja": 0, "Media": 1, "Alta": 2}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map).fillna(1)
    frec_map_inv = {0: "Baja", 1: "Media", 2: "Alta"}
    gdf['Frecuencia_Compra'] = gdf['Frecuencia_Compra'].map(frec_map_inv)

    st.write("Datos después de la limpieza:", gdf)

    # --- ANÁLISIS DE CORRELACIÓN ---
    
    # Correlación global entre Edad e Ingreso Anual USD
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write(f"Correlación global entre Edad e Ingreso Anual USD: {correlation_global:.2f}")

    # Correlación segmentada por Género
    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Género:", correlation_por_genero)

    # Correlación segmentada por Frecuencia de Compra
    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().unstack().iloc[:, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Frecuencia de Compra:", correlation_por_frecuencia)

    # --- VISUALIZACIÓN DE RESULTADOS ---
    
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
