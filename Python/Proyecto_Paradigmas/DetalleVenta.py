class DetalleVenta:
    """
    Representa el detalle de un producto vendido en una venta.
    Incluye el producto, la cantidad, el precio unitario y el subtotal.
    """
    def __init__(self, producto, cantidad, precio_unitario):
        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario

    @property
    def producto(self):
        """Producto vendido."""
        return self.__producto

    @property
    def cantidad(self):
        """Cantidad vendida del producto."""
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad_nuevo):
        """Permite modificar la cantidad vendida."""
        self.__cantidad = cantidad_nuevo

    @property
    def precio_unitario(self):
        """Precio unitario de venta del producto."""
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, precio_unitario_nuevo):
        """Permite modificar el precio unitario."""
        self.__precio_unitario = precio_unitario_nuevo

    @property
    def subtotal(self):
        """Subtotal de este detalle (cantidad x precio unitario)."""
        return self.__cantidad * self.__precio_unitario

    def __str__(self):
        """
        Representación en texto del detalle de venta.
        """
        return f"{self.cantidad} x {self.producto.nombre} a S/{self.precio_unitario:.2f} c/u = S/{self.subtotal:.2f}"