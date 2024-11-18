# Este progreama se hizo con chatgpt
import streamlit as st

# Definir las recetas
recetas = {
    "Hamburguesa": {
        "ingredientes": [
            "Carne molida de res (500g)",
            "Pan de hamburguesa (2 unidades)",
            "Lechuga",
            "Tomate (1 unidad)",
            "Queso (2 rebanadas)",
            "Salsas (ketchup, mayonesa)"
        ],
        "pasos": [
            "1. Forma las hamburguesas con la carne molida.",
            "2. Cocina las hamburguesas en una sartén por 4-5 minutos de cada lado.",
            "3. Tuesta ligeramente los panes de hamburguesa.",
            "4. Coloca la carne en el pan, agrega el queso, lechuga, tomate y salsas.",
            "5. ¡Disfruta tu hamburguesa!"
        ],
        "foto": "https://www.portafolio.co/files/article_new_multimedia/uploads/2022/04/12/6255e2e41db6c.jpeg" 
    },
    "Sancocho": {
        "ingredientes": [
            "Pollo (1 kg)",
            "Papa (2 unidades)",
            "Yuca (300g)",
            "Zanahoria (2 unidades)",
            "Calabaza (200g)",
            "Cebolla, ajo, sal y pimienta"
        ],
        "pasos": [
            "1. Cocina el pollo en agua con cebolla, ajo, sal y pimienta.",
            "2. Añade las papas, yuca, zanahorias y calabaza.",
            "3. Cocina a fuego lento por aproximadamente 30 minutos.",
            "4. Sirve caliente y disfruta."
        ],
        "foto": "https://www.elespectador.com/resizer/v2/NPCOUP725ZBQBCLN6TJ5RUSHHI.jpg?auth=f64cd0a70dc86f5895feddb9b5503ecbbd47c221c78d057e3e925856c4dbccdb&width=1200&height=675&smart=true&quality=80" 
    },
    "Salchipapas con queso": {
        "ingredientes": [
            "Papas (3 unidades)",
            "Salchichas (4 unidades)",
            "Queso rallado",
            "Aceite para freír",
            "Salsas (opcional)"
        ],
        "pasos": [
            "1. Corta las papas en tiras y fríelas hasta que estén doradas.",
            "2. Fría las salchichas y córtalas en rodajas.",
            "3. Sirve las papas, agrega las salchichas y espolvorea queso rallado por encima.",
            "4. Puedes añadir salsas como ketchup o mayonesa.",
            "5. ¡Listo para disfrutar!"
        ],
        "foto": "https://i.ytimg.com/vi/vlo3cRtybbQ/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLA6w8Ydb4SYliuFUYLWyTaIGcz6sA"  
    },
    "Tacos de pollo": {
        "ingredientes": [
            "Pollo desmenuzado (300g)",
            "Tortillas de maíz",
            "Cebolla (1 unidad)",
            "Cilantro fresco",
            "Limón",
            "Salsas"
        ],
        "pasos": [
            "1. Cocina el pollo con cebolla, sal y pimienta.",
            "2. Calienta las tortillas y agrega el pollo desmenuzado.",
            "3. Agrega cilantro, cebolla picada y un chorrito de limón.",
            "4. Añade salsa al gusto y disfruta."
        ],
        "foto": "https://cocinaconmichela.com/wp-content/uploads/2023/10/THUMBNAIL-OCT-5-25-600-x-600-500x500.png"  
    },
    "Ensalada César": {
        "ingredientes": [
            "Lechuga romana",
            "Pechuga de pollo (200g)",
            "Crutones",
            "Queso parmesano",
            "Aderezo César"
        ],
        "pasos": [
            "1. Cocina la pechuga de pollo y córtala en tiras.",
            "2. Lava y corta la lechuga en trozos.",
            "3. Mezcla la lechuga, el pollo, los crutones y el queso.",
            "4. Agrega el aderezo César y mezcla bien.",
            "5. Sirve y disfruta."
        ],
        "foto": "https://www.pequerecetas.com/wp-content/uploads/2017/09/ensalada-cesar.jpg"
    }
}

# Interfaz de usuario
st.title("App de Recetas de Cocina ")
st.write("¡Bienvenido! Elige una receta y te mostramos los ingredientes, los pasos y una foto. por Jeferson Orley Restrepo Bedoya")

# Selección de receta
receta_seleccionada = st.selectbox("¿Qué quieres cocinar?", list(recetas.keys()))

# Definir los estilos por receta
estilos = {
    "Hamburguesa": {
        "color": "#FF6347",  # Rojo
        "border_color": "#D94E41",
        "foto_border": "5px solid #D94E41"
    },
    "Sancocho": {
        "color": "#4682B4",  # Azul
        "border_color": "#3A6B8B",
        "foto_border": "5px solid #3A6B8B"
    },
    "Salchipapas con queso": {
        "color": "#FFD700",  # Amarillo
        "border_color": "#E6B800",
        "foto_border": "5px solid #E6B800"
    },
    "Tacos de pollo": {
        "color": "#32CD32",  # Verde
        "border_color": "#2E8B57",
        "foto_border": "5px solid #2E8B57"
    },
    "Ensalada César": {
        "color": "#8B4513",  # Marrón
        "border_color": "#A0522D",
        "foto_border": "5px solid #A0522D"
    }
}

# Obtener el estilo basado en la receta seleccionada
estilo = estilos[receta_seleccionada]

# Mostrar los ingredientes con el estilo de la receta
st.subheader("Ingredientes:")
ingredientes_html = f"<ul style='list-style-type: none; padding: 0; border: {estilo['foto_border']}'>"
for ingrediente in receta["ingredientes"]:
    ingredientes_html += f"<li style='background-color: {estilo['color']}; color: white; padding: 8px; margin: 2px; border-radius: 5px; border: 1px solid {estilo['border_color']};'>{ingrediente}</li>"

ingredientes_html += "</ul>"
st.markdown(ingredientes_html, unsafe_allow_html=True)

# Mostrar los pasos con el estilo de la receta
st.subheader("Paso a paso:")
pasos_html = f"<ul style='list-style-type: none; padding: 0;'>"
for paso in receta["pasos"]:
    pasos_html += f"<li style='background-color: {estilo['color']}; color: white; padding: 8px; margin: 2px; border-radius: 5px; border: 1px solid {estilo['border_color']};'>{paso}</li>"

pasos_html += "</ul>"
st.markdown(pasos_html, unsafe_allow_html=True)

# Foto con borde de estilo
st.subheader("Foto de la receta:")
st.markdown(f"<div style='border: {estilo['foto_border']}; padding: 10px;'>", unsafe_allow_html=True)
st.image(receta["foto"], use_column_width=True)
st.markdown("</div>", unsafe_allow_html=True)


