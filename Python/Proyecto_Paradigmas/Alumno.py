from Cliente import Cliente

class Alumno(Cliente):
    """
    Representa a un alumno cliente de la cantina.
    Incluye grado y saldo prepago inicial.
    """
    def __init__(self, nombre, grado, saldo_cuenta_prepaga, metodo_pago, caja=None, banco=None):
        """
        Inicializa un alumno con nombre, grado y saldo prepago.
        El saldo prepago se deposita en caja o banco según el método de pago.
        """
        super().__init__(nombre, grado)
        self._saldo_prepago = saldo_cuenta_prepaga

        # Registrar el dinero en la caja o el banco según el método de pago
        if metodo_pago == "caja" and caja:
            caja.dinero += saldo_cuenta_prepaga
        elif metodo_pago == "banco" and banco:
            banco.saldo += saldo_cuenta_prepaga
        else:
            raise ValueError("Método de pago inválido o recursos no proporcionados.")

    @property
    def saldo_prepago(self):
        """Saldo prepago disponible del alumno."""
        return self._saldo_prepago

    @saldo_prepago.setter
    def saldo_prepago(self, nuevo_saldo):
        """ Actualiza el saldo prepago del alumno."""
        self._saldo_prepago = nuevo_saldo