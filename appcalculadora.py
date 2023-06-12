import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup


class ComparadorMonedasApp(App):
    urls = {
        "EUR-USD": "https://es.investing.com/currencies/usd-eur",
        "DOLAR": "https://es.investing.com/currencies/eur-usd",
        "GBP-USD": "https://es.investing.com/currencies/usd-gbp",
        "JPY-USD": "https://es.investing.com/currencies/usd-jpy",
        "CHF-USD": "https://es.investing.com/currencies/usd-chf",
        "AUD-USD": "https://es.investing.com/currencies/usd-aud",
        "CAD-USD": "https://es.investing.com/currencies/usd-cad",
    }

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

    def actualizar_valor_moneda1(self, instance):
        moneda_1 = self.combo_moneda_1.text

        if moneda_1:
            valor_1 = self.obtener_precio_moneda(self.urls[moneda_1])
            if valor_1 is not None:
                self.label_valor_moneda1.text = f"Valor: {valor_1:.2f}"
            else:
                self.label_valor_moneda1.text = "Valor no disponible"
        else:
            self.label_valor_moneda1.text = ""

    def actualizar_valor_moneda2(self, instance):
        moneda_2 = self.combo_moneda_2.text

        if moneda_2:
            valor_2 = self.obtener_precio_moneda(self.urls[moneda_2])
            if valor_2 is not None:
                self.label_valor_moneda2.text = f"Valor: {valor_2:.2f}"
            else:
                self.label_valor_moneda2.text = "Valor no disponible"
        else:
            self.label_valor_moneda2.text = ""

    def comparar_monedas(self, instance):
        moneda_1 = self.combo_moneda_1.text
        moneda_2 = self.combo_moneda_2.text
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

    def build(self):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        label_moneda_nacional = Label(text="Mi moneda Nacional")
        layout.add_widget(label_moneda_nacional)

        self.combo_moneda_1 = Button(text="Seleccionar moneda")
        self.combo_moneda_1.bind(on_release=self.show_dropdown_1)
        layout.add_widget(self.combo_moneda_1)

        self.label_valor_moneda1 = Label()
        layout.add_widget(self.label_valor_moneda1)

        label_pais_visita = Label(text="País que visito")
        layout.add_widget(label_pais_visita)

        self.combo_moneda_2 = Button(text="Seleccionar moneda")
        self.combo_moneda_2.bind(on_release=self.show_dropdown_2)
        layout.add_widget(self.combo_moneda_2)

        self.label_valor_moneda2 = Label()
        layout.add_widget(self.label_valor_moneda2)

        self.entry_cantidad = TextInput(hint_text="Cantidad")
        layout.add_widget(self.entry_cantidad)

        btn_comparar = Button(text="Comparar")
        btn_comparar.bind(on_release=self.comparar_monedas)
        layout.add_widget(btn_comparar)

        self.label_resultado = Label()
        layout.add_widget(self.label_resultado)

        self.dropdown_1 = DropDown()
        self.dropdown_2 = DropDown()

        for moneda in self.urls.keys():
            btn = Button(text=moneda, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.select_dropdown_value(btn.text, 1))
            self.dropdown_1.add_widget(btn)

            btn = Button(text=moneda, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.select_dropdown_value(btn.text, 2))
            self.dropdown_2.add_widget(btn)

        return layout

    def show_dropdown_1(self, instance):
        self.dropdown_1.open(instance)

    def show_dropdown_2(self, instance):
        self.dropdown_2.open(instance)

    def select_dropdown_value(self, value, dropdown_num):
        if dropdown_num == 1:
            self.combo_moneda_1.text = value
            self.actualizar_valor_moneda1(None)
        elif dropdown_num == 2:
            self.combo_moneda_2.text = value
            self.actualizar_valor_moneda2(None)
        self.dismiss_dropdown()

    def dismiss_dropdown(self):
        self.dropdown_1.dismiss()
        self.dropdown_2.dismiss()


if __name__ == "__main__":
    ComparadorMonedasApp().run()
