# Este codigo fue realizado por chatgpt

import streamlit as st
import pandas as pd
import datetime

# Función para calcular la diferencia entre lo presupuestado y lo real
def calcular_diferencia(presupuestado, real):
    return presupuestado - real

# Función para cargar o crear un DataFrame para los registros de finanzas
def cargar_datos():
    try:
        df = pd.read_csv("finanzas.csv")
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo
        df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"])
    return df

# Función para guardar los datos en un archivo CSV
def guardar_datos(df):
    df.to_csv("finanzas.csv", index=False)

# Función para registrar ingresos y gastos
def registrar_transaccion(df, tipo, categoria, monto, descripcion):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nueva_fila = pd.DataFrame({"Fecha": [fecha], "Tipo": [tipo], "Categoría": [categoria],
                               "Monto": [monto], "Descripción": [descripcion]})
    df = pd.concat([df, nueva_fila], ignore_index=True)
    guardar_datos(df)
    return df

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

# Reportes Semanales y Mensuales
st.header("Reportes de Finanzas")

# Convertir la columna "Fecha" a tipo datetime
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# Validar que no haya fechas inválidas
if df["Fecha"].isnull().any():
    st.error("Se encontraron fechas no válidas en los registros. Verifica los datos.")
else:
    # Filtrar datos por fecha
    fecha_hoy = datetime.datetime.now()
    semana_inicio = fecha_hoy - pd.DateOffset(days=fecha_hoy.weekday())  # Lunes de la semana actual
    mes_inicio = fecha_hoy.replace(day=1)  # Primer día del mes

    # Filtrar los registros de la semana y el mes
    df_semana = df[df["Fecha"] >= semana_inicio]
    df_mes = df[df["Fecha"] >= mes_inicio]

    # Mostrar reportes de la semana
    st.subheader("Reporte Semanal")
    gastos_semanales = df_semana[df_semana["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos_semanales = df_semana[df_semana["Tipo"] == "Ingreso"]["Monto"].sum()
    diferencia_semanal = ingresos_semanales - gastos_semanales
    st.write(f"Total de Ingresos Semanales: ${ingresos_semanales:.2f}")
    st.write(f"Total de Gastos Semanales: ${gastos_semanales:.2f}")
    st.write(f"Diferencia Semanal (Ingresos - Gastos): ${diferencia_semanal:.2f}")

    # Mostrar reportes del mes
    st.subheader("Reporte Mensual")
    gastos_mensuales = df_mes[df_mes["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos_mensuales = df_mes[df_mes["Tipo"] == "Ingreso"]["Monto"].sum()
    diferencia_mensual = ingresos_mensuales - gastos_mensuales
    st.write(f"Total de Ingresos Mensuales: ${ingresos_mensuales:.2f}")
    st.write(f"Total de Gastos Mensuales: ${gastos_mensuales:.2f}")
    st.write(f"Diferencia Mensual (Ingresos - Gastos): ${diferencia_mensual:.2f}")

    # Comparar lo presupuestado con lo real
    if presupuesto_categoria and presupuesto_monto > 0:
        st.write(f"Presupuesto para {presupuesto_categoria}: ${presupuesto_monto:.2f}")
        diferencia_presupuesto = presupuesto_monto - gastos_mensuales
        st.write(f"Diferencia entre lo presupuestado y lo real: ${diferencia_presupuesto:.2f}")

    # Meta de ahorro
    st.subheader("Meta de Ahorro")
    if meta_ahorro > 0:
        ahorro_real = ingresos_mensuales - gastos_mensuales
        st.write(f"Meta de Ahorro Mensual: ${meta_ahorro:.2f}")
        st.write(f"Ahorro Real Mensual: ${ahorro_real:.2f}")
        if ahorro_real >= meta_ahorro:
            st.success("¡Felicidades! Has alcanzado tu meta de ahorro mensual.")
        else:
            st.warning(f"Te falta ${meta_ahorro - ahorro_real:.2f} para alcanzar tu meta de ahorro.")



