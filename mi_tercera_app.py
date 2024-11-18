# Este codigo fue realizado por chatgpt

import streamlit as st
import pandas as pd

# Datos en memoria
transacciones = []

# Título de la aplicación
st.title("Registro de Finanzas Personales")

# Selección de fecha
fecha = st.date_input("Selecciona una fecha")

# Selección de tipo de transacción
tipo = st.selectbox("Selecciona el tipo de transacción", ["Ingreso", "Gasto"])

# Entrada de monto
monto = st.number_input("Ingresa el monto", min_value=0.0, format="%.2f")

# Botón para agregar transacción
if st.button("Agregar Transacción"):
    nueva_transaccion = {"Fecha": fecha, "Tipo": tipo, "Monto": monto}
    transacciones.append(nueva_transaccion)
    st.success("Transacción agregada correctamente.")

# Mostrar las transacciones registradas
if transacciones:
    st.subheader("Transacciones Registradas")
    df = pd.DataFrame(transacciones)
    st.dataframe(df)

# Reporte semanal y mensual
if transacciones:
    st.subheader("Reporte de Diferencias")
    df = pd.DataFrame(transacciones)
    ingreso_total = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
    gasto_total = df[df["Tipo"] == "Gasto"]["Monto"].sum()
    st.write(f"**Total Ingresos:** ${ingreso_total:.2f}")
    st.write(f"**Total Gastos:** ${gasto_total:.2f}")
    st.write(f"**Balance:** ${ingreso_total - gasto_total:.2f}")

