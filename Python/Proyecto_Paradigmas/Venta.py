from DetalleVenta import DetalleVenta
from PagoEfectivo import PagoEfectivo

class Venta:
    """
    Representa una venta realizada en la cantina.
    Incluye los detalles de los productos vendidos, el método de pago, el inventario, la caja y el cliente.
    """
    _id_counter = 1  # Variable de clase para autoincremento de IDs

    def __init__(self, productos_vendidos, metodo_pago, inventario, caja, cliente=None):
        """
        Inicializa la venta con su id, los productos vendidos, método de pago, inventario, caja y cliente.
        productos_vendidos: diccionario con id_producto como clave y cantidad como valor.
        """
        self._id = Venta._id_counter
        Venta._id_counter += 1

        self._detalles = []
        self._metodo_pago = metodo_pago
        self._inventario = inventario
        self._caja = caja
        self._cliente = cliente
        self._total = 0  # Se calcula en calcular_total()

        # Crear los detalles de venta para cada producto vendido
        for id_producto, cantidad in productos_vendidos.items():
            producto = self._inventario.buscar_producto(id_producto)
            if not producto:
                raise ValueError(f"Producto con ID {id_producto} no encontrado en el inventario.")
            self._detalles.append(DetalleVenta(producto, cantidad, producto._precio))

    # Getters y Setters
    @property
    def id(self):
        """ID único de la venta."""
        return self._id

    @property
    def detalles(self):
        """Lista de detalles de la venta."""
        return self._detalles

    @property
    def metodo_pago(self):
        """Método de pago utilizado para la venta."""
        return self._metodo_pago

    @property
    def inventario(self):
        """Inventario de la cantina."""
        return self._inventario

    @property
    def caja(self):
        """Caja de la cantina."""
        return self._caja

    @property
    def cliente(self):
        """Cliente de la venta."""
        return self._cliente

    @property
    def total(self):
        """Total de la venta (suma de subtotales de los detalles)."""
        return self._total

    # Metodos
    def calcular_total(self):
        """
        Calcula el total de la venta y valida el stock de los productos.
        """
        total = 0
        for detalle in self._detalles:
            if detalle._cantidad <= 0:
                raise ValueError(f"La cantidad para el producto '{detalle._producto._nombre}' debe ser mayor a 0.")
            if detalle._producto._stock < detalle._cantidad:
                raise ValueError(
                    f"Stock insuficiente para el producto '{detalle._producto._nombre}'. "
                    f"Disponible: {detalle._producto._stock}, solicitado: {detalle._cantidad}."
                )
            total += detalle.subtotal
        self._total = total
        return total

    def procesar_venta(self):
        """
        Procesa la venta:
        - Calcula el total y valida el stock.
        - Procesa el pago usando el método de pago seleccionado.
        - Actualiza el inventario y elimina productos sin stock.
        - Ingresa el dinero en la caja o banco según corresponda.
        Devuelve True si la venta fue exitosa, False si hubo algún error.
        """
        try:
            self.calcular_total()
            # El método de pago decide si se puede procesar el pago
            if not self._metodo_pago.procesar_pago(self._total):
                print("El pago fue rechazado.")
                return False

            # Actualizar el inventario
            for detalle in self._detalles:
                producto = detalle._producto
                producto._stock -= detalle._cantidad
                if producto._stock == 0:
                    self._inventario.eliminar_producto(producto._id)
                    
            # Registrar el ingreso de dinero en la caja o banco
            if isinstance(self._metodo_pago, PagoEfectivo):
                self._caja.ingresar_dinero(self._total)

            print(f"Venta completada. Total: S/{self._total:.2f}")
            return True
        except ValueError as e:
            print(f"Error al procesar la venta: {e}")
            return False

    def __str__(self):
        """
        Representación en texto de la venta, mostrando los detalles y el total.
        """
        detalles_str = "\n".join(str(det) for det in self._detalles)
        return f"ID Venta: {self._id}\nDetalles de la venta:\n{detalles_str}\nTotal: S/{self._total:.2f}"