# Este codigo fue realizado por chatgpt
import streamlit as st
import pandas as pd
import datetime

# Función para inicializar los datos si no existen en el estado de la sesión
def inicializar_datos():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"])

# Función para registrar ingresos y gastos
def registrar_transaccion(tipo, categoria, monto, descripcion, fecha):
    # Asegurarse de que la fecha sea del tipo correcto
    fecha = pd.to_datetime(fecha)
    nueva_fila = pd.DataFrame({"Fecha": [fecha], "Tipo": [tipo], "Categoría": [categoria],
                               "Monto": [monto], "Descripción": [descripcion]})
    st.session_state.df = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)

# Función para generar el reporte semanal
def generar_reporte_semanal(fecha_elegida):
    semana_inicio = fecha_elegida - pd.DateOffset(days=fecha_elegida.weekday())  # Lunes de la semana seleccionada
    
    # Convertir la columna "Fecha" a tipo datetime para evitar errores de comparación
    st.session_state.df["Fecha"] = pd.to_datetime(st.session_state.df["Fecha"])
    
    # Filtrar los registros de la semana
    df_semana = st.session_state.df[st.session_state.df["Fecha"] >= semana_inicio]
    gastos_semanales = df_semana[df_semana["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos_semanales = df_semana[df_semana["Tipo"] == "Ingreso"]["Monto"].sum()
    diferencia_semanal = ingresos_semanales - gastos_semanales
    return df_semana, gastos_semanales, ingresos_semanales, diferencia_semanal

# Función para generar el reporte mensual
def generar_reporte_mensual(fecha_elegida):
    mes_inicio = fecha_elegida.replace(day=1)  # Primer día del mes
    
    # Convertir la columna "Fecha" a tipo datetime para evitar errores de comparación
    st.session_state.df["Fecha"] = pd.to_datetime(st.session_state.df["Fecha"])
    
    df_mes = st.session_state.df[st.session_state.df["Fecha"] >= mes_inicio]
    gastos_mensuales = df_mes[df_mes["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos_mensuales = df_mes[df_mes["Tipo"] == "Ingreso"]["Monto"].sum()
    diferencia_mensual = ingresos_mensuales - gastos_mensuales
    return df_mes, gastos_mensuales, ingresos_mensuales, diferencia_mensual

# Interfaz de usuario en Streamlit
st.title("Registro de Finanzas Personales")

# Inicializar el DataFrame vacío si no existe en session_state
inicializar_datos()

# Registrar Ingresos o Gastos
st.header("Registrar Transacción")
tipo_transaccion = st.selectbox("Tipo de Transacción:", ["Ingreso", "Gasto"])
categoria_transaccion = st.text_input("Categoría (Ej. Alimentación, Renta, Entretenimiento):")
monto_transaccion = st.number_input("Monto:", min_value=0.0, format="%.2f")
descripcion_transaccion = st.text_area("Descripción:")

# Nueva opción para ingresar la fecha de la transacción
fecha_transaccion = st.date_input("Fecha de la Transacción", datetime.date.today())

if st.button("Registrar Transacción"):
    if categoria_transaccion and monto_transaccion > 0:
        registrar_transaccion(tipo_transaccion, categoria_transaccion, monto_transaccion, descripcion_transaccion, fecha_transaccion)
        st.success(f"Transacción de {tipo_transaccion} registrada con éxito!")
    else:
        st.error("Por favor, completa todos los campos correctamente.")

# Mostrar los registros de ingresos y gastos
st.header("Historial de Finanzas")
st.write(st.session_state.df)

# Selección de la fecha para los reportes
st.header("Generar Reportes")
fecha_seleccionada = st.date_input("Selecciona la Fecha para el reporte", datetime.date.today())
fecha_elegida = pd.to_datetime(fecha_seleccionada)  # Convierte la fecha seleccionada a datetime

# Reporte Semanal
st.subheader("Reporte Semanal")
df_semanal, gastos_semanales, ingresos_semanales, diferencia_semanal = generar_reporte_semanal(fecha_elegida)

# Mostrar el reporte semanal
st.write("### Transacciones de la Semana")
st.write(df_semanal)  # Muestra las transacciones de la semana en una tabla

# Mostrar los resultados de la comparación
st.write(f"Total de Ingresos Semanales: ${ingresos_semanales:.2f}")
st.write(f"Total de Gastos Semanales: ${gastos_semanales:.2f}")
st.write(f"Diferencia Semanal (Ingresos - Gastos): ${diferencia_semanal:.2f}")

# Reporte Mensual
st.subheader("Reporte Mensual")
df_mensual, gastos_mensuales, ingresos_mensuales, diferencia_mensual = generar_reporte_mensual(fecha_elegida)

# Mostrar el reporte mensual
st.write("### Transacciones del Mes")
st.write(df_mensual)  # Muestra las transacciones del mes en una tabla

# Mostrar los resultados de la comparación mensual
st.write(f"Total de Ingresos Mensuales: ${ingresos_mensuales:.2f}")
st.write(f"Total de Gastos Mensuales: ${gastos_mensuales:.2f}")
st.write(f"Diferencia Mensual (Ingresos - Gastos): ${diferencia_mensual:.2f}")


