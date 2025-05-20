class CuentaBanco:
    def __init__(self):
        self._saldo = 0

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    def __str__(self):
        return f"Dinero en banco: S/{self.saldo:.2f}"