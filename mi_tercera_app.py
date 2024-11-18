# Este codigo fue realizado por chatgpt

import streamlit as st
import pandas as pd
import datetime
import os

# Función para cargar los datos, crear un DataFrame vacío si no existe el archivo
def cargar_datos():
    if os.path.exists("finanzas.csv"):
        df = pd.read_csv("finanzas.csv")
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")  # Convertir la columna 'Fecha' a datetime
    else:
        df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"])
    return df

# Función para guardar los datos en el archivo CSV
def guardar_datos(df):
    df.to_csv("finanzas.csv", index=False)

# Función para registrar ingresos y gastos
def registrar_transaccion(df, tipo, categoria, monto, descripcion):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nueva_fila = pd.DataFrame({"Fecha": [fecha], "Tipo": [tipo], "Categoría": [categoria],
                               "Monto": [monto], "Descripción": [descripcion]})
    df = pd.concat([df, nueva_fila], ignore_index=True)
    guardar_datos(df)  # Guardar los cambios en el archivo CSV
    return df

# Función para generar el reporte semanal
def generar_reporte_semanal(df):
    fecha_hoy = datetime.datetime.now()
    semana_inicio = fecha_hoy - pd.DateOffset(days=fecha_hoy.weekday())  # Lunes de la semana actual
    # Filtrar los registros de la semana
    df_semana = df[df["Fecha"] >= semana_inicio]
    gastos_semanales = df_semana[df_semana["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos_semanales = df_semana[df_semana["Tipo"] == "Ingreso"]["Monto"].sum()
    diferencia_semanal = ingresos_semanales - gastos_semanales
    return gastos_semanales, ingresos_semanales, diferencia_semanal

# Interfaz de usuario en Streamlit
st.title("Registro de Finanzas Personales")

# Cargar los datos de las finanzas
df = cargar_datos()

# Registrar Ingresos o Gastos
st.header("Registrar Transacción")
tipo_transaccion = st.selectbox("Tipo de Transacción:", ["Ingreso", "Gasto"])
categoria_transaccion = st.text_input("Categoría (Ej. Alimentación, Renta, Entretenimiento):")
monto_transaccion = st.number_input("Monto:", min_value=0.0, format="%.2f")
descripcion_transaccion = st.text_area("Descripción:")
if st.button("Registrar Transacción"):
    if categoria_transaccion and monto_transaccion > 0:
        df = registrar_transaccion(df, tipo_transaccion, categoria_transaccion, monto_transaccion, descripcion_transaccion)
        st.success(f"Transacción de {tipo_transaccion} registrada con éxito!")
    else:
        st.error("Por favor, completa todos los campos correctamente.")

# Mostrar los registros de ingresos y gastos
st.header("Historial de Finanzas")
st.write(df)

# Reporte Semanal
st.header("Reporte Semanal")
gastos_semanales, ingresos_semanales, diferencia_semanal = generar_reporte_semanal(df)

# Mostrar resultados del reporte semanal
st.write(f"Total de Ingresos Semanales: ${ingresos_semanales:.2f}")
st.write(f"Total de Gastos Semanales: ${gastos_semanales:.2f}")
st.write(f"Diferencia Semanal (Ingresos - Gastos): ${diferencia_semanal:.2f}")

# Establecer Presupuestos Mensuales y Metas de Ahorro
st.header("Presupuesto y Meta de Ahorro")
presupuesto_categoria = st.text_input("Categoría del Presupuesto (Ej. Alimentación, Renta):")
presupuesto_monto = st.number_input("Monto del Presupuesto:", min_value=0.0, format="%.2f")
meta_ahorro = st.number_input("Meta de Ahorro Mensual:", min_value=0.0, format="%.2f")
if st.button("Guardar Presupuesto y Meta"):
    if presupuesto_categoria and presupuesto_monto > 0:
        st.success(f"Presupuesto para {presupuesto_categoria} de {presupuesto_monto} guardado correctamente.")
    else:
        st.error("Por favor, ingresa una categoría y monto válidos.")

# Reporte Mensual
st.header("Reporte Mensual")
fecha_hoy = datetime.datetime.now()
mes_inicio = fecha_hoy.replace(day=1)  # Primer día del mes
df_mes = df[df["Fecha"] >= mes_inicio]
gastos_mensuales = df_mes[df_mes["Tipo"] == "Gasto"]["Monto"].sum()
ingresos_mensuales = df_mes[df_mes["Tipo"] == "Ingreso"]["Monto"].sum()
diferencia_mensual = ingresos_mensuales - gastos_mensuales
st.write(f"Total de Ingresos Mensuales: ${ingresos_mensuales:.2f}")
st.write(f"Total de Gastos Mensuales: ${gastos_mensuales:.2f}")
st.write(f"Diferencia Mensual (Ingresos - Gastos): ${diferencia_mensual:.2f}")


