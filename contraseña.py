# Este codigo se realizo con la ayuda de geminis.

#Importar librerias necesarias.
import streamlit as st
import re

def evaluar_contrasena(contrasena, longitud_minima):
    """Evalúa la fortaleza de una contraseña utilizando expresiones regulares.

    Args:
        contrasena (str): La contraseña a evaluar.
        longitud_minima (int): La longitud mínima requerida para la contraseña.

    Returns:
        bool: True si la contraseña es segura, False en caso contrario.
    """

    # Patrones para cada criterio de seguridad
    patron_mayusculas = re.compile('[A-Z]')
    patron_minusculas = re.compile('[a-z]')
    patron_numeros = re.compile('\d')
    patron_especiales = re.compile('[^\w\s]')

    # Verificar si la contraseña cumple con todos los criterios
    if (
        len(contrasena) >= longitud_minima
        and patron_mayusculas.search(contrasena)
        and patron_minusculas.search(contrasena)
        and patron_numeros.search(contrasena)
        and patron_especiales.search(contrasena)
    ):
        return True
    else:
        return False

def sugerencias(contrasena, longitud_minima):
    """Proporciona sugerencias para mejorar la contraseña.

    Args:
        contrasena (str): La contraseña a evaluar.
        longitud_minima (int): La longitud mínima requerida para la contraseña.
    """

    sugerencias = []
    if len(contrasena) < longitud_minima:
        sugerencias.append(f"La contraseña debe tener al menos {longitud_minima} caracteres.")
    if not re.search('[A-Z]', contrasena):
        sugerencias.append("Incluye al menos una letra mayúscula.")
    if not re.search('[a-z]', contrasena):
        sugerencias.append("Incluye al menos una letra minúscula.")
    if not re.search('\d', contrasena):
        sugerencias.append("Incluye al menos un número.")
    if not re.search('[^\w\s]', contrasena):
        sugerencias.append("Incluye al menos un carácter especial.")

    if sugerencias:
        st.error("Tu contraseña no es lo suficientemente segura. Considera las siguientes sugerencias:")
        for sugerencia in sugerencias:
            st.write("- " + sugerencia)
    else:
        st.success("¡Excelente! Tu contraseña es muy segura.")

# Título de la aplicación
st.title("Evaluador de Contraseñas por Jeferson Orley Restrepo Bedoya")

# Barra lateral para personalizar la longitud mínima
st.sidebar.title("Opciones")
longitud_minima = st.sidebar.slider("Longitud mínima", min_value=8, max_value=20, value=8)

# Input para la contraseña
contrasena = st.text_input("Ingrese su contraseña")

# Botón para evaluar
if st.button("Evaluar"):
    sugerencias(contrasena, longitud_minima)
