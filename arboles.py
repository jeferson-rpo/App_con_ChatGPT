import streamlit as st
import pandas as pd

def cargar_datos():
    """
    Permite al usuario cargar un archivo CSV desde una URL o mediante carga manual.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.
    """
    opcion = st.radio("Selecciona una opción", ("Cargar archivo desde URL", "Subir archivo"))

    if opcion == "Cargar archivo desde URL":
        url = st.text_input("Ingresa la URL del archivo CSV")
        if url:
            return pd.read_csv(url)

    elif opcion == "Subir archivo":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            return pd.read_csv(archivo)

    return None

def analizar_especies(gdf):
    """
    Realiza el análisis de las especies más comunes a nivel país y por departamento.

    Args:
        gdf (pd.DataFrame): DataFrame con los datos de madera movilizada.
    """
    # Análisis de especies más comunes a nivel país
    especies_pais = gdf.groupby('ESPECIE')['VOLUMEN M3'].sum().reset_index()
    especies_pais = especies_pais.sort_values(by='VOLUMEN M3', ascending=False)

    st.subheader("Especies de madera más comunes a nivel país")
    st.write(especies_pais)

    # Seleccionar un departamento para el análisis
    depto_seleccionado = st.selectbox("Selecciona un departamento", gdf['DPTO'].unique())

    # Almacenar el departamento seleccionado en el estado de sesión
    if 'depto_seleccionado' not in st.session_state:
        st.session_state.depto_seleccionado = depto_seleccionado

    # Si el departamento cambia, actualizar el estado de sesión
    if st.session_state.depto_seleccionado != depto_seleccionado:
        st.session_state.depto_seleccionado = depto_seleccionado

    # Análisis de especies más comunes por departamento
    especies_depto = gdf[gdf['DPTO'] == st.session_state.depto_seleccionado]
    especies_depto = especies_depto.groupby('ESPECIE')['VOLUMEN M3'].sum().reset_index()
    especies_depto = especies_depto.sort_values(by='VOLUMEN M3', ascending=False)

    st.subheader(f"Especies de madera más comunes en {st.session_state.depto_seleccionado}")
    st.write(especies_depto)

st.title("Análisis de Madera Movilizada")

gdf = cargar_datos()

if gdf is not None:
    st.write("Datos cargados:", gdf)

    # Botón en la barra lateral para analizar especies
    if st.sidebar.button("Analizar Especies"):
        analizar_especies(gdf)
