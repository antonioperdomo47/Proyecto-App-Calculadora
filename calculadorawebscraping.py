import requests
from bs4 import BeautifulSoup
import tkinter as tk

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
    url_euro_dolar = 'https://es.investing.com/currencies/eur-usd'
    url_gbp_dolar = 'https://es.investing.com/currencies/gbp-usd'
    url_jpy_dolar = 'https://es.investing.com/currencies/usd-jpy'
    valor_euro_dolar = obtener_precio_moneda(url_euro_dolar)
    valor_gbp_dolar = obtener_precio_moneda(url_gbp_dolar)
    valor_jpy_dolar = obtener_precio_moneda(url_jpy_dolar)

    valor_formateado_euro_dolar = f"Dollar {float(valor_euro_dolar):.2f}"
    valor_formateado_gbp_dolar = f"Dollar {float(valor_gbp_dolar):.2f}"
    valor_formateado_jpy_dolar = f"Dollar {float(valor_jpy_dolar):.2f}"

    label_valor_euro.config(text=valor_formateado_euro_dolar)
    label_valor_gbp.config(text=valor_formateado_gbp_dolar)
    label_valor_jpy.config(text=valor_formateado_jpy_dolar)

# Crear ventana
ventana = tk.Tk()
ventana.title("Valores de Monedas")
ventana.geometry("300x300")

# Crear etiquetas para mostrar los valores
label_euro = tk.Label(ventana, text="EUR-USD", font=("Arial", 14))
label_euro.pack()
label_valor_euro = tk.Label(ventana, text="", font=("Arial", 24))
label_valor_euro.pack(pady=10)

label_gbp = tk.Label(ventana, text="GBP-USD", font=("Arial", 14))
label_gbp.pack()
label_valor_gbp = tk.Label(ventana, text="", font=("Arial", 24))
label_valor_gbp.pack(pady=10)

label_jpy = tk.Label(ventana, text="JPY-USD", font=("Arial", 14))
label_jpy.pack()
label_valor_jpy = tk.Label(ventana, text="", font=("Arial", 24))
label_valor_jpy.pack(pady=10)

# Botón para actualizar los valores
btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_valor)
btn_actualizar.pack()

# Actualizar los valores inicialmente
actualizar_valor()

# Iniciar el bucle principal de la ventana
ventana.mainloop()
