from abc import ABC, abstractmethod

class Pago(ABC):
    """
    Clase abstracta base para representar un método de pago.
    """
    def __init__(self, monto):
        """
        Inicializa el pago con el monto correspondiente.
        """
        self._monto = monto

    # Getters y Setters
    @property
    def monto(self):
        """Monto del pago."""
        return self._monto

    @monto.setter
    def monto(self, monto_nuevo):
        """Permite actualizar el monto del pago."""
        self._monto = monto_nuevo

    # Métodos abstractos
    @abstractmethod
    def procesar_pago(self, monto):
        """
        Procesa el pago por el monto indicado.
        Debe ser implementado por las subclases.
        """
        pass