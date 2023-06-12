import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox


def obtener_precio_moneda(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        valor_element = soup.find(
            "span", class_="text-2xl", attrs={"data-test": "instrument-price-last"}
        )

        if valor_element:
            valor = valor_element.text.strip()
            valor = valor.replace(",", ".")
            return float(valor)
        else:
            return None
    else:
        return None


def actualizar_valor_moneda1(*args):
    moneda_1 = combo_moneda_1.get()

    if moneda_1:
        valor_1 = obtener_precio_moneda(urls[moneda_1])
        if valor_1 is not None:
            label_valor_moneda1.config(text=f"Valor: {valor_1:.2f}")
        else:
            label_valor_moneda1.config(text="Valor no disponible")
    else:
        label_valor_moneda1.config(text="")


def actualizar_valor_moneda2(*args):
    moneda_2 = combo_moneda_2.get()

    if moneda_2:
        valor_2 = obtener_precio_moneda(urls[moneda_2])
        if valor_2 is not None:
            label_valor_moneda2.config(text=f"Valor: {valor_2:.2f}")
        else:
            label_valor_moneda2.config(text="Valor no disponible")
    else:
        label_valor_moneda2.config(text="")


def comparar_monedas():
    moneda_1 = combo_moneda_1.get()
    moneda_2 = combo_moneda_2.get()
    cantidad = entry_cantidad.get()

    if moneda_1 and moneda_2 and cantidad:
        valor_1 = obtener_precio_moneda(urls[moneda_1])
        valor_2 = obtener_precio_moneda(urls[moneda_2])

        if valor_1 is not None and valor_2 is not None:
            resultado = (valor_1 / valor_2) * float(cantidad)
            label_resultado.config(
                text=f"El resultado de la comparación es: {resultado:.2f}"
            )
        else:
            label_resultado.config(
                text="No se pudo obtener el valor de una o ambas monedas."
            )
    else:
        label_resultado.config(
            text="Debes seleccionar dos monedas y especificar una cantidad."
        )


ventana = tk.Tk()
ventana.title("Comparador de Monedas")
ventana.geometry("400x300")

urls = {
    "EUR-USD": "https://es.investing.com/currencies/usd-eur",
    "DOLAR": "https://es.investing.com/currencies/eur-usd",
    "GBP-USD": "https://es.investing.com/currencies/usd-gbp",
    "JPY-USD": "https://es.investing.com/currencies/usd-jpy",
    "CHF-USD": "https://es.investing.com/currencies/usd-chf",
    "AUD-USD": "https://es.investing.com/currencies/usd-aud",
    "CAD-USD": "https://es.investing.com/currencies/usd-cad",
}

label_moneda_nacional = tk.Label(ventana, text="Mi moneda Nacional")
label_moneda_nacional.pack(pady=(10, 0))

combo_moneda_1 = AutocompleteCombobox(ventana, completevalues=list(urls.keys()))
combo_moneda_1.pack(pady=10)
combo_moneda_1.bind("<<ComboboxSelected>>", actualizar_valor_moneda1)

label_valor_moneda1 = tk.Label(ventana)
label_valor_moneda1.pack()

label_pais_visita = tk.Label(ventana, text="País que visito")
label_pais_visita.pack(pady=(10, 0))

combo_moneda_2 = AutocompleteCombobox(ventana, completevalues=list(urls.keys()))
combo_moneda_2.pack(pady=10)
combo_moneda_2.bind("<<ComboboxSelected>>", actualizar_valor_moneda2)

label_valor_moneda2 = tk.Label(ventana)
label_valor_moneda2.pack()

entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack(pady=10)

btn_comparar = tk.Button(ventana, text="Comparar", command=comparar_monedas)
btn_comparar.pack(pady=10)

label_resultado = tk.Label(ventana)
label_resultado.pack(pady=10)

ventana.mainloop()
