"""
Módulo que contiene la clase ControlViaje, la cual permite gestionar viajes, 
registrar gastos y calcular diferencias de presupuesto diarios asociados a un viaje.
"""

from datetime import date

from servicios.conversor_moneda import ConversorMoneda

from entidades.forma_pago import FormaPago
from entidades.tipo_gasto import TipoGasto
from entidades.viaje import Viaje
from entidades.gasto import Gasto


class ControlViaje:
    """
    Clase para gestionar viajes y registrar gastos asociados a ellos.

    paramas __viajes (list): Lista privada que almacena los objetos Viaje registrados.
    """

    def __init__(self):
        self.__viajes: list = []
        self.conversor = ConversorMoneda()

    def obtener_viaje(self, fecha):
        """
        Obtiene el viaje que esté actualmente activo.

        params fecha (date): Fecha para verificar si hay un viaje activo

        Returns Viaje o None: El viaje activo si existe, o None si no hay ninguno activo.
        """
        for viaje in self.__viajes:
            if viaje.esta_activo(fecha):
                return viaje
        
        return None
    
    def agregar_viaje(self, viaje: Viaje):
        """
        Agrega un nuevo viaje a la lista de viajes.
        """
        self.__viajes.append(viaje)

    def registrar_gasto(self, fecha: date, valor: float, 
                        metodo_pago: FormaPago, tipo_gasto: TipoGasto):
        """
        Registra un gasto en el viaje activo. Si el país del viaje no es Colombia,
        convierte el valor del gasto a pesos colombianos usando la tasa de cambio.

        params:
            fecha (date): Fecha en la que se realiza el gasto.
            valor (float): Valor del gasto en la moneda local del viaje.
            metodo_pago (FormaPago): Método de pago utilizado.
            tipo_gasto (TipoGasto): Tipo de gasto realizado.

        Returns:
            float: Diferencia entre el presupuesto diario y la suma de gastos del día.
            Exception: Si no hay viaje activo, retorna una excepción.
        """
        viaje: Viaje = self.obtener_viaje(fecha)
        if viaje is None:
            raise ValueError("No hay un viaje activo")
        
        if viaje.get_pais().lower() != "colombia":
            moneda = viaje.get_moneda()
            tasa = self.conversor.obtener_tasa_cambio(fecha, moneda, moneda_destino="cop")
            valor = valor*tasa

        gasto = Gasto(fecha, valor, metodo_pago, tipo_gasto)
        viaje.guardar_gasto(gasto)
        diferencia = self.obtener_diferencia_presupuesto(fecha, viaje)

        return diferencia

    def obtener_diferencia_presupuesto(self, fecha: date, viaje: Viaje):
        """
        Calcula la diferencia entre el presupuesto diario y la suma de gastos realizados en una fecha específica.

        Args:
            fecha (date): Fecha para la que se calcula la diferencia.
            viaje (Viaje): Instancia del viaje donde se calculan los gastos.

        Returns:
            float: Diferencia entre presupuesto diario y gastos en la fecha dada.
        """
        suma_gastos = 0

        for gasto in viaje.get_gastos():
            if gasto.get_fecha() == fecha:
                suma_gastos += gasto.get_valor_gastado()

        diferencia = viaje.get_presupuesto_diario() - suma_gastos

        return diferencia
    
    def mostrar_gastos_por_dia(self, viaje: Viaje):
        """
        Muestra el valor gastado cada día del viaje, separado por forma de pago (efectivo y tarjeta), y el total diario.

        Param viaje (Viaje): El objeto del viaje para el cual se desea generar el reporte.

        Returns None. Imprime el resumen por consola.
        """
        resumen = {}
        for gasto in viaje.get_gastos():
            fecha = gasto.get_fecha()
            forma_pago = gasto.get_forma_pago()
            valor = gasto.get_valor_gastado()

            if fecha not in resumen:
                resumen[fecha] = {"EFECTIVO": 0.0, "TARJETA": 0.0}

            resumen[fecha][forma_pago.name] += valor

        for fecha, valores in resumen.items():
            total = valores["EFECTIVO"] + valores["TARJETA"]
            print(f"Fecha: {fecha}")
            print(f"  Efectivo: {valores['EFECTIVO']}")
            print(f"  Tarjeta: {valores['TARJETA']}")
            print(f"  Total: {total}")

    def mostrar_gastos_por_tipo(self, viaje: Viaje):
        """
        Muestra el valor gastado en cada tipo de gasto del viaje, separado por forma de pago (efectivo y tarjeta), y el total por tipo.

        Param viaje (Viaje): El objeto del viaje para el cual se desea generar el reporte.

        Return None. Imprime el resumen por consola.
        """
        resumen = {}
        for gasto in viaje.get_gastos():
            tipo = gasto.get_tipo_gasto()
            forma_pago = gasto.get_forma_pago()
            valor = gasto.get_valor_gastado()

            if tipo not in resumen:
                resumen[tipo] = {"EFECTIVO": 0.0, "TARJETA": 0.0}

            resumen[tipo][forma_pago.name] += valor

        for tipo, valores in resumen.items():
            total = valores["EFECTIVO"] + valores["TARJETA"]
            print(f"Tipo de gasto: {tipo.name}")
            print(f"  Efectivo: {valores['EFECTIVO']}")
            print(f"  Tarjeta: {valores['TARJETA']}")
            print(f"  Total: {total}")