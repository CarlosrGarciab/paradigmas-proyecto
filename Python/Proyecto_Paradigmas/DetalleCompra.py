class DetalleCompra:
    """
    Representa el detalle de un producto comprado a un proveedor.
    Incluye el producto, la cantidad, el costo unitario y el subtotal.
    """
    def __init__(self, producto, cantidad, costo_unitario):
        self._producto = producto
        self._cantidad = cantidad
        self._costo_unitario = costo_unitario

    # Getters y Setters
    @property
    def producto(self):
        """Producto comprado."""
        return self._producto

    @property
    def cantidad(self):
        """Cantidad comprada del producto."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, cantidad_nuevo):
        """Permite modificar la cantidad comprada."""
        self._cantidad = cantidad_nuevo

    @property
    def costo_unitario(self):
        """Costo unitario de compra del producto."""
        return self._costo_unitario

    @costo_unitario.setter
    def costo_unitario(self, costo_unitario_nuevo):
        """Permite modificar el costo unitario."""
        self._costo_unitario = costo_unitario_nuevo

    @property
    def subtotal(self):
        """Subtotal de este detalle (cantidad x costo unitario)."""
        return self._cantidad * self._costo_unitario

    # Metodos
    def __str__(self):
        """
        Representación en texto del detalle de compra.
        """
        return f"{self._cantidad} x {self._producto._nombre} a S/{self._costo_unitario:.2f} c/u = S/{self.subtotal:.2f}"