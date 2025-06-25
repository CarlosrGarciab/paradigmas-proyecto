class CuentaBanco:
    """
    Representa la cuenta bancaria de la cantina.
    Permite consultar y modificar el saldo.
    """
    def __init__(self):
        self._saldo = 0

    # Getters y Setters
    @property
    def saldo(self):
        """Saldo actual en el banco."""
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        """Permite actualizar el saldo del banco."""
        self._saldo = valor