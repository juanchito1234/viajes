from datetime import date
from tipo_gasto import TipoGasto
from forma_pago import FormaPago

class Gasto:
    def __init__(self, fecha, valor, forma_pago, tipo_gasto):
        self.__fecha: date = fecha
        self.__valor_gastado: float = valor
        self.__forma_pago: FormaPago = forma_pago
        self.__tipo_gasto: TipoGasto = tipo_gasto

    def get_valor_gastado(self):
        return self.__valor_gastado
    
    def get_fecha(self):
        return self.__fecha
    
