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
        Procesa el pago por transferencia, sumando el monto al banco usando la propiedad saldo.
        """
        self._banco.saldo += monto
        return True