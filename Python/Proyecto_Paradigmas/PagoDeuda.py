from Pago import Pago

class PagoDeuda(Pago):
    """
    Representa un pago realizado a crédito (deuda) por un cliente.
    """
    def __init__(self, cliente, monto):
        super().__init__(monto)
        self._cliente = cliente

    def procesar_pago(self, monto):
        """
        Procesa el pago por deuda, sumando el monto a la deuda del cliente usando la propiedad deuda.
        """
        self._cliente.deuda += monto
        return True