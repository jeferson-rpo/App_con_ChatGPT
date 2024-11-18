# Este codigo fue realizado por chatgpt

import streamlit as st
import pandas as pd
import datetime

# Función para inicializar los datos, sin guardar en CSV
def inicializar_datos():
    return pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"])

# Función para registrar ingresos y gastos
def registrar_transaccion(df, tipo, categoria, monto, descripcion):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nueva_fila = pd.DataFrame({"Fecha": [fecha], "Tipo": [tipo], "Categoría": [categoria],
                               "Monto": [monto], "Descripción": [descripcion]})
    df = pd.concat([df, nueva_fila], ignore_index=True)
    return df

# Función para generar el reporte semanal
def generar_reporte_semanal(df, fecha_elegida):
    semana_inicio = fecha_elegida - pd.DateOffset(days=fecha_elegida.weekday())  # Lunes de la semana seleccionada
    # Filtrar los registros de la semana
    df_semana = df[df["Fecha"] >= semana_inicio]
    gastos_semanales = df_semana[df_semana["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos_semanales = df_semana[df_semana["Tipo"] == "Ingreso"]["Monto"].sum()
    diferencia_semanal = ingresos_semanales - gastos_semanales
    return df_semana, gastos_semanales, ingresos_semanales, diferencia_semanal

# Función para generar el reporte mensual
def generar_reporte_mensual(df, fecha_elegida):
    mes_inicio = fecha_elegida.replace(day=1)  # Primer día del mes
    df_mes = df[df["Fecha"] >= mes_inicio]
    gastos_mensuales = df_mes[df_mes["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos_mensuales = df_mes[df_mes["Tipo"] == "Ingreso"]["Monto"].sum()
    diferencia_mensual = ingresos_mensuales - gastos_mensuales
    return df_mes, gastos_mensuales, ingresos_mensuales, diferencia_mensual

# Interfaz de usuario en Streamlit
st.title("Registro de Finanzas Personales")

# Inicializar el DataFrame vacío
df = inicializar_datos()

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

# Selección de la fecha para los reportes
st.header("Generar Reportes")
fecha_seleccionada = st.date_input("Selecciona la Fecha", datetime.date.today())
fecha_elegida = pd.to_datetime(fecha_seleccionada)

# Reporte Semanal
st.subheader("Reporte Semanal")
df_semanal, gastos_semanales, ingresos_semanales, diferencia_semanal = generar_reporte_semanal(df, fecha_elegida)

# Mostrar el reporte semanal
st.write("### Transacciones de la Semana")
st.write(df_semanal)  # Muestra las transacciones de la semana en una tabla

# Mostrar los resultados de la comparación
st.write(f"Total de Ingresos Semanales: ${ingresos_semanales:.2f}")
st.write(f"Total de Gastos Semanales: ${gastos_semanales:.2f}")
st.write(f"Diferencia Semanal (Ingresos - Gastos): ${diferencia_semanal:.2f}")

# Reporte Mensual
st.subheader("Reporte Mensual")
df_mensual, gastos_mensuales, ingresos_mensuales, diferencia_mensual = generar_reporte_mensual(df, fecha_elegida)

# Mostrar el reporte mensual
st.write("### Transacciones del Mes")
st.write(df_mensual)  # Muestra las transacciones del mes en una tabla

# Mostrar los resultados de la comparación mensual
st.write(f"Total de Ingresos Mensuales: ${ingresos_mensuales:.2f}")
st.write(f"Total de Gastos Mensuales: ${gastos_mensuales:.2f}")
st.write(f"Diferencia Mensual (Ingresos - Gastos): ${diferencia_mensual:.2f}")


