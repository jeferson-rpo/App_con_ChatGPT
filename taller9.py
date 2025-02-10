import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    # Identificar los NaN en el DataFrame
    st.write("NaN en las columnas:", gdf.isna().sum())

    # Rellenar NaN en 'Ingreso_Anual_USD' con el promedio de la columna
    promedio_ingreso = gdf['Ingreso_Anual_USD'].mean()
    gdf['Ingreso_Anual_USD'] = gdf['Ingreso_Anual_USD'].fillna(promedio_ingreso)

    # Rellenar NaN en 'Edad' con el valor entero más cercano al promedio
    promedio_edad = gdf['Edad'].mean()
    valor_entero_edad = round(promedio_edad)  # Redondear al entero más cercano
    gdf['Edad'] = gdf['Edad'].fillna(valor_entero_edad)

    # Rellenar NaN en 'Historial_Compras' con el valor entero más cercano al promedio
    promedio_historial = gdf['Historial_Compras'].mean()
    valor_entero_historial = round(promedio_historial)  # Redondear al entero más cercano
    gdf['Historial_Compras'] = gdf['Historial_Compras'].fillna(valor_entero_historial)

    # Rellenar NaN en 'Género' con el valor más frecuente
    genero_mas_frecuente = gdf['Género'].mode()[0]  # Obtiene el valor más frecuente
    gdf['Género'] = gdf['Género'].fillna(genero_mas_frecuente)

    # Verificar los valores únicos después de la limpieza
    st.write("Valores únicos en 'Género' después de la limpieza:", gdf['Género'].unique())

    # Realizar el análisis de correlación global entre 'Edad' e 'Ingreso_Anual_USD'
    correlation_global = gdf[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write(f"Correlación global entre Edad e Ingreso Anual USD: {correlation_global:.2f}")

    # Realizar el análisis de correlación segmentado por 'Género'
    correlation_por_genero = gdf.groupby('Género')[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Género:")
    st.write(correlation_por_genero)

    # Para extraer los valores de la correlación por género de manera correcta:
    correlation_por_genero_values = correlation_por_genero.groupby('Género').first()['Ingreso_Anual_USD']
    
    # Realizar el análisis de correlación segmentado por 'Frecuencia_Compra'
    correlation_por_frecuencia = gdf.groupby('Frecuencia_Compra')[['Edad', 'Ingreso_Anual_USD']].corr().iloc[0, 1]
    st.write("Correlación entre Edad e Ingreso Anual USD segmentado por Frecuencia de Compra:")
    st.write(correlation_por_frecuencia)

    # Para extraer los valores de la correlación por frecuencia de compra de manera correcta:
    correlation_por_frecuencia_values = correlation_por_frecuencia.groupby('Frecuencia_Compra').first()['Ingreso_Anual_USD']

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

    # Mostrar los datos después de la limpieza
    st.write("Datos después de la limpieza:", gdf)
