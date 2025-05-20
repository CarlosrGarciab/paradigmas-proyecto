class CuentaPrepago:
    """
    Representa una cuenta prepaga asociada a un cliente.
    Permite cargar crédito y descontar saldo.
    """
    def __init__(self, saldo_inicial):
        self.__saldo = saldo_inicial

    @property
    def saldo(self):
        """Saldo actual de la cuenta prepaga."""
        return self.__saldo

    def cargar_credito(self, valor):
        """Agrega crédito a la cuenta prepaga."""
        self.__saldo += valor

    def descontar(self, valor):
        """Descuenta saldo de la cuenta prepaga."""
        self.__saldo -= valor

    def tiene_credito(self):
        """Indica si la cuenta prepaga tiene saldo positivo."""
        return self.__saldo > 0

    def __str__(self):
        """Representación en texto del saldo prepago."""
        return f"Saldo cuenta prepaga: {self.__saldo:.2f}"