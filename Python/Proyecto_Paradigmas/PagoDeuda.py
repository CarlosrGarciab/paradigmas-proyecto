from Pago import Pago

class PagoDeuda:
    def __init__(self, cliente, monto):
        self._cliente = cliente
        self._monto = monto

    def agregar_deuda(self):
        """Agrega el monto como deuda al cliente."""
        self._cliente.deuda += self._monto
        print(f"Deuda agregada: S/{self._monto:.2f} a la cuenta de {self._cliente.nombre}. Deuda actual: S/{self._cliente.deuda:.2f}")

    def procesar_pago(self):
        """Permite al cliente pagar su deuda."""
        if self._cliente.deuda >= self._monto:
            self._cliente.deuda -= self._monto  # Se descuenta de la deuda
            print(f"Pago de deuda procesado: S/{self._monto:.2f} descontado de la deuda de {self._cliente.nombre}. Deuda actual: S/{self._cliente.deuda:.2f}")
        else:
            # Si la deuda es menor que el monto, no permitir que se procese el pago
            print(f"Pago fallido: La deuda de {self._cliente.nombre} es menor al monto del pago. Deuda actual: S/{self._cliente.deuda:.2f}")