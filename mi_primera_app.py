# El siguiente codigo fue utilizado con chat gpt
import streamlit as st

# Título de la app
st.title("Mi primera app")

# Autor de la app
st.write("Esta app fue elaborada por Jeferson Orley Restrepo Bedoya.")

# Preguntar el nombre del usuario
nombre_usuario = st.text_input("¿Cual es tu nombre?")

# Verificar si el nombre ha sido ingresado y mostrar mensaje de bienvenida
if nombre_usuario:
    st.write(f"{nombre_usuario}, te doy la bienvenida a mi primera app.")
