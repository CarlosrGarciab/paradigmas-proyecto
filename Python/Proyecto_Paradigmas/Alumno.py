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
        """Permite actualizar el saldo prepago del alumno."""
        if nuevo_saldo < 0:
            raise ValueError("El saldo prepago no puede ser negativo.")
        self._saldo_prepago = nuevo_saldo

    def recargar_cuenta_prepaga(self, monto, caja=None, banco=None):
        """
        Recarga saldo en la cuenta prepaga del alumno.
        El dinero debe ser registrado en la caja o en el banco.
        """
        if monto <= 0:
            raise ValueError("El monto de recarga debe ser positivo.")
        if caja:
            caja.dinero += monto
        elif banco:
            banco.saldo += monto
        else:
            raise ValueError("Debe especificar si el dinero proviene de la caja o del banco.")
        self._saldo_prepago += monto
        
    def __str__(self):
        """
        Representación en texto del alumno.
        """
        return (
            f"Nombre: {self._nombre}\n"
            f"Grado: {self._grado}\n"
            f"Saldo Cuenta Prepaga: {self._saldo_prepago:.2f}\n"
            f"Deuda: {self._deuda:.2f}"
        )