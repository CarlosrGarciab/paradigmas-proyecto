from Pago import Pago

class PagoEfectivo(Pago):
    """
    Representa un pago realizado en efectivo.
    """
    def __init__(self, caja, monto):
        """
        Inicializa el pago en efectivo con la caja y el monto recibido.
        """
        super().__init__(monto)
        self.caja = caja

    def procesar_pago(self, monto):
        """
        Procesa el pago en efectivo.
        Verifica si el monto recibido es suficiente.
        """
        if monto <= self.monto:
            print(f"Pago en efectivo procesado por S/{monto:.2f}")
            return True
        else:
            print(f"Pago fallido: El cliente no tiene suficiente efectivo. Disponible: S/{self.monto:.2f}, requerido: S/{monto:.2f}")
            return False