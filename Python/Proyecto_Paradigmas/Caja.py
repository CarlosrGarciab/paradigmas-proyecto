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
        """Agrega dinero a la caja."""
        if monto <= 0:
            raise ValueError("El monto a ingresar debe ser positivo.")
        self._dinero += monto

    def retirar_dinero(self, monto):
        """Retira dinero de la caja si hay suficiente saldo."""
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser positivo.")
        if monto > self._dinero:
            raise ValueError("No hay suficiente dinero en la caja.")
        self._dinero -= monto