class DetalleCompra:
    def __init__(self, producto, cantidad, costo_unitario):
        self.__producto = producto
        self.__cantidad = cantidad
        self.__costo_unitario = costo_unitario

    # Producto
    @property
    def producto(self):
        return self.__producto

    # Cantidad
    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad_nuevo):
        self.__cantidad = cantidad_nuevo

    # Costo unitario
    @property
    def costo_unitario(self):
        return self.__costo_unitario

    @costo_unitario.setter
    def costo_unitario(self, costo_unitario_nuevo):
        self.__costo_unitario = costo_unitario_nuevo

    # Subtotal
    @property
    def subtotal(self):
        return self.__cantidad * self.__costo_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} a S/{self.costo_unitario:.2f} c/u = S/{self.subtotal:.2f}"