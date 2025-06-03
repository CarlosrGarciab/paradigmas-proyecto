from DetalleCompra import DetalleCompra

class Compra:
    """
    Representa una compra realizada a un proveedor.
    Incluye el proveedor, la fecha, los detalles de la compra y el total.
    """
    _id_counter = 1  # Variable para autoincremento de IDs

    def __init__(self, proveedor, fecha, productos_comprados):
        """
        Inicializa la compra con su id, proveedor, fecha y productos_comprados.
        productos_comprados: diccionario con nombre_producto como clave y tupla (producto, cantidad, precio_compra, disponible_venta) como valor.
        """
        self._id = Compra._id_counter
        Compra._id_counter += 1
        self._proveedor = proveedor
        self._fecha = fecha
        self._detalles = []
        for producto, cantidad, precio_compra, _ in productos_comprados.values():
            # Si el producto es None (insumo no para la venta), crea un detalle con nombre genérico
            if producto is None:
                class Insumo:
                    def __init__(self, nombre):
                        self._nombre = nombre
                insumo = Insumo("INSUMO")
                self._detalles.append(DetalleCompra(insumo, cantidad, precio_compra))
            else:
                self._detalles.append(DetalleCompra(producto, cantidad, precio_compra))

    # Getters
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

    # Metodos
    def registrar_compra(self, caja, inventario):
        """
        Registra la compra: descuenta el dinero de la caja, paga al proveedor y agrega productos al inventario.
        Solo agrega al inventario los productos que no son insumos (producto no es None).
        """
        total_compra = self.total
        if caja._dinero < total_compra:
            raise ValueError("No hay suficiente dinero en caja para pagar al proveedor.")
        caja._dinero -= total_compra
        self._proveedor.recibir_pago(total_compra)
        for detalle in self._detalles:
            producto = detalle.producto
            # Solo agregar al inventario si el producto no es un insumo genérico
            if hasattr(producto, "_id"):
                prod_existente = inventario.buscar_producto(producto._id)
                if prod_existente:
                    prod_existente._stock += detalle._cantidad
                else:
                    producto._stock = detalle._cantidad
                    inventario.agregar_producto(producto)
        print(f"Compra registrada y pagada a {self._proveedor._nombre} por S/{total_compra:.2f}")

    def __str__(self):
        """
        Representación en texto de la compra.
        """
        detalles_str = "\n".join(str(det) for det in self._detalles)
        return f"ID Compra: {self._id}\nProveedor: {self._proveedor._nombre}\nFecha: {self._fecha}\nDetalles:\n{detalles_str}\nTotal: S/{self.total:.2f}"