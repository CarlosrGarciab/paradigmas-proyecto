class CuentaDeuda:
    """
    Representa una cuenta de deuda asociada a un cliente.
    Permite sumar deuda y pagarla.
    """
    def __init__(self, deuda):
        self.__deuda = deuda

    @property
    def deuda(self):
        """Deuda actual de la cuenta."""
        return self.__deuda

    def sumar_deuda(self, valor):
        """Agrega un monto a la deuda."""
        self.__deuda += valor

    def pagar(self, valor):
        """Reduce la deuda al pagar un monto."""
        self.__deuda -= valor

    def tiene_deuda(self):
        """Indica si la cuenta tiene deuda pendiente."""
        return self.__deuda > 0

    def __str__(self):
        """Representación en texto de la deuda."""
        return f"Deuda actual: {self.__deuda:.2f}"