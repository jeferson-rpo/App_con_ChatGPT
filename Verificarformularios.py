#Este codigo fue realizado con geminis

#librerias necesarias
import streamlit as st
import re

def validar_nombre(nombre):
    """Valida si un nombre solo contiene caracteres alfabéticos e inicia con mayúscula."""
    patron = r"^[A-Z][a-zA-Z]+$"
    return re.match(patron, nombre)

def validar_email(email):
    """Valida una dirección de correo electrónico."""
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email)

def validar_telefono(telefono):
    """Valida un número de teléfono (ejemplo: +54 11 1234-5678)."""
    patron = r"^\+\d{2} \d{2} \d{4}-\d{4}$"  # Ajusta el patrón según tu formato de teléfono
    return re.match(patron, telefono)

def validar_fecha(fecha):
    """Valida una fecha en formato DD/MM/AAAA."""
    patron = r"^\d{2}/\d{2}/\d{4}$"
    return re.match(patron, fecha)

# Título de la aplicación
st.title("Validador de Formularios")

# Campos del formulario
nombre = st.text_input("Ingrese su nombre")
email = st.text_input("Ingrese su correo electrónico")
telefono = st.text_input("Ingrese su número de teléfono")
fecha_nacimiento = st.text_input("Ingrese su fecha de nacimiento (DD/MM/AAAA)")

# Botón para validar
if st.button("Validar"):
    if not validar_nombre(nombre):
        st.error("El nombre debe contener solo letras y comenzar con mayúscula.")
    if not validar_email(email):
        st.error("El correo electrónico no es válido.")
    if not validar_telefono(telefono):
        st.error("El número de teléfono no es válido.")
    if not validar_fecha(fecha_nacimiento):
        st.error("La fecha de nacimiento no es válida. Use el formato DD/MM/AAAA.")
    else:
        st.success("¡Todos los datos son válidos!")
