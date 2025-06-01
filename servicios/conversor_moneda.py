"""
Módulo para obtener tasas de cambio de monedas históricas usando una API pública.
Incluye una clase para obtener tasas y listar monedas disponibles.
"""

from datetime import date
import requests


class ConversorMoneda:
    """
    Clase para convertir monedas y obtener tasas de cambio en fechas específicas.
    """

    def obtener_tasa_cambio(self, fecha: date, moneda_origen: str, moneda_destino: str) -> float:
        """
        Obtiene la tasa de cambio desde `moneda_origen` hacia `moneda_destino` en una fecha específica.

        Args:
            fecha (date): Fecha para la tasa de cambio.
            moneda_origen (str): Código ISO de la moneda origen.
            moneda_destino (str): Código ISO de la moneda destino.

        Return tasa de cambio solicitada o 1.0 si hay algún error.
        """
        fecha_str = fecha.strftime('%Y-%m-%d')  # Convertir date a string para URL
        url = f"https://{fecha_str}.currency-api.pages.dev/v1/currencies/{moneda_origen.lower()}.json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            tasa_cambio = data[moneda_origen.lower()].get(moneda_destino.lower(), 1.0)
            return tasa_cambio
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo la tasa de cambio: {e}")
            return 1.0

    def lista_monedas(self) -> dict:
        """
        Devuelve un diccionario con el codigo ISO de cada
        pais, en el formato {Nombre de la moneda: Código ISO}.
        """
        url = "https://restcountries.com/v3.1/all"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            paises = response.json()

            monedas = {}
            for pais in paises:
                if "currencies" in pais:
                    for codigo, info in pais["currencies"].items():
                        monedas[codigo] = info["name"]
            
            return monedas

        except requests.RequestException as e:
            print(f"Error al obtener monedas: {e}")
            return {}

if __name__ == "__main__":
    fecha_obj = date(2025, 1, 6)
    conversor = ConversorMoneda()
    tasa = conversor.obtener_tasa_cambio(fecha_obj, "usd", "cop")
    print(f"Tasa de cambio USD a COP el {fecha_obj}: {tasa}")

    moneda = conversor.lista_monedas()
    for codigo_iso, nombre in moneda.items():
        print(f"{nombre}: {codigo_iso}")
