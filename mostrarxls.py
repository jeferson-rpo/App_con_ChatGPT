import pandas as pd
import re
import streamlit as st

# Función para extraer información de una línea con regex
def extraer_info(linea):
    # Patrones definidos para cada tipo de dato
    patron_serie = r"^\d+-\d+"  # Ejemplo: 1234-5678 (ajusta si es necesario)
    patron_nombre = r"[A-Z][a-z]+"
    patron_email = r"\S+@\S+"
    patron_telefono = r"\+\d+"
    patron_fecha = r"\d{2}/\d{2}/\d{2}"
    patron_valor = r"\d+(\.\d+)?$"

    # Inicializar variables
    serie = ""
    nombre = ""
    email = ""
    telefono = ""
    fecha = ""
    valor = ""

    # Dividir la línea en palabras
    palabras = linea.split()

    # Iterar sobre las palabras y aplicar los patrones
    for palabra in palabras:
        if re.match(patron_serie, palabra):
            serie = palabra
        elif re.match(patron_nombre, palabra):
            nombre += f" {palabra}"
        elif re.match(patron_email, palabra):
            email = palabra
        elif re.match(patron_telefono, palabra):
            telefono = palabra
        elif re.match(patron_fecha, palabra):
            fecha = palabra
        elif re.match(patron_valor, palabra):
            valor = palabra

    return [serie, nombre.strip(), valor, fecha, f"{email} {telefono}".strip()]

# Streamlit: configuración inicial
st.title("Organizador de Datos con Regex")
st.write("Esta aplicación organiza datos de un archivo CSV utilizando expresiones regulares.")

# Leer y procesar el archivo CSV
nombre_archivo_csv = "regex_productos.csv"

try:
    # Leer el archivo
    with open(nombre_archivo_csv, "r") as file:
        lineas = file.readlines()

    # Procesar cada línea y extraer la información
    datos = [extraer_info(linea) for linea in lineas]

    # Crear un DataFrame
    columnas = ["Número de serie", "Nombre del producto", "Valor", "Fecha de compra", "Información de contacto"]
    df = pd.DataFrame(datos, columns=columnas)

    # Mostrar los datos organizados
    st.write("Datos organizados:")
    st.dataframe(df)

    # Guardar los datos en un archivo Excel
    nombre_archivo_excel = "productos_organizados.xls"
    df.to_excel(nombre_archivo_excel, index=False)

    # Descargar el archivo Excel
    with open(nombre_archivo_excel, "rb") as file:
        st.download_button(
            label="Descargar archivo organizado en Excel",
            data=file,
            file_name=nombre_archivo_excel,
            mime="application/vnd.ms-excel",
        )

except FileNotFoundError:
    st.error(f"El archivo '{nombre_archivo_csv}' no se encontró. Asegúrate de que esté en el directorio actual.")
except Exception as e:
    st.error(f"Error al procesar el archivo: {e}")
