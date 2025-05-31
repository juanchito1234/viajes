import unittest
from controles.control_viaje import ControlViaje
from entidades.gasto import Gasto
from unittest.mock import MagicMock

class TestControlViaje(unittest.TestCase):
    """
        Pruebas unitarias para el método registrar_gasto de ControlViaje
    """
    def setUp(self):
        self.mock_viaje = MagicMock()
        self.mock_conversor = MagicMock()

        self.control_viaje = ControlViaje()

        self.control_viaje.agregar_viaje(self.viaje)
    
    



