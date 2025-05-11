class Venta:
    def __init__(self, productos_vendidos, metodo_pago, inventario, caja):
        self.productos_vendidos = productos_vendidos  # dict con id y cantidad
        self.metodo_pago = metodo_pago
        self.inventario = inventario
        self.caja = caja
        self.total = self.calcular_total()

    def calcular_total(self):
        total = 0
        for id_producto, cantidad in self.productos_vendidos.items():
            producto = self.inventario.buscar_producto(id_producto)
            if not producto:
                raise ValueError(f"Producto con ID {id_producto} no encontrado.")
            if producto.stock < cantidad:
                raise ValueError(f"No hay suficiente stock para {producto.nombre}.")
            total += producto.precio * cantidad
        return total

    def procesar_venta(self):
        if self.metodo_pago.procesar_pago(self.total):
            for id_producto, cantidad in self.productos_vendidos.items():
                producto = self.inventario.buscar_producto(id_producto)
                producto.stock -= cantidad
                if producto.stock == 0:
                    self.inventario.eliminar_producto(id_producto)
            self.caja.ingresar_dinero(self.total)
            print(f"Venta completada por {self.total}")
            return True
        else:
            print("El pago fue rechazado.")
            return False
