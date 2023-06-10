import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

def obtener_precio_moneda(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        valor_element = soup.find('span', class_='text-2xl', attrs={'data-test': 'instrument-price-last'})

        if valor_element:
            valor = valor_element.text.strip()
            valor = valor.replace(',', '.')  # Reemplazar la coma por un punto decimal
            return valor
        else:
            return "No se encontró el valor de la moneda en la página."
    else:
        return f"No se pudo acceder a la página {url}."


def actualizar_valor():
    moneda_seleccionada = combo_moneda.get()
    url = urls[moneda_seleccionada]
    valor = obtener_precio_moneda(url)
    valor_formateado = f"Dollar {float(valor):.2f}"
    label_valor.config(text=valor_formateado)


# Crear ventana
ventana = tk.Tk()
ventana.title("Valores de Monedas")
ventana.geometry("300x200")

# Diccionario de monedas y sus URLs correspondientes
urls = {
    'EUR-USD': 'https://es.investing.com/currencies/eur-usd',
    'GBP-USD': 'https://es.investing.com/currencies/gbp-usd',
    'JPY-USD': 'https://es.investing.com/currencies/usd-jpy',
    'CHF-USD': 'https://es.investing.com/currencies/usd-chf',
    'AUD-USD': 'https://es.investing.com/currencies/aud-usd',
    'CAD-USD': 'https://es.investing.com/currencies/usd-cad',
    'NZD-USD': 'https://es.investing.com/currencies/nzd-usd',
    'ZAR-USD': 'https://es.investing.com/currencies/usd-zar',
    'TRY-USD': 'https://es.investing.com/currencies/usd-try'
}

# Crear Combobox
combo_moneda = ttk.Combobox(ventana, state="normal", font=("Arial", 12), width=15)
combo_moneda['values'] = tuple(urls.keys())
combo_moneda.set("Escribe la moneda")  # Texto inicial
combo_moneda.pack(pady=20)

# Botón para actualizar los valores
btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_valor)
btn_actualizar.pack()

# Crear etiqueta para mostrar el valor
label_valor = tk.Label(ventana, text="", font=("Arial", 14))
label_valor.pack(pady=20)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
