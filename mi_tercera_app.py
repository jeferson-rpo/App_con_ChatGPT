# Este codigo fue realizado por chatgpt
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import csv

# Archivo para guardar los datos
archivo_finanzas = "finanzas.csv"

# Función para inicializar el archivo CSV si no existe
def inicializar_archivo():
    try:
        with open(archivo_finanzas, "x", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Fecha", "Tipo", "Monto"])
    except FileExistsError:
        pass  # El archivo ya existe, no hacemos nada

# Función para agregar una transacción
def agregar_transaccion():
    fecha = calendario.get_date()
    tipo = tipo_transaccion.get()
    monto = entrada_monto.get()
    
    if not monto.isdigit():
        label_estado.config(text="Por favor, ingresa un monto válido.", fg="red")
        return
    
    with open(archivo_finanzas, "a", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([fecha, tipo, monto])
    
    label_estado.config(text="Transacción agregada correctamente.", fg="green")
    actualizar_lista_transacciones()
    entrada_monto.delete(0, tk.END)

# Función para actualizar la lista de transacciones
def actualizar_lista_transacciones():
    for item in tabla.get_children():
        tabla.delete(item)
    
    with open(archivo_finanzas, "r") as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezado
        for fila in lector:
            tabla.insert("", tk.END, values=fila)

# Configuración inicial
inicializar_archivo()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Registro de Finanzas Personales")
ventana.geometry("600x500")

# Calendario para seleccionar fecha
calendario = Calendar(ventana, selectmode='day', date_pattern='dd/mm/yyyy')
calendario.pack(pady=10)

# Tipo de transacción
tipo_transaccion = ttk.Combobox(ventana, values=["Ingreso", "Gasto"])
tipo_transaccion.set("Selecciona tipo")
tipo_transaccion.pack(pady=5)

# Entrada para el monto
entrada_monto = ttk.Entry(ventana)
entrada_monto.pack(pady=5)
entrada_monto.insert(0, "Ingresa el monto")

# Botón para agregar la transacción
btn_agregar = ttk.Button(ventana, text="Agregar Transacción", command=agregar_transaccion)
btn_agregar.pack(pady=10)

# Estado de las operaciones
label_estado = ttk.Label(ventana, text="")
label_estado.pack(pady=5)

# Tabla para mostrar transacciones
tabla = ttk.Treeview(ventana, columns=("Fecha", "Tipo", "Monto"), show="headings")
tabla.heading("Fecha", text="Fecha")
tabla.heading("Tipo", text="Tipo")
tabla.heading("Monto", text="Monto")
tabla.pack(pady=20, fill=tk.BOTH, expand=True)

# Cargar las transacciones existentes
actualizar_lista_transacciones()

# Ejecutar la ventana principal
ventana.mainloop()

