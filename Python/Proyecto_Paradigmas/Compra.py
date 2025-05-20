class Compra:
    _id_counter = 1

    def __init__(self, id, proveedor, fecha, detalles):
        self.__id = id if id is not None else Compra._id_counter
        Compra._id_counter = max(Compra._id_counter, self.__id + 1)
        self.__proveedor = proveedor
        self.__fecha = fecha
        self.__detalles = detalles  # Lista de DetalleCompra

    # Id
    @property
    def id(self):
        return self.__id

    # Proveedor
    @property
    def proveedor(self):
        return self.__proveedor

    # Fecha
    @property
    def fecha(self):
        return self.__fecha

    # Detalles
    @property
    def detalles(self):
        return self.__detalles

    # Total
    @property
    def total(self):
        return sum(det.subtotal for det in self.__detalles)

    def registrar_compra(self, caja, inventario):
        total_compra = self.total
        if caja.dinero < total_compra:
            raise ValueError("No hay suficiente dinero en caja para pagar al proveedor.")
        # Pagar al proveedor
        caja.dinero -= total_compra
        self.proveedor.recibir_pago(total_compra)
        # Agregar productos al inventario
        for detalle in self.detalles:
            producto = detalle.producto
            # Si el producto ya existe en inventario, suma la cantidad
            prod_existente = inventario.buscar_producto(producto.id)
            if prod_existente:
                prod_existente.stock += detalle.cantidad
            else:
                # Si no existe, agrega el producto con la cantidad comprada
                producto.stock = detalle.cantidad
                inventario.agregar_producto(producto)
        print(f"Compra registrada y pagada a {self.proveedor.nombre} por S/{total_compra:.2f}")

    def __str__(self):
        detalles_str = "\n".join(str(det) for det in self.__detalles)
        return f"Compra ID: {self.id}\nProveedor: {self.proveedor.nombre}\nFecha: {self.fecha}\nDetalles:\n{detalles_str}\nTotal: S/{self.total:.2f}"
# git add .
# git commit -m "comentario"
# git push

# git pull