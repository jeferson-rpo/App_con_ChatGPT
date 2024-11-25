import pandas as pd
import re
import streamlit as st

# Función mejorada para extraer información de una línea con regex
def extraer_info(linea):
    # Patrones definidos para cada tipo de dato
    patron_serie = r"\b\d{6}\b"  # Exactamente 6 dígitos
    patron_nombre = r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)*"  # Nombre compuesto
    patron_email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    patron_telefono = r"\+\d{1,4}\s?\d{6,}"  # +57 123456 o similar
    patron_fecha = r"\d{2}/\d{2}/\d{2}"
    patron_valor = r"\d+\.\d+"  # Números con punto decimal (ej: 123.45)

    # Extraer información usando regex
    serie = re.search(patron_serie, linea)
    nombre = re.search(patron_nombre, linea)
    email = re.search(patron_email, linea)
    telefono = re.search(patron_telefono, linea)
    fecha = re.search(patron_fecha, linea)
    valor = re.search(patron_valor, linea)

    # Manejar valores extraídos y convertir None a ""
    return [
        serie.group() if serie else "",
        nombre.group() if nombre else "",
        valor.group() if valor else "",
        fecha.group() if fecha else "",
        email.group() if email else "",
        telefono.group() if telefono else ""
    ]

# Streamlit: configuración inicial
st.title("Organizador de Datos con Regex Mejorado")
st.write("Esta aplicación organiza datos de un archivo CSV utilizando expresiones regulares Por Jeferson Orley Restrepo Bedoya.")

# Leer y procesar el archivo CSV
nombre_archivo_csv = "regex_productos.csv"

try:
    # Leer el archivo
    with open(nombre_archivo_csv, "r") as file:
        lineas = file.readlines()

    # Procesar cada
")

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
