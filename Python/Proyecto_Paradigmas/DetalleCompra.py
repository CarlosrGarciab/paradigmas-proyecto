class DetalleCompra:
    """
    Representa el detalle de un producto comprado a un proveedor.
    Incluye el producto, la cantidad, el costo unitario y el subtotal.
    """
    def __init__(self, producto, cantidad, costo_unitario):
        self.__producto = producto
        self.__cantidad = cantidad
        self.__costo_unitario = costo_unitario

    # Producto
    @property
    def producto(self):
        """Producto comprado."""
        return self.__producto

    # Cantidad
    @property
    def cantidad(self):
        """Cantidad comprada del producto."""
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad_nuevo):
        """Permite modificar la cantidad comprada."""
        self.__cantidad = cantidad_nuevo

    # Costo unitario
    @property
    def costo_unitario(self):
        """Costo unitario de compra del producto."""
        return self.__costo_unitario

    @costo_unitario.setter
    def costo_unitario(self, costo_unitario_nuevo):
        """Permite modificar el costo unitario."""
        self.__costo_unitario = costo_unitario_nuevo

    # Subtotal
    @property
    def subtotal(self):
        """Subtotal de este detalle (cantidad x costo unitario)."""
        return self.__cantidad * self.__costo_unitario

    def __str__(self):
        """
        Representación en texto del detalle de compra.
        """
        return f"{self.cantidad} x {self.producto.nombre} a S/{self.costo_unitario:.2f} c/u = S/{self.subtotal:.2f}"