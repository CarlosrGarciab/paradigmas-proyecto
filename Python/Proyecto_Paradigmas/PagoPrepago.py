from Pago import Pago

class PagoPrepago(Pago):
    def __init__(self, cliente, monto):
        super().__init__(monto)
        self._cliente = cliente

    def procesar_pago(self):
        self._cliente.recargar_cuenta_prepaga(-self._monto)  # Usamos el método para restar el monto
        print(f"Pago de prepago procesado: S/{self._monto:.2f} descontado de la cuenta prepaga de {self._cliente.nombre}.")
