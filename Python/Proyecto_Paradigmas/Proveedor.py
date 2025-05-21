class Proveedor:
    """
    Representa un proveedor de la cantina.
    Gestiona nombre, saldo a favor y permite recibir pagos.
    """
    _id_counter = 1

    def __init__(self, nombre):
        """
        Inicializa un proveedor con un nombre y saldo en 0.
        """
        self._id = Proveedor._id_counter
        Proveedor._id_counter += 1
        self._nombre = nombre
        self._saldo = 0.0

    # Getters y Setters
    @property
    def id(self):
        """ID único del proveedor."""
        return self._id

    @property
    def nombre(self):
        """Nombre del proveedor."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Permite cambiar el nombre del proveedor."""
        self._nombre = nuevo_nombre

    @property
    def saldo(self):
        """Saldo a favor del proveedor."""
        return self._saldo

    # Metodos
    def recibir_pago(self, monto):
        """
        Suma un pago al saldo del proveedor.
        Lanza un error si el monto es negativo.
        """
        if monto < 0:
            raise ValueError("El monto a pagar no puede ser negativo.")
        self._saldo += monto

    def __str__(self):
        """
        Representación en texto del proveedor.
        """
        return f"Proveedor: {self._nombre} - Se le Pago: S/{self._saldo:.2f}"