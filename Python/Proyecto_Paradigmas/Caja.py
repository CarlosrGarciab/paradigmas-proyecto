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