class Proveedor:
    _id_counter = 1

    def __init__(self, nombre):
        self._id = Proveedor._id_counter
        Proveedor._id_counter += 1
        self._nombre = nombre
        self._saldo = 0.0  # Saldo a favor del proveedor (por cobrar)

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    @property
    def saldo(self):
        return self._saldo

    def recibir_pago(self, monto):
        if monto < 0:
            raise ValueError("El monto a pagar no puede ser negativo.")
        self._saldo += monto

    def __str__(self):
        return f"Proveedor: {self.nombre} (ID: {self.id}) - Saldo por cobrar: S/{self.saldo:.2f}"