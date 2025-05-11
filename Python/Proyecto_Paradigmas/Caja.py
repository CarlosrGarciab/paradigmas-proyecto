class Caja:
    def __init__(self):
        self._dinero = 0

    @property
    def dinero(self):
        return self._dinero

    @dinero.setter
    def dinero(self, valor):
        self._dinero = valor