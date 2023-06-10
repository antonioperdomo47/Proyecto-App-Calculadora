import requests
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.ttk as ttk


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


def comparar_monedas():
    moneda_1 = combo_moneda_1.get()
    moneda_2 = combo_moneda_2.get()

    if moneda_1 and moneda_2:
        valor_1 = obtener_precio_moneda(urls[moneda_1])
        valor_2 = obtener_precio_moneda(urls[moneda_2])

        if valor_1 is not None and valor_2 is not None:
            resultado = valor_1 / valor_2
            label_resultado.config(
                text=f"El resultado de la comparación es: {resultado:.2f}"
            )
        else:
            label_resultado.config(
                text="No se pudo obtener el valor de una o ambas monedas."
            )
    else:
        label_resultado.config(text="Debes seleccionar dos monedas.")


ventana = tk.Tk()
ventana.title("Comparador de Monedas")
ventana.geometry("300x200")

urls = {
    "EUR-USD": "https://es.investing.com/currencies/eur-usd",
    "GBP-USD": "https://es.investing.com/currencies/gbp-usd",
    "JPY-USD": "https://es.investing.com/currencies/usd-jpy",
    "CHF-USD": "https://es.investing.com/currencies/usd-chf",
    "AUD-USD": "https://es.investing.com/currencies/aud-usd",
    "CAD-USD": "https://es.investing.com/currencies/usd-cad",
    "NZD-USD": "https://es.investing.com/currencies/nzd-usd",
    "ZAR-USD": "https://es.investing.com/currencies/usd-zar",
    "TRY-USD": "https://es.investing.com/currencies/usd-try",
}

combo_moneda_1 = ttk.Combobox(ventana, values=list(urls.keys()))
combo_moneda_1.pack(pady=10)

combo_moneda_2 = ttk.Combobox(ventana, values=list(urls.keys()))
combo_moneda_2.pack(pady=10)

btn_comparar = tk.Button(ventana, text="Comparar", command=comparar_monedas)
btn_comparar.pack(pady=10)

label_resultado = tk.Label(ventana)
label_resultado.pack(pady=10)

ventana.mainloop()
