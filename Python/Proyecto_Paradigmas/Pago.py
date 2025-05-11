from abc import ABC, abstractmethod

class Pago(ABC):
    def __init__(self, monto):
        self._monto = monto

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, monto_nuevo):
        self._monto = monto_nuevo

    @abstractmethod
    def procesar_pago(self):
        pass
