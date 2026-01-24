import requests
from bs4 import BeautifulSoup


def get_cotizacion_oficial_venta():
    url_dolar_oficial = "https://dolarapi.com/v1/dolares/oficial"
    respuesta = requests.get(url_dolar_oficial, verify=True)

    resp_json = respuesta.json()
    valor_dolar_oficial_venta = resp_json["venta"]
    return valor_dolar_oficial_venta


def get_cotizacion_blue_venta():
    url_dolar_blue = "https://dolarapi.com/v1/dolares/blue"
    respuesta = requests.get(url_dolar_blue, verify=True)

    resp_json = respuesta.json()
    valor_dolar_blue_venta = resp_json["venta"]
    return valor_dolar_blue_venta


def get_cotizacion_miel_clara():
    url = r"https://infomiel.com/"
    respuesta = requests.get(url)
    html_resp = respuesta.text

    soup = BeautifulSoup(html_resp, "html.parser")

    todas_las_etiquetas = soup.find_all("td")
    precio_miel_clara = todas_las_etiquetas[0]
    precio_miel_clara = precio_miel_clara.text

    miel_clara_limpia = ""
    for caracter in precio_miel_clara:
        if caracter.isdigit():
            miel_clara_limpia += caracter

    return miel_clara_limpia


def get_cotizacion_miel_oscura():
    url = r"https://infomiel.com/"
    respuesta = requests.get(url)
    html_resp = respuesta.text

    soup = BeautifulSoup(html_resp, "html.parser")

    todas_las_etiquetas = soup.find_all("td")
    precio_miel_oscura = todas_las_etiquetas[1]
    precio_miel_oscura = precio_miel_oscura.text

    miel_oscura_limpia = ""
    for caracter in precio_miel_oscura:
        if caracter.isdigit():
            miel_oscura_limpia += caracter

    return miel_oscura_limpia