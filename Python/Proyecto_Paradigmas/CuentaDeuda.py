class CuentaDeuda:
    """
    Representa una cuenta de deuda asociada a un cliente.
    Permite sumar deuda y pagarla.
    """
    def __init__(self, deuda):
        self._deuda = deuda

    @property
    def deuda(self):
        """Deuda actual de la cuenta."""
        return self._deuda

    def sumar_deuda(self, valor):
        """Agrega un monto a la deuda."""
        if valor < 0:
            raise ValueError("El valor a sumar debe ser positivo.")
        self._deuda += valor

    def pagar(self, valor):
        """Reduce la deuda al pagar un monto."""
        if valor < 0:
            raise ValueError("El valor a pagar debe ser positivo.")
        if valor > self._deuda:
            raise ValueError("No se puede pagar más de la deuda actual.")
        self._deuda -= valor

    def tiene_deuda(self):
        """Indica si la cuenta tiene deuda pendiente."""
        return self._deuda > 0

    def __str__(self):
        """Representación en texto de la deuda."""
        return f"Deuda actual: {self._deuda:.2f}"