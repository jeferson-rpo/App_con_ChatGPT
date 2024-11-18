# El siguiente codigo fue realizado por chatgpt
import streamlit as st

# Funciones para las conversiones
def celsius_a_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def fahrenheit_a_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

def celsius_a_kelvin(celsius):
    return celsius + 273.15

def kelvin_a_celsius(kelvin):
    return kelvin - 273.15

def pies_a_metros(pies):
    return pies * 0.3048

def metros_a_pies(metros):
    return metros / 0.3048

def pulgadas_a_centimetros(pulgadas):
    return pulgadas * 2.54

def centimetros_a_pulgadas(centimetros):
    return centimetros / 2.54

def libras_a_kilogramos(libras):
    return libras * 0.453592

def kilogramos_a_libras(kilogramos):
    return kilogramos / 0.453592

def onzas_a_gramos(onzas):
    return onzas * 28.3495

def gramos_a_onzas(gramos):
    return gramos / 28.3495

def galones_a_litros(galones):
    return galones * 3.78541

def litros_a_galones(litros):
    return litros / 3.78541

def pulgadas_cubicas_a_centimetros_cubicos(pulgadas):
    return pulgadas * 16.387

def centimetros_cubicos_a_pulgadas_cubicas(centimetros):
    return centimetros / 16.387

def horas_a_minutos(horas):
    return horas * 60

def minutos_a_segundos(minutos):
    return minutos * 60

def dias_a_horas(dias):
    return dias * 24

def semanas_a_dias(semanas):
    return semanas * 7

def millas_por_hora_a_kilometros_por_hora(millas):
    return millas * 1.60934

def kilometros_por_hora_a_metros_por_segundo(kilometros):
    return kilometros / 3.6

def nudos_a_millas_por_hora(nudos):
    return nudos * 1.15078

def metros_por_segundo_a_pies_por_segundo(metros):
    return metros * 3.28084

def metros_cuadrados_a_pies_cuadrados(metros):
    return metros * 10.7639

def pies_cuadrados_a_metros_cuadrados(pies):
    return pies / 10.7639

def kilometros_cuadrados_a_millas_cuadradas(kilometros):
    return kilometros / 2.58999

def millas_cuadradas_a_kilometros_cuadrados(millas):
    return millas * 2.58999

def julios_a_calorias(julios):
    return julios * 0.239006

def calorias_a_kilojulios(calorias):
    return calorias / 239.006

def kilovatios_hora_a_megajulios(kwh):
    return kwh * 3.6

def megajulios_a_kilovatios_hora(mj):
    return mj / 3.6

def pascales_a_atmosferas(pascales):
    return pascales / 101325

def atmosferas_a_pascales(atm):
    return atm * 101325

def barras_a_libras_por_pulgada_cuadrada(barras):
    return barras * 14.5038

def libras_por_pulgada_cuadrada_a_bares(libras):
    return libras / 14.5038

def megabytes_a_gigabytes(mb):
    return mb / 1024

def gigabytes_a_terabytes(gb):
    return gb / 1024

def kilobytes_a_megabytes(kb):
    return kb / 1024

def terabytes_a_petabytes(tb):
    return tb / 1024

# Interfaz de usuario en Streamlit
st.title("Conversor Universal")
st.write("Selecciona una categoría y luego el tipo de conversión que deseas realizar.")

# Selección de categoría
categoria = st.selectbox(
    "Selecciona la categoría de conversión:",
    ("Temperatura", "Longitud", "Peso/Masa", "Volumen", "Tiempo", "Velocidad", "Área", "Energía", "Presión", "Tamaño de Datos")
)

# Conversión según la categoría seleccionada
if categoria == "Temperatura":
    tipo_conversion = st.selectbox(
        "Selecciona la conversión de temperatura:",
        ("Celsius a Fahrenheit", "Fahrenheit a Celsius", "Celsius a Kelvin", "Kelvin a Celsius")
    )
    valor = st.number_input("Introduce el valor a convertir:", format="%.2f")

    if tipo_conversion == "Celsius a Fahrenheit":
        st.write(f"{valor} °C = {celsius_a_fahrenheit(valor)} °F")
    elif tipo_conversion == "Fahrenheit a Celsius":
        st.write(f"{valor} °F = {fahrenheit_a_celsius(valor)} °C")
    elif tipo_conversion == "Celsius a Kelvin":
        st.write(f"{valor} °C = {celsius_a_kelvin(valor)} K")
    elif tipo_conversion == "Kelvin a Celsius":
        st.write(f"{valor} K = {kelvin_a_celsius(valor)} °C")

elif categoria == "Longitud":
    tipo_conversion = st.selectbox(
        "Selecciona la conversión de longitud:",
        ("Pies a metros", "Metros a pies", "Pulgadas a centímetros", "Centímetros a pulgadas")
    )
    valor = st.number_input("Introduce el valor a convertir:", format="%.2f")

    if tipo_conversion == "Pies a metros":
        st.write(f"{valor} pies = {pies_a_metros(valor)} metros")
    elif tipo_conversion == "Metros a pies":
        st.write(f"{valor} metros = {metros_a_pies(valor)} pies")
    elif tipo_conversion == "Pulgadas a centímetros":
        st.write(f"{valor} pulgadas = {pulgadas_a_centimetros(valor)} centímetros")
    elif tipo_conversion == "Centímetros a pulgadas":
        st.write(f"{valor} centímetros = {centimetros_a_pulgadas(valor)} pulgadas")

elif categoria == "Peso/Masa":
    tipo_conversion = st.selectbox(
        "Selecciona la conversión de peso/masa:",
        ("Libras a kilogramos", "Kilogramos a libras", "Onzas a gramos", "Gramos a onzas")
    )
    valor = st.number_input("Introduce el valor a convertir:", format="%.2f")

    if tipo_conversion == "Libras a kilogramos":
        st.write(f"{valor} libras = {libras_a_kilogramos(valor)} kg")
    elif tipo_conversion == "Kilogramos a libras":
        st.write(f"{valor} kg = {kilogramos_a_libras(valor)} libras")
    elif tipo_conversion == "Onzas a gramos":
        st.write(f"{valor} onzas = {onzas_a_gramos(valor)} gramos")
    elif tipo_conversion == "Gramos a onzas":
        st.write(f"{valor} gramos = {gramos_a_onzas(valor)} onzas")

# Puedes continuar agregando las conversiones para las demás categorías (Volumen, Tiempo, Velocidad, etc.)


