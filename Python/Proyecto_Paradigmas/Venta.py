from DetalleVenta import DetalleVenta

class Venta:
    """
    Representa una venta realizada en la cantina.
    Incluye los detalles de los productos vendidos, el método de pago, el inventario, la caja y el cliente.
    """
    def __init__(self, productos_vendidos, metodo_pago, inventario, caja, cliente=None):
        """
        Inicializa la venta con los productos vendidos, método de pago, inventario, caja y cliente.
        productos_vendidos: dict con id_producto como clave y cantidad como valor.
        """
        self.detalles = []
        self.metodo_pago = metodo_pago
        self.inventario = inventario
        self.caja = caja
        self.cliente = cliente
        self.total = 0  # Se calcula en calcular_total()

        # Crear los detalles de venta
        for id_producto, cantidad in productos_vendidos.items():
            producto = self.inventario.buscar_producto(id_producto)
            if not producto:
                raise ValueError(f"Producto con ID {id_producto} no encontrado en el inventario.")
            self.detalles.append(DetalleVenta(producto, cantidad, producto.precio))

    def calcular_total(self):
        """
        Calcula el total de la venta y valida el stock de los productos.
        """
        total = 0
        for detalle in self.detalles:
            if detalle.cantidad <= 0:
                raise ValueError(f"La cantidad para el producto '{detalle.producto.nombre}' debe ser mayor a 0.")
            if detalle.producto.stock < detalle.cantidad:
                raise ValueError(f"Stock insuficiente para el producto '{detalle.producto.nombre}'. Disponible: {detalle.producto.stock}, solicitado: {detalle.cantidad}.")
            total += detalle.subtotal
        self.total = total
        return total

    def procesar_venta(self):
        """
        Procesa la venta: valida el pago, descuenta el stock y registra el ingreso en caja.
        """
        try:
            self.calcular_total()
            # El método de pago decide si se puede procesar el pago
            if not self.metodo_pago.procesar_pago(self.total):
                print("El pago fue rechazado.")
                return False

            # Actualizar el inventario
            for detalle in self.detalles:
                producto = detalle.producto
                producto.stock -= detalle.cantidad
                if producto.stock == 0:
                    self.inventario.eliminar_producto(producto.id)

            self.caja.ingresar_dinero(self.total)
            print(f"Venta completada. Total: S/{self.total:.2f}")
            return True
        except ValueError as e:
            print(f"Error al procesar la venta: {e}")
            return False

    def __str__(self):
        """
        Representación en texto de la venta.
        """
        detalles_str = "\n".join(str(det) for det in self.detalles)
        return f"Detalles de la venta:\n{detalles_str}\nTotal: S/{self.total:.2f}"