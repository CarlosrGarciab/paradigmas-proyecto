class Compra:
    """
    Representa una compra realizada a un proveedor.
    """

    def __init__(self, proveedor, fecha, productos_comprados):
        """
        productos_comprados: diccionario {nombre_producto: (cantidad, precio_compra, disponible)}
        El tercer valor (disponible) es opcional (por compatibilidad).
        """
        self._proveedor = proveedor
        self._fecha = fecha
        # Guardar datos: nombre del producto, cantidad, precio, disponible (bool)
        self._productos_comprados = {}  # {str: (cantidad, precio_compra, disponible)}
        for nombre_producto, datos in productos_comprados.items():
            if len(datos) == 3:
                cantidad, precio_compra, disponible = datos
            else:
                cantidad, precio_compra = datos
                disponible = True  # Por defecto, para compatibilidad
            self._productos_comprados[nombre_producto] = (cantidad, precio_compra, disponible)
        self._total = self.calcular_total()

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
        return sum(cantidad * precio_compra for _, (cantidad, precio_compra, _) in self._productos_comprados.items())

    def __str__(self):
        detalles = []
        for nombre, datos in self._productos_comprados.items():
            if len(datos) == 3:
                cantidad, precio_compra, _ = datos  # ignorar disponible
            else:
                cantidad, precio_compra = datos
            linea = f"{nombre} x {cantidad} = S/{precio_compra * cantidad:.2f} (Compra: S/{precio_compra:.2f})"
            detalles.append(linea)
        return f"Proveedor: {self._proveedor.nombre}\nFecha: {self._fecha}\nProductos comprados:\n" + "\n".join(detalles) + f"\nTotal: S/{self._total:.2f}"