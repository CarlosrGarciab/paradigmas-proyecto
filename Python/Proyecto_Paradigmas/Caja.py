class Caja:
    """
    Representa la caja de la cantina.
    Permite ingresar dinero y consultar el saldo.
    """
    def __init__(self):
        self._dinero = 0

    @property
    def dinero(self):
        """Saldo actual en la caja."""
        return self._dinero

    @dinero.setter
    def dinero(self, valor):
        """Permite actualizar el saldo de la caja."""
        self._dinero = valor

    def ingresar_dinero(self, monto):
        """
        Agrega dinero a la caja.
        """
        if monto < 0:
            raise ValueError("El monto a ingresar no puede ser negativo.")
        self._dinero += monto

    def __str__(self):
        """
        Representación en texto del saldo en caja.
        """
        return f"Dinero en caja: S/{self._dinero:.2f}"