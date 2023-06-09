import tkinter as tk
import json
from forex_python.converter import CurrencyRates
from PIL import ImageTk, Image

# Creamos una instancia de la clase CurrencyRates
c = CurrencyRates()

# Nombre del archivo donde se guardará la configuración
CONFIG_FILE = "config.json"


# Función para realizar la conversión de monedas
def convertir():
    moneda_base = combo_moneda_base.get()
    moneda_destino = combo_moneda_destino.get()
    cantidad = float(entry_cantidad.get())

    resultado = c.convert(moneda_base, moneda_destino, cantidad)

    label_resultado.config(text=f"Resultado: {resultado:.2f} {moneda_destino}")


# Función para borrar el contenido de la casilla de Cantidad y el resultado
def borrar_cantidad():
    entry_cantidad.delete(0, tk.END)  # Eliminar el contenido de la casilla
    label_resultado.config(text="Resultado:")  # Borrar el resultado


# Función para guardar la configuración en un archivo
def guardar_configuracion():
    moneda_base = combo_moneda_base.get()
    moneda_destino = combo_moneda_destino.get()

    # Crear un diccionario con la configuración
    configuracion = {"moneda_base": moneda_base, "moneda_destino": moneda_destino}

    # Guardar el diccionario en un archivo JSON
    with open(CONFIG_FILE, "w") as file:
        json.dump(configuracion, file)


# Creación de la ventana principal
ventana = tk.Tk()
ventana.title("Cuanto estoy pagando?")
ventana.geometry("300x400")
ventana.config(bg="#5d7973")  # Color de fondo

# Cargar la imagen
imagen = Image.open("intercambiodinero.png")
imagen = imagen.resize(
    (200, 200)
)  # Ajustar el tamaño de la imagen según tus necesidades
imagen = ImageTk.PhotoImage(imagen)

# Crear un widget Label para mostrar la imagen
label_imagen = tk.Label(ventana, image=imagen)
label_imagen.pack()

# Obtener la lista de monedas disponibles
monedas_disponibles = c.get_rates("").keys()

# Creación de los widgets
label_moneda_base = tk.Label(ventana, text="Moneda base:")
label_moneda_base.pack()

combo_moneda_base = tk.StringVar(ventana)
combo_moneda_base.set("USD")  # Valor predeterminado
menu_moneda_base = tk.OptionMenu(ventana, combo_moneda_base, *monedas_disponibles)
menu_moneda_base.pack()

label_moneda_destino = tk.Label(ventana, text="Moneda destino:")
label_moneda_destino.pack()

combo_moneda_destino = tk.StringVar(ventana)
combo_moneda_destino.set("EUR")  # Valor predeterminado
menu_moneda_destino = tk.OptionMenu(ventana, combo_moneda_destino, *monedas_disponibles)
menu_moneda_destino.pack()

label_cantidad = tk.Label(ventana, text="Cantidad:")
label_cantidad.pack()

entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()

btn_convertir = tk.Button(
    ventana, text="Convertir", command=convertir, relief=tk.RIDGE, borderwidth=5
)
btn_convertir.pack()

label_resultado = tk.Label(ventana, text="Resultado:")
label_resultado.pack()

btn_borrar = tk.Button(
    ventana,
    text="Borrar",
    command=borrar_cantidad,  # Asociar la función borrar_cantidad al botón
    relief=tk.RIDGE,
    borderwidth=5,
)
btn_borrar.pack()

btn_guardar = tk.Button(
    ventana,
    text="Guardar Configuración",
    command=guardar_configuracion,  # Asociar la función guardar_configuracion al botón
    relief=tk.RIDGE,
    borderwidth=5,
)
btn_guardar.pack()

# Ejecución de la aplicación
ventana.mainloop()
