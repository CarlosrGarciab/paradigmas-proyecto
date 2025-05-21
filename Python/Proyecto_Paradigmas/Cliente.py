from abc import ABC

class Cliente(ABC):
    """
    Clase abstracta base para representar un cliente de la cantina.
    Gestiona nombre, grado y deuda.
    """
    _id_counter = 1  # Variable para autoincremento de IDs

    def __init__(self, nombre, grado):
        """
        Inicializa un cliente con su id, nombre, grado y deuda en 0.
        """
        self._id = Cliente._id_counter
        Cliente._id_counter += 1
        self._nombre = nombre
        self._grado = grado
        self._deuda = 0.0

    # Getters y Setters
    @property
    def id(self):
        """ID unico del cliente."""
        return self._id

    @property
    def nombre(self):
        """Nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Permite cambiar el nombre del cliente."""
        self._nombre = nuevo_nombre

    @property
    def grado(self):
        """Grado del cliente."""
        return self._grado

    @grado.setter
    def grado(self, valor):
        """Permite cambiar el grado del cliente."""
        self._grado = valor

    @property
    def deuda(self):
        """Deuda actual del cliente."""
        return self._deuda

    @deuda.setter
    def deuda(self, valor):
        """Permite actualizar la deuda del cliente."""
        self._deuda = valor

    # Métodos
    def adquirir_deuda(self, monto):
        """
        Suma una nueva deuda al cliente.
        """
        if monto <= 0:
            raise ValueError("El monto de la deuda debe ser positivo.")
        self._deuda += monto
        print(f"Deuda adquirida: S/{monto:.2f}. Deuda actual: S/{self._deuda:.2f}")

    def pagar_deuda(self, monto):
        """
        Permite pagar parte o toda la deuda del cliente.
        """
        if monto <= 0:
            raise ValueError("El monto a pagar debe ser positivo.")
        if monto > self._deuda:
            raise ValueError("El monto a pagar no puede ser mayor que la deuda actual.")
        self._deuda -= monto
        print(f"Deuda pagada: S/{monto:.2f}. Deuda restante: S/{self._deuda:.2f}")

    def __str__(self):
        """
        Representación en texto del cliente.
        """
        return f"Cliente: {self._nombre} - Grado: {self._grado} - Deuda: S/{self._deuda:.2f}"