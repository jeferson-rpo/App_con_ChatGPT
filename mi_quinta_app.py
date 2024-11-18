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
        "foto": "imagenes/hamburguesa.jpg"  # Asegúrate de que la imagen esté en la carpeta correcta
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
        "foto": "imagenes/sancocho.jpg"  # Asegúrate de que la imagen esté en la carpeta correcta
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
        "foto": "imagenes/salchipapas.jpg"  # Asegúrate de que la imagen esté en la carpeta correcta
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
        "foto": "imagenes/tacos.jpg"  # Asegúrate de que la imagen esté en la carpeta correcta
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
        "foto": "imagenes/ensalada_cesar.jpg"  # Asegúrate de que la imagen esté en la carpeta correcta
    }
}

# Interfaz de usuario
st.title("App de Recetas de Cocina")
st.write("¡Bienvenido! Elige una receta y te mostramos los ingredientes, los pasos y una foto.")

# Selección de receta
receta_seleccionada = st.selectbox("¿Qué quieres cocinar?", list(recetas.keys()))

# Mostrar ingredientes, pasos y foto
receta = recetas[receta_seleccionada]

# Ingredientes
st.subheader("Ingredientes:")
for ingrediente in receta["ingredientes"]:
    st.write(f"- {ingrediente}")

# Pasos
st.subheader("Paso a paso:")
for paso in receta["pasos"]:
    st.write(paso)

# Foto
st.subheader("Foto de la receta:")
st.image(receta["foto"], use_column_width=True)