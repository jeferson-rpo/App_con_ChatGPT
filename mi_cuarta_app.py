# Este documento fue realizado por chatgpt

import streamlit as st
import pandas as pd
import io

# Función para calcular el PAPA
def calcular_papa(df):
    # Verificar si hay datos en el DataFrame
    if df.empty:
        return 0.0

    # Calcular el total de créditos y la suma ponderada de calificación por créditos
    total_creditos = df["Créditos"].sum()
    if total_creditos == 0:
        return 0.0

    suma_ponderada = (df["Calificación"] * df["Créditos"]).sum()
    papa = suma_ponderada / total_creditos
    return papa

# Función para calcular el PAPA por tipología de asignatura
def calcular_papa_por_tipologia(df, tipologia):
    # Filtrar las asignaturas por tipología
    df_tipologia = df[df["Tipología"] == tipologia]
    return calcular_papa(df_tipologia)

# Función para exportar los datos a CSV
def exportar_a_csv(df, papa_global, papa_por_tipologia):
    # Añadir los resultados del PAPA al DataFrame
    resultados = pd.DataFrame({
        "Resultado": ["PAPA Global"] + [f"PAPA {tipologia}" for tipologia in papa_por_tipologia.keys()],
        "Valor": [papa_global] + list(papa_por_tipologia.values())
    })
    
    # Crear un buffer en memoria y guardar el DataFrame como CSV
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)

    # Añadir los resultados del PAPA al archivo CSV
    resultados_buf = io.StringIO()
    resultados.to_csv(resultados_buf, index=False)
    resultados_buf.seek(0)
    
    return buf, resultados_buf

# Interfaz de usuario en Streamlit
st.title("Cálculo del PAPA - Promedio Ponderado Acumulado por Jeferson Orley Restrepo Bedoya")
st.write("Ingrese los datos de las asignaturas para calcular su PAPA global y por tipología.")

# Crear un DataFrame vacío para almacenar los datos
df = pd.DataFrame(columns=["Materia", "Calificación", "Créditos", "Tipología"])

# Ingreso de materias y sus calificaciones, créditos y tipología
materias = []
calificaciones = []
creditos = []
tipologias = []

n_materias = st.number_input("Número de materias a ingresar:", min_value=1, max_value=20, value=1)

for i in range(n_materias):
    st.subheader(f"Materia {i+1}")
    materia = st.text_input(f"Nombre de la materia {i+1}", key=f"materia_{i}")
    calificacion = st.number_input(f"Calificación de {materia} (0-10)", min_value=0.0, max_value=10.0, format="%.1f", key=f"calificacion_{i}")
    credito = st.number_input(f"Créditos de {materia}", min_value=1, max_value=6, value=3, key=f"credito_{i}")
    tipologia = st.selectbox(f"Tipología de {materia}", options=["Libre eleccion", "Disciplinar optaviva", "Disciplinar Obligatoria","Fundamental Obligatoria","Fundamental Obligatoria"], key=f"tipologia_{i}")
    
    # Validaciones antes de agregar los datos
    if calificacion > 0 and credito > 0:
        materias.append(materia)
        calificaciones.append(calificacion)
        creditos.append(credito)
        tipologias.append(tipologia)

# Almacenar los datos en el DataFrame
df = pd.DataFrame({
    "Materia": materias,
    "Calificación": calificaciones,
    "Créditos": creditos,
    "Tipología": tipologias
})

# Botón para calcular el PAPA global y por tipología
if st.button("Calcular PAPA"):
    if df.empty:
        st.error("No hay datos para calcular el PAPA. Por favor, ingrese al menos una materia.")
    else:
        # Calcular PAPA global
        papa_global = calcular_papa(df)
        st.write(f"**PAPA Global:** {papa_global:.2f}")
        
        # Calcular PAPA por tipología
        papa_por_tipologia = {}
        for tipologia in df["Tipología"].unique():
            papa_tipologia = calcular_papa_por_tipologia(df, tipologia)
            papa_por_tipologia[tipologia] = papa_tipologia
            st.write(f"**PAPA para asignaturas de tipo {tipologia}:** {papa_tipologia:.2f}")
        
        # Mostrar los datos ingresados en una tabla
        st.subheader("Datos Ingresados")
        st.write(df)

        # Exportar a CSV
        buf, resultados_buf = exportar_a_csv(df, papa_global, papa_por_tipologia)
        
        # Crear un botón para descargar el archivo CSV
        st.download_button(
            label="Descargar los resultados en CSV",
            data=buf.getvalue(),
            file_name="datos_asignaturas.csv",
            mime="text/csv"
        )
        
        # Descargar los resultados del PAPA
        st.download_button(
            label="Descargar los resultados del PAPA en CSV",
            data=resultados_buf.getvalue(),
            file_name="resultados_papa.csv",
            mime="text/csv"
        )
