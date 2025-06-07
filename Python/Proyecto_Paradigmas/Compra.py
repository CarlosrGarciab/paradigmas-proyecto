class Compra:
    """
    Representa una compra realizada a un proveedor.
    """
    _id_counter = 1

    def __init__(self, proveedor, fecha, productos_comprados):
        """
        productos_comprados: diccionario {nombre_producto: (cantidad, precio_compra)}
        """
        self._id = Compra._id_counter
        Compra._id_counter += 1

        self._proveedor = proveedor
        self._fecha = fecha
        # Guardar solo datos simples: nombre del producto, cantidad, precio
        self._productos_comprados = {}  # {str: (cantidad, precio_compra)}
        for nombre_producto, (cantidad, precio_compra) in productos_comprados.items():
            self._productos_comprados[nombre_producto] = (cantidad, precio_compra)
        self._total = self.calcular_total()

    @property
    def id(self):
        return self._id

    @property
    def proveedor(self):
        return self._proveedor

    @property
    def fecha(self):
        return self._fecha

    @property
    def productos_comprados(self):
        return self._productos_comprados

    @property
    def total(self):
        return self._total

    def calcular_total(self):
        return sum(cantidad * precio_compra for _, (cantidad, precio_compra) in self._productos_comprados.items())

    def __str__(self):
        detalles = "\n".join(
            f"{nombre} x {cantidad} = S/{precio_compra * cantidad:.2f} (Compra: S/{precio_compra:.2f})"
            for nombre, (cantidad, precio_compra) in self._productos_comprados.items()
        )
        return f"ID Compra: {self._id}\nProveedor: {self._proveedor.nombre}\nFecha: {self._fecha}\nProductos comprados:\n{detalles}\nTotal: S/{self._total:.2f}"