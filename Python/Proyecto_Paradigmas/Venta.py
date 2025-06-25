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
        self._productos_vendidos = {}
        self._metodo_pago = metodo_pago
        self._inventario = inventario
        self._caja = caja
        self._cliente = cliente
        self._total = 0
        self._fecha = fecha

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