from Producto import Producto

class Inventario:
    """
    Representa el inventario de la cantina.
    Permite agregar, eliminar, buscar y listar productos.
    """
    def __init__(self):
        self._productos = {}  # clave: id, valor: Producto

    # Metodos
    def agregar_producto(self, p):
        """
        Agrega un producto al inventario.
        Si el producto ya existe (por nombre), suma el stock.
        """
        if not isinstance(p, Producto):
            raise TypeError("El objeto debe ser una instancia de la clase Producto.")
        # Buscar producto existente por nombre (ignorando mayúsculas/minúsculas)
        for existente in self._productos.values():
            if existente._nombre.lower() == p._nombre.lower():
                existente._stock += p._stock
                # Opcional: actualizar precio, categoría o stock_minimo si quieres
                existente._precio = p._precio  # Si quieres actualizar el precio al último ingresado
                existente._categoria = p._categoria
                existente._stock_minimo = p._stock_minimo
                return
        # Si no existe, agregar como nuevo
        self._productos[p._id] = p

    def eliminar_producto(self, id):
        """
        Elimina un producto del inventario por su ID.
        """
        if id in self._productos:
            del self._productos[id]
        else:
            raise KeyError(f"Producto con ID {id} no encontrado.")

    def buscar_producto(self, id):
        """
        Busca un producto por su ID.
        """
        return self._productos.get(id)

    def listar_productos(self):
        """
        Devuelve una lista de todos los productos en el inventario.
        """
        return list(self._productos.values())
    
    def productos_bajo_stock(self):
        """
        Devuelve una lista de productos cuyo stock está por debajo del mínimo.
        """
        return [p for p in self._productos.values() if p._stock <= p._stock_minimo]

    def __str__(self):
        """
        Representación en texto del inventario.
        """
        if not self._productos:
            return "El inventario está vacío."
        return "\n".join(str(p) for p in self._productos.values())