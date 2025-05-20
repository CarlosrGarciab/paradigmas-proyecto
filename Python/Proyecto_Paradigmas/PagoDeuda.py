from Pago import Pago

class PagoDeuda(Pago):
    def __init__(self, cliente, monto):
        super().__init__(monto)
        self._cliente = cliente

    def procesar_pago(self, monto):
        self._cliente.deuda += monto
        print(f"Deuda agregada: S/{monto:.2f} a la cuenta de {self._cliente.nombre}. Deuda actual: S/{self._cliente.deuda:.2f}")
        return True