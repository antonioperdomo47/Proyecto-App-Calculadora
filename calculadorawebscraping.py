import requests
from bs4 import BeautifulSoup

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
        print("Valor del Euro-Dólar:", valor)
    else:
        print("No se encontró el valor del Euro-Dólar en la página.")
else:
    print(f"No se pudo acceder a la página {url}.")
