import streamlit as st
import re

# Función para extraer las palabras clave usando expresiones regulares
def extraer_palabras_clave(texto):
    # Patrones para las palabras clave (expresiones regulares)
    patron_palabras_clave = r"\b(ladrón|robo|fraude|prisión|tienda|antigüedades|bolsa negra|testigos|2:00 AM|compañero|plan|1 de noviembre|cámaras de seguridad|escapó|desesperado|secuestro|sonido extraño|chaqueta azul|gorro negro)\b"
    
    # Buscar las palabras clave en el texto
    palabras_encontradas = re.findall(patron_palabras_clave, texto, flags=re.IGNORECASE)
    
    return list(set(palabras_encontradas))  # Evitar duplicados

# Función para verificar si una respuesta contiene una palabra clave
def verificar_respuesta(respuesta, palabra_clave):
    # Usar regex para buscar la palabra clave en la respuesta
    if re.search(r"\b" + re.escape(palabra_clave) + r"\b", respuesta, re.IGNORECASE):
        return True
    return False

# Función para mostrar el contenido del juego
def juego():
    # Títulos y descripción
    st.title("Detective Regex: Encuentra las Pistas")
    st.markdown("""
    ¡Bienvenido, detective! En este juego, usarás pistas clave extraídas de textos misteriosos para resolver casos. 
    Tu tarea es responder preguntas sobre los textos. ¡Resuelve el caso y avanza a niveles más difíciles!
    """)

    # Seleccionar nivel
    nivel = st.selectbox("Selecciona un nivel", 
                         ["Nivel 1: El Robo en la Tienda de Antigüedades", 
                          "Nivel 2: El Sospechoso Escapó", 
                          "Nivel 3: La Conexión Final"], 
                         key="nivel_selectbox")

    # Definir textos y preguntas de los niveles
    if nivel == "Nivel 1: El Robo en la Tienda de Antigüedades":
        texto_pista = """
        El robo ocurrió en la tienda de antigüedades el 12 de octubre. Según el informe de la policía, el ladrón ingresó en la tienda durante la noche.
        La cámara de seguridad grabó todo el evento, pero no se puede identificar claramente al sospechoso. 
        Se sabe que el robo fue realizado por una persona que lleva una bolsa negra, y algunos testigos mencionaron haber oído un sonido extraño alrededor de las 2:00 AM.
        El dueño de la tienda está desesperado por recuperar las piezas robadas.
        """
        preguntas = [
            ("¿Dónde ocurrió el robo?", "Tienda de antigüedades"),
            ("¿Qué llevaba el ladrón?", "Bolsa negra"),
            ("¿A qué hora se oyó el sonido extraño?", "2:00 AM"),
            ("¿Qué usó la policía para investigar?", "Cámaras de seguridad"),
            
        ]

    elif nivel == "Nivel 2: El Sospechoso Escapó":
        texto_pista = """
        La ciudad estaba tranquila hasta que el ladrón se escapó de la cárcel. La policía no sabe mucho sobre el ladrón, pero hay algo extraño en el caso.
        En el pasado, el ladrón estuvo en prisión por robo y fraude. Nadie ha visto a la persona sospechosa desde entonces. 
        Los testigos afirman que fue un hombre de mediana edad, con una chaqueta azul y una gorra negra. 
        """
        preguntas = [
            ("¿Dónde estuvo el ladrón antes de escapar?", "Prisión"),
            ("¿Qué delitos cometió el ladrón?", "Robo y fraude"),
            ("¿Qué llevaba el ladrón?", "chaqueta azul"),
            ("¿Qué dijeron los testigos?", "Lo vieron escapar")
        ]

    elif nivel == "Nivel 3: La Conexión Final":
        texto_pista = """
        Después de días de investigación, encontramos una nueva pista. El sospechoso parece tener una conexión con un antiguo compañero de prisión que estuvo involucrado en robos similares. 
        El compañero está en una localidad cercana, y se ha mencionado que ambos se reunieron el 1 de noviembre para discutir un plan.
        La policía está monitoreando sus movimientos para capturarlos antes de que escapen.
        """
        preguntas = [
            ("¿Cuándo se reunieron los dos sospechosos?", "1 de noviembre"),
            ("¿Qué discutieron?", "Un plan para realizar un robo"),
            ("¿Qué conecta a los dos sospechosos?", "Compañero de prisión"),
            ("¿Qué está haciendo la policía?", "Monitoreando sus movimientos")
        ]

    # Mostrar el texto del caso
    st.subheader(f"Texto del {nivel}")
    st.write(texto_pista)

    # Extraer las palabras clave usando regex
    palabras_clave = extraer_palabras_clave(texto_pista)

    # Mostrar las palabras clave encontradas
    st.subheader("Palabras clave encontradas en el texto:")
    st.write(", ".join(palabras_clave))

    # Preguntar al jugador
    st.subheader("Responde las siguientes preguntas:")
    
    respuestas = {}
    
    for pregunta, respuesta_correcta in preguntas:
        # Crear un cuadro de texto para que el jugador ingrese la respuesta completa
        respuestas[pregunta] = st.text_input(pregunta, key=pregunta, help="Escribe la respuesta completa.")

    # Agregar el botón de verificación
    if st.button('Verificar respuestas', key="verificar_respuestas"):
        respuestas_correctas = 0
        
        # Verificar respuestas
        for pregunta, respuesta_correcta in preguntas:
            if verificar_respuesta(respuestas.get(pregunta, "").strip(), respuesta_correcta):
                respuestas_correctas += 1
                st.success(f"✔️ Respuesta correcta para: {pregunta}")
            else:
                st.error(f"❌ Respuesta incorrecta para: {pregunta}. La respuesta correcta era: {respuesta_correcta}")
        
        # Verificar si todas las respuestas son correctas
        if respuestas_correctas == len(preguntas):
            st.success("🎉 ¡Correcto! Has resuelto el caso. ¡Avancemos al siguiente nivel!")
        else:
            st.warning("🔍 Algunas respuestas son incorrectas. Intenta de nuevo.")

# Llamada a la función del juego
if __name__ == "__main__":
    juego()

