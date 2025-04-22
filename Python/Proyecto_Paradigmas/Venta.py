class Venta:
    def __init__(self, id, usuario, fecha, detalles):
        self.__id = id
        self.__usuario = usuario
        self.__fecha = fecha
        self.__detalles = detalles  # Lista de DetalleVenta

    # |--- Getters ---|
    # Id
    @property
    def id(self):
        return self.__id

    # Usuario
    @property
    def usuario(self):
        return self.__usuario

    # Fecha
    @property
    def fecha(self):
        return self.__fecha

    # Detalles
    @property
    def detalles(self):
        return self.__detalles

    # Total
    @property
    def total(self):
        return sum(det.subtotal for det in self.__detalles)
