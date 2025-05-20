from abc import ABC

class Cliente(ABC):
    """
    Clase abstracta base para representar un cliente de la cantina.
    Gestiona nombre, saldo prepago y deuda.
    """
    _id_counter = 1  # Variable de clase para autoincremento de IDs

    def __init__(self, nombre):
        """
        Inicializa un cliente con nombre, saldo prepago y deuda en 0.
        """
        self._id = Cliente._id_counter
        Cliente._id_counter += 1
        self._nombre = nombre
        self._saldo_prepago = 0.0
        self._deuda = 0.0

    # Id
    @property
    def id(self):
        """ID único del cliente (solo lectura)."""
        return self._id

    # Nombre
    @property
    def nombre(self):
        """Nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Permite cambiar el nombre del cliente."""
        self._nombre = nuevo_nombre

    # Saldo prepago
    @property
    def saldo_prepago(self):
        """Saldo prepago disponible del cliente."""
        return self._saldo_prepago

    @saldo_prepago.setter
    def saldo_prepago(self, nuevo_saldo):
        """Permite actualizar el saldo prepago del cliente."""
        if nuevo_saldo < 0:
            raise ValueError("El saldo prepago no puede ser negativo.")
        self._saldo_prepago = nuevo_saldo

    def recargar_saldo(self, monto, caja=None, banco=None):
        """
        Recarga saldo en la cuenta prepaga del cliente.
        El dinero debe ser registrado en la caja o en el banco.
        """
        if monto <= 0:
            raise ValueError("El monto de recarga debe ser positivo.")
        if caja:
            caja.ingresar_dinero(monto)
        elif banco:
            banco.ingresar_dinero(monto)
        else:
            raise ValueError("Debe especificar si el dinero proviene de la caja o del banco.")
        self._saldo_prepago += monto
        print(f"Saldo recargado: S/{monto:.2f}. Saldo actual: S/{self._saldo_prepago:.2f}")

    # Deuda
    @property
    def deuda(self):
        """Deuda actual del cliente."""
        return self._deuda

    @deuda.setter
    def deuda(self, valor):
        """Permite actualizar la deuda del cliente."""
        self._deuda = valor

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
        Representación en texto del cliente (sin mostrar el ID).
        """
        return f"Cliente: {self.nombre} - Saldo prepago: S/{self.saldo_prepago:.2f} - Deuda: S/{self.deuda:.2f}"