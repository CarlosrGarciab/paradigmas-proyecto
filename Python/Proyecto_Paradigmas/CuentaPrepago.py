class CuentaPrepago:
    """
    Representa una cuenta prepaga asociada a un cliente.
    Permite cargar crédito y descontar saldo.
    """
    def __init__(self, saldo_inicial):
        self._saldo = saldo_inicial

    @property
    def saldo(self):
        """Saldo actual de la cuenta prepaga."""
        return self._saldo

    def cargar_credito(self, valor):
        """Agrega crédito a la cuenta prepaga."""
        if valor < 0:
            raise ValueError("El valor a cargar debe ser positivo.")
        self._saldo += valor

    def descontar(self, valor):
        """Descuenta saldo de la cuenta prepaga."""
        if valor < 0:
            raise ValueError("El valor a descontar debe ser positivo.")
        if valor > self._saldo:
            raise ValueError("No hay suficiente saldo para descontar.")
        self._saldo -= valor

    def tiene_credito(self):
        """Indica si la cuenta prepaga tiene saldo positivo."""
        return self._saldo > 0

    def __str__(self):
        """Representación en texto del saldo prepago."""
        return f"Saldo cuenta prepaga: {self._saldo:.2f}"