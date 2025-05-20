class DetalleVenta:
    def __init__(self, producto, cantidad, precio_unitario):
        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario

    @property
    def producto(self):
        return self.__producto

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad_nuevo):
        self.__cantidad = cantidad_nuevo

    @property
    def precio_unitario(self):
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, precio_unitario_nuevo):
        self.__precio_unitario = precio_unitario_nuevo

    @property
    def subtotal(self):
        return self.__cantidad * self.__precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} a S/{self.precio_unitario:.2f} c/u = S/{self.subtotal:.2f}"