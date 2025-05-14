class Venta:
    def __init__(self, productos_vendidos, metodo_pago, inventario, caja, cliente=None):
        """
        productos_vendidos: dict con id_producto como clave y cantidad como valor.
        metodo_pago: instancia de un método de pago (por ejemplo, efectivo, prepago, etc.).
        inventario: instancia de la clase Inventario.
        caja: instancia de la clase Caja.
        cliente: instancia de la clase Cliente (opcional).
        """
        self.productos_vendidos = productos_vendidos
        self.metodo_pago = metodo_pago
        self.inventario = inventario
        self.caja = caja
        self.cliente = cliente
        self.total = 0  # Se calcula en calcular_total()

    def calcular_total(self):
        """Calcula el total de la venta y valida el stock."""
        total = 0
        for id_producto, cantidad in self.productos_vendidos.items():
            if cantidad <= 0:
                raise ValueError(f"La cantidad para el producto con ID {id_producto} debe ser mayor a 0.")
            
            producto = self.inventario.buscar_producto(id_producto)
            if not producto:
                raise ValueError(f"Producto con ID {id_producto} no encontrado en el inventario.")
            if producto.stock < cantidad:
                raise ValueError(f"Stock insuficiente para el producto '{producto.nombre}'. Disponible: {producto.stock}, solicitado: {cantidad}.")
            
            total += producto.precio * cantidad
        self.total = total
        return total

    def procesar_venta(self):
        """
        Procesa la venta:
        - Verifica el pago.
        - Reduce el stock de los productos vendidos.
        - Ingresa el dinero en la caja o genera deuda.
        """
        try:
            # Calcular el total antes de procesar el pago
            self.calcular_total()

            if self.cliente:
                # Usar saldo prepago si está disponible
                if self.cliente.saldo_prepago >= self.total:
                    self.cliente.saldo_prepago -= self.total
                    print(f"Venta procesada con saldo prepago. Total: S/{self.total:.2f}")
                else:
                    # Generar deuda si el saldo prepago es insuficiente
                    deuda = self.total - self.cliente.saldo_prepago
                    self.cliente.saldo_prepago = 0
                    self.cliente.adquirir_deuda(deuda)
                    print(f"Venta procesada con deuda. Total: S/{self.total:.2f}, Deuda generada: S/{deuda:.2f}")
            else:
                # Procesar el pago con el método de pago
                if not self.metodo_pago.procesar_pago(self.total):
                    print("El pago fue rechazado.")
                    return False

            # Actualizar el inventario
            for id_producto, cantidad in self.productos_vendidos.items():
                producto = self.inventario.buscar_producto(id_producto)
                producto.stock -= cantidad
                if producto.stock == 0:
                    self.inventario.eliminar_producto(id_producto)

            # Registrar el dinero en la caja
            self.caja.ingresar_dinero(self.total)

            print(f"Venta completada. Total: S/{self.total:.2f}")
            return True
        except ValueError as e:
            print(f"Error al procesar la venta: {e}")
            return False