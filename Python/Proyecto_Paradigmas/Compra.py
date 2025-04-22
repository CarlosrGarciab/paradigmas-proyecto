class Compra:
    def __init__(self, id, proveedor, fecha, detalles):
        self.__id = id
        self.__proveedor = proveedor
        self.__fecha = fecha
        self.__detalles = detalles  # Lista de DetalleCompra

    # |--- Getters y Setters ---|
    # Id
    @property
    def id(self):
        return self.__id

    # Proveedor
    @property
    def proveedor(self):
        return self.__proveedor

    @proveedor.setter
    def proveedor(self, proovedor_nuevo):
        self.__proveedor = proovedor_nuevo

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
