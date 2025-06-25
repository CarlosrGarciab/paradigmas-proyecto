class CuentaBanco:
    """
    Representa la cuenta bancaria de la cantina.
    Permite consultar y modificar el saldo.
    """
    def __init__(self):
        self._saldo = 0

    @property
    def saldo(self):
        """Saldo actual en el banco."""
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        """Permite actualizar el saldo del banco."""
        self._saldo = valor
        
    def ingresar_dinero(self, monto):
        """Agrega dinero al banco."""
        if monto <= 0:
            raise ValueError("El monto a ingresar debe ser positivo.")
        self._saldo += monto

    def retirar_dinero(self, monto):
        """Retira dinero del banco si hay suficiente saldo."""
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser positivo.")
        if monto > self._saldo:
            raise ValueError("No hay suficiente saldo en el banco.")
        self._saldo -= monto