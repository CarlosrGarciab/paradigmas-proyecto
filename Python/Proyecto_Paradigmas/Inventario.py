from Producto import Producto

class Inventario:
    """
    Representa el inventario de la cantina.
    Permite agregar, eliminar, buscar y listar productos.
    """
    def __init__(self):
        self._productos = {}  # clave: nombre, valor: Producto

    def agregar_producto(self, p):
        """
        Agrega un producto al inventario.
        Si el producto ya existe (por nombre), suma el stock usando el método del producto.
        """
        if not isinstance(p, Producto):
            raise TypeError("El objeto debe ser una instancia de la clase Producto.")
        existente = self.buscar_producto_por_nombre(p.nombre)
        if existente:
            existente.agregar_stock(p.stock)
            existente.precio = p.precio
            existente.categoria = p.categoria
            existente.stock_minimo = p.stock_minimo
            existente.disponible = getattr(p, 'disponible', True)
        else:
            self._productos[p.nombre.lower()] = p

    def eliminar_producto(self, nombre):
        """
        Elimina un producto del inventario por su nombre.
        """
        key = nombre.lower()
        if key in self._productos:
            del self._productos[key]
        else:
            raise KeyError(f"Producto con nombre '{nombre}' no encontrado.")

    def buscar_producto(self, nombre):
        """
        Busca un producto por su nombre (ignorando mayúsculas/minúsculas).
        """
        return self._productos.get(nombre.lower())

    def listar_productos(self):
        """
        Devuelve una lista de todos los productos en el inventario.
        """
        return list(self._productos.values())

    def productos_bajo_stock(self):
        """
        Devuelve una lista de productos cuyo stock está por debajo del mínimo.
        """
        return [p for p in self._productos.values() if p.stock <= p.stock_minimo]

    def buscar_producto_por_nombre(self, nombre):
        """Busca un producto por nombre (ignorando mayúsculas/minúsculas)."""
        for producto in self._productos.values():
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None

    def agregar_o_sumar_producto(self, producto, cantidad):
        """Si existe suma stock usando el método del producto, si no lo agrega."""
        existente = self.buscar_producto(producto.nombre)
        if existente:
            existente.agregar_stock(cantidad)
        else:
            self._productos[producto.nombre.lower()] = producto

    def actualizar_producto(self, nombre_producto, **kwargs):
        """Actualiza los datos de un producto existente."""
        producto = self.buscar_producto(nombre_producto)
        if producto:
            producto.actualizar_datos(**kwargs)
        else:
            raise KeyError("Producto no encontrado.")

    def __str__(self):
        """
        Representación en texto del inventario.
        """
        if not self._productos:
            return "El inventario está vacío."
        return "\n".join(str(p) for p in self._productos.values())