import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class ComparadorMonedas(App):
    def build(self):
        self.urls = {
            "EUR-USD": "https://es.investing.com/currencies/usd-eur",
            "DOLAR": "https://es.investing.com/currencies/eur-usd",
            "GBP-USD": "https://es.investing.com/currencies/usd-gbp",
            "JPY-USD": "https://es.investing.com/currencies/usd-jpy",
            "CHF-USD": "https://es.investing.com/currencies/usd-chf",
            "AUD-USD": "https://es.investing.com/currencies/usd-aud",
            "CAD-USD": "https://es.investing.com/currencies/usd-cad",
        }

        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        self.label_moneda_nacional = Label(text="Mi moneda Nacional")
        self.layout.add_widget(self.label_moneda_nacional)

        self.combo_moneda_1 = DropDown()
        self.combo_moneda_1.bind(on_select=self.actualizar_valor_moneda1)

        for moneda in self.urls.keys():
            btn = Button(text=moneda, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.combo_moneda_1.select(btn.text))
            self.combo_moneda_1.add_widget(btn)

        self.btn_moneda_1 = Button(
            text="Seleccionar moneda", size_hint=(1, None), height=40
        )
        self.btn_moneda_1.bind(on_release=self.combo_moneda_1.open)
        self.layout.add_widget(self.btn_moneda_1)

        self.label_valor_moneda1 = Label()
        self.layout.add_widget(self.label_valor_moneda1)

        self.label_pais_visita = Label(text="País que visito")
        self.layout.add_widget(self.label_pais_visita)

        self.combo_moneda_2 = DropDown()
        self.combo_moneda_2.bind(on_select=self.actualizar_valor_moneda2)

        for moneda in self.urls.keys():
            btn = Button(text=moneda, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.combo_moneda_2.select(btn.text))
            self.combo_moneda_2.add_widget(btn)

        self.btn_moneda_2 = Button(
            text="Seleccionar moneda", size_hint=(1, None), height=40
        )
        self.btn_moneda_2.bind(on_release=self.combo_moneda_2.open)
        self.layout.add_widget(self.btn_moneda_2)

        self.label_valor_moneda2 = Label()
        self.layout.add_widget(self.label_valor_moneda2)

        self.entry_cantidad = TextInput(hint_text="Cantidad", multiline=False)
        self.layout.add_widget(self.entry_cantidad)

        self.btn_comparar = Button(text="Comparar", size_hint=(1, None), height=40)
        self.btn_comparar.bind(on_release=self.comparar_monedas)
        self.layout.add_widget(self.btn_comparar)

        self.label_resultado = Label()
        self.layout.add_widget(self.label_resultado)

        return self.layout

    def obtener_precio_moneda(self, url):
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

    def actualizar_valor_moneda1(self, instance, value):
        moneda_1 = value

        if moneda_1:
            valor_1 = self.obtener_precio_moneda(self.urls[moneda_1])
            if valor_1 is not None:
                self.label_valor_moneda1.text = f"Valor: {valor_1:.2f}"
            else:
                self.label_valor_moneda1.text = "Valor no disponible"
        else:
            self.label_valor_moneda1.text = ""

    def actualizar_valor_moneda2(self, instance, value):
        moneda_2 = value

        if moneda_2:
            valor_2 = self.obtener_precio_moneda(self.urls[moneda_2])
            if valor_2 is not None:
                self.label_valor_moneda2.text = f"Valor: {valor_2:.2f}"
            else:
                self.label_valor_moneda2.text = "Valor no disponible"
        else:
            self.label_valor_moneda2.text = ""

    def comparar_monedas(self, instance):
        moneda_1 = self.combo_moneda_1.button.text
        moneda_2 = self.combo_moneda_2.button.text
        cantidad = self.entry_cantidad.text

        if moneda_1 and moneda_2 and cantidad:
            valor_1 = self.obtener_precio_moneda(self.urls[moneda_1])
            valor_2 = self.obtener_precio_moneda(self.urls[moneda_2])

            if valor_1 is not None and valor_2 is not None:
                resultado = (valor_1 / valor_2) * float(cantidad)
                self.label_resultado.text = (
                    f"El resultado de la comparación es: {resultado:.2f}"
                )
            else:
                self.label_resultado.text = (
                    "No se pudo obtener el valor de una o ambas monedas."
                )
        else:
            self.label_resultado.text = (
                "Debes seleccionar dos monedas y especificar una cantidad."
            )


ComparadorMonedas().run()
