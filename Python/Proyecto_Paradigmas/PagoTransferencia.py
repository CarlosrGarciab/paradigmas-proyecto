from Pago import Pago

class PagoTransferencia(Pago):
    def __init__(self, banco, monto):
        super().__init__(monto)
        self._banco = banco

    def procesar_pago(self):
        self._banco.saldo += self._monto
        print(f"Pago por transferencia procesado: S/{self._monto:.2f} agregado al banco.")