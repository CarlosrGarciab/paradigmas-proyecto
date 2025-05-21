from Pago import Pago

class PagoPrepago(Pago):
    """
    Representa un pago realizado usando el saldo prepago de un cliente.
    """
    def __init__(self, cliente, monto):
        """
        Inicializa el pago prepago con el cliente y el monto.
        """
        super().__init__(monto)
        self._cliente = cliente

    def procesar_pago(self, monto):
        """
        Procesa el pago prepago, descontando el monto del saldo prepago del cliente.
        """
        if self._cliente.saldo_prepago >= monto:
            self._cliente.saldo_prepago -= monto
            print(f"Pago prepago procesado: S/{monto:.2f} descontado del saldo prepago de {self._cliente.nombre}.")
            return True
        else:
            print("Saldo prepago insuficiente.")
            return False