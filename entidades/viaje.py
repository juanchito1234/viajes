from datetime import date
from gasto import Gasto

class Viaje:
    def __init__(self, pais: str, fecha_inicio: date, fecha_fin: date,
                 presupuesto_diario: float, moneda_iso: str):
        self.__pais: str
        self.__fecha_inicio: date
        self.__fecha_fin: date
        self.__presupuesto_diario: float
        self.__moneda_iso: str
        self.__gastos = []

    def esta_activo(self):
        if ((self.__fecha_inicio < date.today) and (self.__fecha_fin > date.today)):
            return True
        else:
            return False
        
    def get_pais(self):
        return self.__pais
        
    def get_moneda(self):
        return self.__moneda_iso
    
    def guardar_gasto(self, gasto: Gasto):
        self.__gastos.append(gasto)

    def get_presupuesto_diario(self):
        return self.__presupuesto_diario