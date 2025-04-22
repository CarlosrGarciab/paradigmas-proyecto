class DetalleVenta:
    def __init__(self, producto, cantidad, precio_unitario):
        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario

    # |--- Getters y Setters ---|
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

    # Precio unitario
    @property
    def precio_unitario(self):
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, precio_unitario_nuevo):
        self.__precio_unitario = precio_unitario_nuevo

    # Subtotal
    @property
    def subtotal(self):
        return self.__cantidad * self.__precio_unitario
