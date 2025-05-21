class Compra:
    """
    Representa una compra realizada a un proveedor.
    Incluye el proveedor, la fecha, los detalles de la compra y el total.
    """
    _id_counter = 1

    def __init__(self, id, proveedor, fecha, detalles):
        """
        Inicializa la compra con proveedor, fecha y detalles.
        """
        self._id = id if id is not None else Compra._id_counter
        Compra._id_counter = max(Compra._id_counter, self._id + 1)
        self._proveedor = proveedor
        self._fecha = fecha
        self._detalles = detalles

    @property
    def id(self):
        """ID único de la compra."""
        return self._id

    @property
    def proveedor(self):
        """Proveedor de la compra."""
        return self._proveedor

    @property
    def fecha(self):
        """Fecha de la compra."""
        return self._fecha

    @property
    def detalles(self):
        """Lista de detalles de la compra."""
        return self._detalles

    @property
    def total(self):
        """Total de la compra (suma de subtotales de los detalles)."""
        return sum(det.subtotal for det in self._detalles)

    def registrar_compra(self, caja, inventario):
        """
        Registra la compra: descuenta el dinero de la caja, paga al proveedor y agrega productos al inventario.
        Lanza un error si no hay suficiente dinero en caja.
        """
        total_compra = self.total
        if caja.dinero < total_compra:
            raise ValueError("No hay suficiente dinero en caja para pagar al proveedor.")
        caja.dinero -= total_compra
        self.proveedor.recibir_pago(total_compra)
        for detalle in self.detalles:
            producto = detalle.producto
            prod_existente = inventario.buscar_producto(producto.id)
            if prod_existente:
                prod_existente.stock += detalle.cantidad
            else:
                producto.stock = detalle.cantidad
                inventario.agregar_producto(producto)
        print(f"Compra registrada y pagada a {self.proveedor.nombre} por S/{total_compra:.2f}")

    def __str__(self):
        """
        Representación en texto de la compra.
        """
        detalles_str = "\n".join(str(det) for det in self._detalles)
        return f"\nProveedor: {self.proveedor.nombre}\nFecha: {self.fecha}\nDetalles:\n{detalles_str}\nTotal: S/{self.total:.2f}"