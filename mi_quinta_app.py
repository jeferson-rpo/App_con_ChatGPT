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
    "Ens
