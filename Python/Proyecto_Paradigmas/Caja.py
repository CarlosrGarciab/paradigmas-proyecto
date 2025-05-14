class Caja:
    def __init__(self):
        self.dinero = 0.0  # Inicializar el dinero en la caja

    def ingresar_dinero(self, monto):
        """Agrega dinero a la caja."""
        if monto < 0:
            raise ValueError("El monto a ingresar no puede ser negativo.")
        self.dinero += monto

    def __str__(self):
        return f"Dinero en caja: S/{self.dinero:.2f}"