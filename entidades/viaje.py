from datetime import date
from entidades.gasto import Gasto

class Viaje:
    def __init__(self, pais, fecha_inicio, fecha_fin, presupuesto_diario, moneda_iso):
        self.__pais: str = pais
        self.__fecha_inicio: date = fecha_inicio
        self.__fecha_fin: date = fecha_fin
        self.__presupuesto_diario: float = presupuesto_diario
        self.__moneda_iso: str = moneda_iso
        self.__gastos = []

    def esta_activo(self, fecha):
        if self.__fecha_inicio < fecha < self.__fecha_fin:
            return True
        else:
            return False
        
    def get_pais(self):
        return self.__pais
        
    def get_moneda(self):
        return self.__moneda_iso
    
    def get_gastos(self):
        return self.__gastos
    
    def guardar_gasto(self, gasto: Gasto):
        self.__gastos.append(gasto)

    def get_presupuesto_diario(self):
        return self.__presupuesto_diario