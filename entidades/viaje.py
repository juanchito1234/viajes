from datetime import date

class Viaje:
    def __init__(self):
        self.__pais: str
        self.__fecha_inicio: date
        self.__fecha_fin: date
        self.__presupuesto_diario: float
        self.__moneda_iso: str