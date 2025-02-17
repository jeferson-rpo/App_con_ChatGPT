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

def cargar_datos_municipios():
    """
    Carga el archivo de municipios directamente desde la URL proporcionada.

    Returns:
        pd.DataFrame: DataFrame con los datos de municipios.
    """
    url_municipios = "https://raw.githubusercontent.com/jeferson-rpo/App_con_ChatGPT/refs/heads/main/DIVIPOLA-_C_digos_municipios_geolocalizados_20250217.csv"
    df_municipios = pd.read_csv(url_municipios)

    # Asegurarse de que los nombres de los municipios estén en el mismo formato (capitalización correcta)
    df_municipios['NOM_MPIO'] = df_municipios['NOM_MPIO'].str.title()  # Convierte a formato "Primera letra mayúscula"
    
    return df_municipios

def cargar_y_relacionar_datos():
    """
    Carga los datos de madera movilizada y los relaciona con los municipios.
    
    Returns:
        pd.DataFrame: DataFrame con los datos relacionados.
    """
    # Cargar el archivo de madera movilizada desde la URL o mediante carga manual
    df_madera = cargar_datos()
    
    # Cargar los datos de los municipios desde la URL
    df_municipios = cargar_datos_municipios()

    # Normalizar los nombres de los municipios en df_madera y df_municipios
    df_madera['MUNICIPIO'] = df_madera['MUNICIPIO'].str.title()  # Normaliza el nombre del municipio en df_madera

    # Relacionar los datos de madera movilizada con los municipios
    df_relacionado = df_madera.merge(df_municipios, how="left", left_on="MUNICIPIO", right_on="NOM_MPIO")
    
    return df_relacionado

# Llamar a la función para cargar y relacionar los datos
df_relacionado = cargar_y_relacionar_datos()

# Mostrar el DataFrame relacionado
st.write(df_relacionado)

