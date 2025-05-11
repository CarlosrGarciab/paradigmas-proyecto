from Pago import Pago

class PagoEfectivo(Pago):
    def __init__(self, caja, monto):
        super().__init__(monto)
        self._caja = caja

    def procesar_pago(self):
        self._caja.dinero += self._monto
        print(f"Pago en efectivo procesado: S/{self._monto:.2f} agregado a la caja.")
