from Pago import Pago

class PagoDeuda(Pago):
    """
    Representa un pago realizado a crédito (deuda) por un cliente.
    """
    def __init__(self, cliente, monto):
        """
        Inicializa el pago por deuda con el cliente y el monto.
        """
        super().__init__(monto)
        self._cliente = cliente

    def procesar_pago(self, monto):
        """
        Procesa el pago por deuda, sumando el monto a la deuda del cliente.
        """
        self._cliente.deuda += monto
        print(f"Deuda agregada: S/{monto:.2f} a la cuenta de {self._cliente.nombre}. Deuda actual: S/{self._cliente.deuda:.2f}")
        return True