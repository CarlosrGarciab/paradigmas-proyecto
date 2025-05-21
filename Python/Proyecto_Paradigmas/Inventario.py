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
        Si el producto ya existe, suma el stock.
        """
        if not isinstance(p, Producto):
            raise TypeError("El objeto debe ser una instancia de la clase Producto.")
        if p._id in self._productos:
            existente = self._productos[p._id]
            existente._stock += p._stock
        else:
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

    def __str__(self):
        """
        Representación en texto del inventario.
        """
        if not self._productos:
            return "El inventario está vacío."
        return "\n".join(str(p) for p in self._productos.values())