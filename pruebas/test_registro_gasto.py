"""
Este módulo contiene pruebas de integración para el método registrar_gasto de la clase ControlViaje.
"""
import unittest

from datetime import date
from unittest.mock import MagicMock

from controles.control_viaje import ControlViaje
from entidades.viaje import Viaje
from entidades.tipo_gasto import TipoGasto
from entidades.forma_pago import FormaPago


class TestRegistrarGasto(unittest.TestCase):
    """
    Pruebas de integración para el método registrar_gasto de ControlViaje.
    """

    def setUp(self):
        self.viaje = None
        self.mock_conversor = MagicMock()
        self.control_viaje = ControlViaje()
        self.control_viaje.conversor = self.mock_conversor

    def test_registrar_gasto_en_moneda_local(self):
        """
        Debe registrar un gasto en moneda local sin conversión de divisas.
        """
        self.viaje = Viaje(
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 10),
            pais="Colombia",
            moneda_iso="COP",
            presupuesto_diario=100.0
        )
        self.control_viaje.agregar_viaje(self.viaje)

        diferencia = self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 3),
            valor=50000,
            metodo_pago=FormaPago.EFECTIVO,
            tipo_gasto=TipoGasto.ALIMENTACION
        )

        self.assertEqual(len(self.viaje.get_gastos()), 1)
        self.assertEqual(self.viaje.get_gastos()[0].get_valor_gastado(), 50000)
        self.assertEqual(self.viaje.get_gastos()[0].get_tipo_gasto(), TipoGasto.ALIMENTACION)
        self.assertEqual(self.viaje.get_gastos()[0].get_forma_pago(), FormaPago.EFECTIVO)
        self.assertEqual(diferencia, 100.0 - 50000)

    def test_registrar_gasto_con_conversion_divisa(self):
        """
        Debe registrar un gasto en moneda extranjera y convertirlo a COP.
        """
        self.viaje = Viaje(
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 10),
            pais="México",
            moneda_iso="MXN",
            presupuesto_diario=100.0
        )
        self.control_viaje.agregar_viaje(self.viaje)

        # suponiendo que 1 MXN son 200 COP
        self.mock_conversor.obtener_tasa_cambio.return_value = 200

        diferencia = self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 4),
            valor=10.0,
            metodo_pago=FormaPago.TARJETA,
            tipo_gasto=TipoGasto.TRANSPORTE
        )

        self.assertEqual(len(self.viaje.get_gastos()), 1)
        self.assertEqual(self.viaje.get_gastos()[0].get_valor_gastado(), 2000)  #10.0 MXN * 210.77062077 = 2107.7062077
        self.assertEqual(self.viaje.get_gastos()[0].get_tipo_gasto(), TipoGasto.TRANSPORTE)
        self.assertEqual(self.viaje.get_gastos()[0].get_forma_pago(), FormaPago.TARJETA)
        self.mock_conversor.obtener_tasa_cambio.assert_called_once()
        self.assertEqual(diferencia, 100.0 - 2000)

    def test_viaje_no_activo(self):
        """
        No debe registrar gasto si el viaje no está activo.
        """
        with self.assertRaises(ValueError):
            self.control_viaje.registrar_gasto(
                fecha=date(2024, 1, 5),
                valor=50,
                metodo_pago=FormaPago.EFECTIVO,
                tipo_gasto=TipoGasto.ALIMENTACION
            )
    
    def test_registrar_multiples_gastos_mismo_dia(self):
        """
        Debe registrar múltiples gastos el mismo día y calcular correctamente la diferencia de presupuesto.
        """
        self.viaje = Viaje(
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 10),
            pais="Colombia",
            moneda_iso="COP",
            presupuesto_diario=100000.0
        )
        self.control_viaje.agregar_viaje(self.viaje)

        self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 5),
            valor=30000,
            metodo_pago=FormaPago.EFECTIVO,
            tipo_gasto=TipoGasto.ALIMENTACION
        )

        diferencia = self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 5),
            valor=45000,
            metodo_pago=FormaPago.TARJETA,
            tipo_gasto=TipoGasto.ENTRETENIMIENTO
        )

        self.assertEqual(len(self.viaje.get_gastos()), 2)
        self.assertEqual(diferencia, 100000.0 - (30000 + 45000))
        self.assertEqual(self.viaje.get_gastos()[0].get_tipo_gasto(), TipoGasto.ALIMENTACION)
        self.assertEqual(self.viaje.get_gastos()[0].get_forma_pago(), FormaPago.EFECTIVO)
        self.assertEqual(self.viaje.get_gastos()[1].get_tipo_gasto(), TipoGasto.ENTRETENIMIENTO)
        self.assertEqual(self.viaje.get_gastos()[1].get_forma_pago(), FormaPago.TARJETA)

    def test_registrar_gastos_en_dias_diferentes(self):
        """
        Debe registrar gastos en días distintos con conversión de ARS a COP.
        """
        self.viaje = Viaje(
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 10),
            pais="Argentina",
            moneda_iso="ARS",
            presupuesto_diario=1000.0
        )
        self.control_viaje.agregar_viaje(self.viaje)

        # Suponiendo que 1 ARS son 3 COP
        self.mock_conversor.obtener_tasa_cambio.return_value = 3.0

        diferencia_dia1 = self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 3),
            valor=50.0,
            metodo_pago=FormaPago.EFECTIVO,
            tipo_gasto=TipoGasto.ALIMENTACION
        )

        diferencia_dia2 = self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 4),
            valor=100.0,
            metodo_pago=FormaPago.TARJETA,
            tipo_gasto=TipoGasto.ENTRETENIMIENTO
        )

        self.assertEqual(len(self.viaje.get_gastos()), 2)
        self.assertEqual(diferencia_dia1, 1000.0 - 150.0)
        self.assertEqual(diferencia_dia2, 1000.0 - 300.0)
        self.assertEqual(self.viaje.get_gastos()[0].get_forma_pago(), FormaPago.EFECTIVO)
        self.assertEqual(self.viaje.get_gastos()[0].get_valor_gastado(), 150.0)
        self.assertEqual(self.viaje.get_gastos()[1].get_valor_gastado(), 300.0)
        self.assertEqual(self.viaje.get_gastos()[1].get_tipo_gasto(), TipoGasto.ENTRETENIMIENTO)
        self.assertEqual(self.mock_conversor.obtener_tasa_cambio.call_count, 2)