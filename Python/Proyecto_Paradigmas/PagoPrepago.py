from Pago import Pago

class PagoPrepago(Pago):
    """
    Representa un pago realizado con saldo prepago de un alumno.
    """
    def __init__(self, alumno, monto):
        super().__init__(monto)
        self._alumno = alumno

    def procesar_pago(self, monto):
        """
        Procesa el pago con saldo prepago, descontando el monto del saldo del alumno.
        """
        if self._alumno.saldo_prepago < monto:
            raise ValueError("Saldo prepago insuficiente.")
        self._alumno.saldo_prepago -= monto
        return True