import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

def cargar_y_relacionar_datos():
    """
    Carga los datos de dos fuentes y realiza la relación entre los municipios.
    
    Returns:
        pd.DataFrame: DataFrame con los datos relacionados.
    """
    # Cargar el primer archivo CSV (madera movilizada)
    df_madera = cargar_datos()
    
    # Cargar el segundo archivo CSV (con coordenadas y nombres de municipios)
    df_municipios = cargar_datos()

    # Asegurarse de que los nombres de municipios estén en el mismo formato (capitalización correcta)
    df_municipios['NOM_MPIO'] = df_municipios['NOM_MPIO'].str.title()  # Convierte a formato "Primera letra mayúscula"

    # Ahora puedes relacionar el DataFrame de madera movilizada con el de municipios, asumiendo que
    # ambos tienen una columna en común, por ejemplo, 'NOM_MPIO'.
    df_relacionado = df_madera.merge(df_municipios, how="left", on="NOM_MPIO")
    
    return df_relacionado

# Llamar a la función para cargar y relacionar los datos
df_relacionado = cargar_y_relacionar_datos()

# Mostrar el DataFrame relacionado
st.write(df_relacionado)
