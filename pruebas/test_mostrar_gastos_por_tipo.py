"""
Este módulo contiene pruebas de integración para el método obtener_diferencia_presupuesto de la clase ControlViaje.
"""
import unittest

from datetime import date
from unittest.mock import MagicMock

from controles.control_viaje import ControlViaje
from entidades.viaje import Viaje
from entidades.tipo_gasto import TipoGasto
from entidades.forma_pago import FormaPago


class TestMostrarGastosPorTipo(unittest.TestCase):
    """
    Pruebas de integración para el método obtener_diferencia_presupuesto de ControlViaje.
    """

    def setUp(self):
        self.viaje = None
        self.mock_conversor = MagicMock()
        self.control_viaje = ControlViaje()
        self.control_viaje.conversor = self.mock_conversor

    def test_mostrar_gastos_por_un_solo_tipo(self):
        """
        Se registran gastos de un solo tipo y se verifica que se 
        guarde correctamente y la totalidad de los gastos sea de ese tipo.
        """

        self.viaje = Viaje(
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 10),
            pais="Colombia",
            moneda_iso="COP",
            presupuesto_diario=100000
        )

        self.control_viaje.agregar_viaje(self.viaje)

        self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 1),
            valor=50000,
            metodo_pago=FormaPago.EFECTIVO,
            tipo_gasto=TipoGasto.ALIMENTACION
        )

        resultado = self.control_viaje.mostrar_gastos_por_tipo(self.viaje)

        self.assertEqual(len(resultado), 1)
        self.assertIn(TipoGasto.ALIMENTACION, resultado)
        self.assertEqual(resultado[TipoGasto.ALIMENTACION]["EFECTIVO"], 50000)

    def test_mostrar_gastos_por_varios_tipos(self):
        """
        Se registran gastos de varios tipos y se verifica que cada
        uno se guarde correctamente y la totalidad de los gastos sean
        la suma de los de cada tipo.
        """

        self.viaje = Viaje(
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 1, 10),
            pais="Colombia",
            moneda_iso="COP",
            presupuesto_diario=100.0
        )

        self.control_viaje.agregar_viaje(self.viaje)

        self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 1),
            valor=50000,
            metodo_pago=FormaPago.EFECTIVO,
            tipo_gasto=TipoGasto.ALIMENTACION
        )

        self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 2),
            valor=50000,
            metodo_pago=FormaPago.EFECTIVO,
            tipo_gasto=TipoGasto.ALOJAMIENTO
        )

        self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 2),
            valor=50000,
            metodo_pago=FormaPago.EFECTIVO,
            tipo_gasto=TipoGasto.COMPRAS
        )

        resultado = self.control_viaje.mostrar_gastos_por_tipo(self.viaje)

        self.assertEqual(len(resultado), 3)
        self.assertIn(TipoGasto.ALIMENTACION, resultado)
        self.assertIn(TipoGasto.ALOJAMIENTO, resultado)
        self.assertIn(TipoGasto.COMPRAS, resultado)
        self.assertEqual(resultado[TipoGasto.ALIMENTACION]["EFECTIVO"] +
                         resultado[TipoGasto.ALOJAMIENTO]["EFECTIVO"] +
                         resultado[TipoGasto.COMPRAS]["EFECTIVO"], 150000)
    
    def test_mostrar_gastos_con_varias_formas_de_pago(self):
        """
        Se registran gastos de un mismo tipo con varias formas de pago y se
        verifica que se sume correctamente.
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

        self.control_viaje.registrar_gasto(
            fecha=date(2025, 1, 5),
            valor=30000,
            metodo_pago=FormaPago.TARJETA,
            tipo_gasto=TipoGasto.ALIMENTACION
        )

        resultado = self.control_viaje.mostrar_gastos_por_tipo(self.viaje)

        self.assertEqual(len(resultado), 1)
        self.assertIn(TipoGasto.ALIMENTACION, resultado)
        self.assertEqual(resultado[TipoGasto.ALIMENTACION]["EFECTIVO"] +
                         resultado[TipoGasto.ALIMENTACION]["TARJETA"], 60000)
