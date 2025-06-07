from PagoEfectivo import PagoEfectivo

class Venta:
    """
    Representa una venta realizada en la cantina.
    Incluye los productos vendidos, el método de pago, y el cliente.
    """
    _id_counter = 1  # Variable de clase para autoincremento de IDs

    def __init__(self, productos_vendidos, metodo_pago, inventario, caja, cliente=None):
        """
        productos_vendidos: diccionario {nombre_producto: (cantidad, precio_unitario)}
        """
        self._id = Venta._id_counter
        Venta._id_counter += 1

        # Guardar solo datos simples: nombre del producto, cantidad, precio
        self._productos_vendidos = {}  # {str: (cantidad, precio_unitario)}
        for nombre_producto, cantidad in productos_vendidos.items():
            # Buscar el producto en el inventario para obtener el precio actual
            producto = inventario.buscar_producto_por_nombre(nombre_producto)
            precio_unitario = producto.precio if producto else 0
            self._productos_vendidos[nombre_producto] = (cantidad, precio_unitario)
        self._metodo_pago = metodo_pago
        self._cliente = cliente
        self._total = self.calcular_total()

    @property
    def id(self):
        return self._id

    @property
    def productos_vendidos(self):
        return self._productos_vendidos

    @property
    def metodo_pago(self):
        return self._metodo_pago

    @property
    def cliente(self):
        return self._cliente

    @property
    def total(self):
        return self._total

    def calcular_total(self):
        total = 0
        for _, (cantidad, precio_unitario) in self._productos_vendidos.items():
            total += precio_unitario * cantidad
        self._total = total
        return total

    def procesar_venta(self):
        try:
            # No modificar el stock aquí, ya se hace en el flujo del menú
            if not self._metodo_pago.procesar_pago(self._total):
                return False
            return True
        except ValueError:
            return False

    def __str__(self):
        detalles_str = "\n".join(
            f"{nombre} x {cantidad} = S/{precio_unitario * cantidad:.2f} (Precio: S/{precio_unitario:.2f})"
            for nombre, (cantidad, precio_unitario) in self._productos_vendidos.items()
        )
        return f"ID Venta: {self._id}\nProductos vendidos:\n{detalles_str}\nTotal: S/{self._total:.2f}"