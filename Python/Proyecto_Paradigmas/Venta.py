from PagoEfectivo import PagoEfectivo

class Venta:
    """
    Representa una venta realizada en la cantina.
    Incluye los productos vendidos, el método de pago, el inventario, la caja y el cliente.
    """

    def __init__(self, productos_vendidos, metodo_pago, inventario, caja, cliente=None, fecha=None):
        """
        productos_vendidos: diccionario con nombre_producto como clave y cantidad como valor.
        """
        self._productos_vendidos = {}  # {str: cantidad}
        self._metodo_pago = metodo_pago
        self._inventario = inventario
        self._caja = caja
        self._cliente = cliente
        self._total = 0  # Se calcula en calcular_total()
        self._fecha = fecha  # Nueva: fecha de la venta

        # Asocia cada producto real con la cantidad vendida
        for nombre_producto, cantidad in productos_vendidos.items():
            producto = self._inventario.buscar_producto_por_nombre(nombre_producto)
            if not producto:
                raise ValueError(f"Producto con nombre '{nombre_producto}' no encontrado en el inventario.")
            self._productos_vendidos[nombre_producto] = cantidad

    @property
    def productos_vendidos(self):
        return self._productos_vendidos

    @property
    def metodo_pago(self):
        return self._metodo_pago

    @property
    def inventario(self):
        return self._inventario

    @property
    def caja(self):
        return self._caja

    @property
    def cliente(self):
        return self._cliente

    @property
    def total(self):
        return self._total

    @property
    def fecha(self):
        return self._fecha
    
    def calcular_total(self):
        total = 0
        for nombre_producto, cantidad in self._productos_vendidos.items():
            producto = self._inventario.buscar_producto_por_nombre(nombre_producto)
            if producto:
                total += producto.precio * cantidad
        self._total = total
        return total

    def procesar_venta(self):
        try:
            # Primero valida stock y realiza la venta (descuenta stock)
            for nombre_producto, cantidad in self._productos_vendidos.items():
                producto = self._inventario.buscar_producto_por_nombre(nombre_producto)
                if not producto:
                    raise ValueError(f"Producto '{nombre_producto}' no encontrado en el inventario.")
                producto.vender(cantidad)
            self.calcular_total()
            if not self._metodo_pago.procesar_pago(self._total):
                return False

            # Si el método de pago es efectivo, ingresa el dinero en caja
            if isinstance(self._metodo_pago, PagoEfectivo):
                self._caja.ingresar_dinero(self._total)

            return True
        except ValueError:
            return False

    def __str__(self):
        detalles_str = "\n".join(
            f"{nombre_producto} x {cantidad} = S/{self._inventario.buscar_producto_por_nombre(nombre_producto).precio * cantidad:.2f}"
            for nombre_producto, cantidad in self._productos_vendidos.items()
            if self._inventario.buscar_producto_por_nombre(nombre_producto)
        )
        return f"Productos vendidos:\n{detalles_str}\nTotal: S/{self._total:.2f}"