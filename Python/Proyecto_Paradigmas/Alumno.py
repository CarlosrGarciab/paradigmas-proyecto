from Cliente import Cliente

class Alumno(Cliente):
    def __init__(self, id_cliente, nombre, grado, saldo_cuenta_prepaga):
        super().__init__(id_cliente, nombre)
        self._grado = grado
        self._saldo_cuenta_prepaga = saldo_cuenta_prepaga

    @property
    def grado(self):
        return self._grado

    @grado.setter
    def grado(self, valor):
        self._grado = valor

    @property
    def prepago(self):
        return self._saldo_cuenta_prepaga

    @prepago.setter
    def prepago(self, valor):
        self._saldo_cuenta_prepaga = valor

    def recargar_cuenta_prepaga(self, valor):
        self._saldo_cuenta_prepaga += valor

    def __str__(self):
        return (
            f"Nombre: {self.nombre}\n"
            f"ID: {self.id}\n"
            f"Grado: {self.grado}\n"
            f"Saldo Cuenta Prepaga: {self._saldo_cuenta_prepaga:.2f}"
        )