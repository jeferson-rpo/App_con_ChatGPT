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

def validar_telefono_colombia(telefono):
    """Valida un número de teléfono colombiano sin prefijo internacional."""
    patron = r"^\d{10}$"
    return re.match(patron, telefono)

def validar_fecha(fecha):
    """Valida una fecha en formato DD/MM/AAAA, considerando rangos válidos."""
    patron = r"^(0[1-9]|1[0-9]|2[0-9]|3[01])/(0[1-9]|1[0-2])/((19[2-9]\d)|(20[0-2]\d|2024))$"
    return re.match(patron, fecha)

# Título de la aplicación
st.title("Validador de Formularios Colombianos por Jeferson Orley Restrepo Bedoya")

# Campos del formulario
nombre = st.text_input("Ingrese su nombre")
email = st.text_input("Ingrese su correo electrónico")
telefono = st.text_input("Ingrese su número de teléfono (10 dígitos)")
fecha_nacimiento = st.text_input("Ingrese su fecha de nacimiento (DD/MM/AAAA)")

# Botón para validar
if st.button("Validar"):
    if not validar_nombre(nombre):
        st.error("El nombre debe contener solo letras y comenzar con mayúscula.")
    if not validar_email(email):
        st.error("El correo electrónico no es válido.")
    if not validar_telefono_colombia(telefono):
        st.error("El número de teléfono debe tener 10 dígitos y ser válido para Colombia.")
    if not validar_fecha(fecha_nacimiento):
        st.error("La fecha de nacimiento no es válida. Use el formato DD/MM/AAAA y asegúrese de que esté dentro del rango permitido.")
    else:
        st.success("¡Todos los datos son válidos!")