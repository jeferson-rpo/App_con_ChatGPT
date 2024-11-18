import streamlit as st

# Funciones para las conversiones
def celsius_a_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_a_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

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

