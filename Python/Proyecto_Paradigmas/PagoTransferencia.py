from Pago import Pago

class PagoTransferencia(Pago):
    def __init__(self, banco, monto):
        super().__init__(monto)
        self._banco = banco

    def procesar_pago(self, monto):
        self._banco.saldo += monto
        print(f"Pago por transferencia procesado: S/{monto:.2f} agregado al banco.")
        return True