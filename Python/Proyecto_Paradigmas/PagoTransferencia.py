from Pago import Pago

class PagoTransferencia(Pago):
    """
    Representa un pago realizado por transferencia bancaria.
    """
    def __init__(self, banco, monto):
        """
        Inicializa el pago por transferencia con el banco y el monto.
        """
        super().__init__(monto)
        self._banco = banco

    def procesar_pago(self, monto):
        """
        Procesa el pago por transferencia, sumando el monto al banco.
        """
        self._banco.saldo += monto
        print(f"Pago por transferencia procesado: S/{monto:.2f} agregado al banco.")
        return True