from Pago import Pago

class PagoEfectivo(Pago):
    def __init__(self, caja, monto):
        super().__init__(monto)
        self.caja = caja

    def procesar_pago(self, monto):
        """
        Procesa el pago en efectivo.
        """
        if monto <= self.monto:
            print(f"Pago en efectivo procesado por S/{monto:.2f}")
            return True
        else:
            print(f"Pago fallido: El cliente no tiene suficiente efectivo. Disponible: S/{self.monto:.2f}, requerido: S/{monto:.2f}")
            return False