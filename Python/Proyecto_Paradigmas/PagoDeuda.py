from Pago import Pago

class PagoDeuda:
    def __init__(self, cliente, monto):
        self._cliente = cliente
        self._monto = monto

    def procesar_pago(self):
        # Verificar si la deuda es suficiente
        if self._cliente.deuda >= self._monto:
            self._cliente.deuda -= self._monto  # Se descuenta de la deuda
            print(f"Pago de deuda procesado: S/{self._monto:.2f} descontado de la deuda de {self._cliente.nombre}.")
        else:
            # Si la deuda es menor que el monto, no permitir que se procese el pago
            print(f"Pago fallido: La deuda de {self._cliente.nombre} es menor al monto del pago.")
