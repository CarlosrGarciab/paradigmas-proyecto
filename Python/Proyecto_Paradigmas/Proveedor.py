class Proveedor:
    """
    Representa un proveedor de la cantina.
    Gestiona nombre, saldo a favor y permite recibir pagos.
    """

    def __init__(self, nombre, contacto="", telefono=""):
        """
        Inicializa un proveedor con un nombre, saldo en 0, contacto y teléfono opcionales.
        """
        self._nombre = nombre
        self._saldo = 0.0
        self.contacto = contacto
        self.telefono = telefono

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