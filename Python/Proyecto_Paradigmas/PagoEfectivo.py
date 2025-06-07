from Pago import Pago

class PagoEfectivo(Pago):
    """
    Representa un pago realizado en efectivo.
    """
    def __init__(self, caja, monto):
        super().__init__(monto)
        self._caja = caja

    @property
    def caja(self):
        """
        Obtiene la caja asociada al pago en efectivo.
        """
        return self._caja

    def procesar_pago(self, monto):
        """
        Procesa el pago en efectivo.
        Verifica si el monto recibido es suficiente.
        """
        return monto <= self.monto