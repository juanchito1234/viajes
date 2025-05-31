from datetime import date
from entidades.forma_pago import FormaPago
from entidades.tipo_gasto import TipoGasto
from entidades.viaje import Viaje
from entidades.gasto import Gasto
from conversor_moneda import ConversorMoneda

class ControlViaje:
    def __init__(self):
        self.__viajes: list = []

    def obtener_viaje(self):
        for viaje in self.__viajes:
            if viaje.esta_activo():
                return viaje
        
        return None
    
    def agregar_viaje(self, viaje: Viaje):
        self.__viajes.append(viaje)

    def registrar_gasto(self, fecha: date, valor: float, 
                        metodo_pago: FormaPago, tipo_gasto: TipoGasto):
        viaje: Viaje = self.obtener_viaje()

        if viaje is None:
            return Exception
        
        if viaje.get_pais() != "Colombia":
            moneda = viaje.get_moneda()

            tasa = ConversorMoneda.obtener_tasa_cambio(fecha, moneda, "COP")

            valor = valor*tasa

        gasto = Gasto(fecha, valor, metodo_pago, tipo_gasto)

        viaje.guardar_gasto(gasto)

        diferencia = self.obtener_diferencia_presupuesto(fecha, viaje)

        return diferencia

    def obtener_diferencia_presupuesto(self, fecha: date, viaje: Viaje):
        suma_gastos = 0

        for gasto in viaje.__gastos:
            if gasto.get_fecha() == fecha:
                suma_gastos += gasto.get_valor_gastado()

        diferencia = viaje.get_presupuesto_diario() - suma_gastos

        return diferencia   
    