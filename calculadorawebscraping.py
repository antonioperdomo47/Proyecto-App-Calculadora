import requests
from bs4 import BeautifulSoup
import tkinter as tk

def obtener_precio_euro_dolar():
    url = 'https://es.investing.com/currencies/eur-usd'

    # Realizar la solicitud GET al sitio web
    response = requests.get(url)

    if response.status_code == 200:
        # Analizar el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar el elemento que contiene el valor del Euro-Dólar
        valor_element = soup.find('span', class_='text-2xl', attrs={'data-test': 'instrument-price-last'})

        if valor_element:
            valor = valor_element.text.strip()
            return valor
        else:
            return "No se encontró el valor del Euro-Dólar en la página."
    else:
        return f"No se pudo acceder a la página {url}."


def actualizar_valor():
    valor = obtener_precio_euro_dolar()
    label_valor.config(text=valor)

# Crear ventana
ventana = tk.Tk()
ventana.title("Valor del Euro-Dólar")
ventana.geometry("300x300")

# Crear etiqueta para mostrar el valor
label_valor = tk.Label(ventana, text="", font=("Arial", 24))
label_valor.pack(pady=50)

# Botón para actualizar el valor
btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_valor)
btn_actualizar.pack()

# Actualizar el valor inicialmente
actualizar_valor()

# Iniciar el bucle principal de la ventana
ventana.mainloop()
