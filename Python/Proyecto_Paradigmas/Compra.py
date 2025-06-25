class Compra:
    """
    Representa una compra realizada a un proveedor.
    """

    def __init__(self, proveedor, fecha, productos_comprados):
        """
        productos_comprados: diccionario {nombre_producto: (cantidad, precio_compra, disponible)}.
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
                disponible = True  # Por defecto
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