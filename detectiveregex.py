import streamlit as st
import re

# Función para extraer las palabras clave usando expresiones regulares
def extraer_palabras_clave(texto):
    # Patrones para las palabras clave (expresiones regulares)
    patron_palabras_clave = r"\b(ladrón|robo|fraude|prisión|tienda|antigüedades|bolsa negra|testigos|2:00 AM|compañero|plan|1 de noviembre)\b"
    
    # Buscar las palabras clave en el texto
    palabras_encontradas = re.findall(patron_palabras_clave, texto, flags=re.IGNORECASE)
    
    return palabras_encontradas

# Función para mostrar el contenido del juego
def juego():
    # Texto misterioso (Pistas del caso)
    texto_pista = """
    El robo ocurrió en la tienda de antigüedades el 12 de octubre. Según el informe de la policía, el ladrón ingresó en la tienda durante la noche.
    La cámara de seguridad grabó todo el evento, pero no se puede identificar claramente al sospechoso.
    Se sabe que el robo fue realizado por una persona que lleva una bolsa negra, y algunos testigos mencionaron haber oído un sonido extraño alrededor de las 2:00 AM.
    El dueño de la tienda está desesperado por recuperar las piezas robadas.
    """

    # Título y descripción
    st.title("Detective Regex: Encuentra las Pistas")
    st.markdown("""
    En este juego, serás un detective que usa pistas clave encontradas en el texto para resolver el misterio.
    Usa las pistas encontradas para responder preguntas sobre el caso.
    """)

    # Mostrar el texto del caso
    st.subheader("Texto del Caso")
    st.write(texto_pista)

    # Extraer las palabras clave usando regex
    palabras_clave = extraer_palabras_clave(texto_pista)

    # Mostrar las palabras clave encontradas
    st.subheader("Palabras clave encontradas en el texto:")
    st.write(", ".join(set(palabras_clave)))

    # Pregunta y respuestas
    st.subheader("Responde las siguientes preguntas:")
    
    # Pregunta 1: ¿Dónde ocurrió el robo?
    respuesta_1 = st.text_input("Pregunta 1: ¿Dónde ocurrió el robo? ")
    
    # Pregunta 2: ¿Qué llevaba el sospechoso?
    respuesta_2 = st.text_input("Pregunta 2: ¿Qué llevaba el sospechoso? ")
    
    # Verificar respuestas
    if respuesta_1 and respuesta_2:
        if respuesta_1.lower() == "tienda de antigüedades" and respuesta_2.lower() == "bolsa negra":
            st.success("¡Correcto! Has encontrado las pistas clave y resuelto el caso.")
        else:
            st.error("Lo siento, una o más respuestas son incorrectas. Intenta de nuevo.")
    
# Llamada a la función del juego
if __name__ == "__main__":
    juego()
