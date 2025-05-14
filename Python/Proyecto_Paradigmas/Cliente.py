from abc import ABC

class Cliente(ABC):
    _id_counter = 1  # Variable de clase para autoincremento

    def __init__(self, nombre):
        self._id = Cliente._id_counter
        Cliente._id_counter += 1
        self._nombre = nombre
        self._saldo_prepago = 0.0
        self._deuda = 0.0

    # Id
    @property
    def id(self):
        return self._id

    # Nombre
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    # Saldo prepago
    @property
    def saldo_prepago(self):
        return self._saldo_prepago

    @saldo_prepago.setter
    def saldo_prepago(self, nuevo_saldo):
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
        
        # Registrar el dinero en la caja o el banco
        if caja:
            caja.ingresar_dinero(monto)
        elif banco:
            banco.ingresar_dinero(monto)
        else:
            raise ValueError("Debe especificar si el dinero proviene de la caja o del banco.")
        
        # Recargar el saldo prepago
        self._saldo_prepago += monto
        print(f"Saldo recargado: S/{monto:.2f}. Saldo actual: S/{self._saldo_prepago:.2f}")

    # Deuda
    @property
    def deuda(self):
        return self._deuda

    def adquirir_deuda(self, monto):
        if monto <= 0:
            raise ValueError("El monto de la deuda debe ser positivo.")
        self._deuda += monto
        print(f"Deuda adquirida: S/{monto:.2f}. Deuda actual: S/{self._deuda:.2f}")

    def pagar_deuda(self, monto):
        if monto <= 0:
            raise ValueError("El monto a pagar debe ser positivo.")
        if monto > self._deuda:
            raise ValueError("El monto a pagar no puede ser mayor que la deuda actual.")
        self._deuda -= monto
        print(f"Deuda pagada: S/{monto:.2f}. Deuda restante: S/{self._deuda:.2f}")

    def __str__(self):
        return f"Cliente: {self.nombre} (ID: {self.id}) - Saldo prepago: S/{self.saldo_prepago:.2f} - Deuda: S/{self.deuda:.2f}"