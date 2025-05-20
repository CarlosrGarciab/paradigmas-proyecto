from Producto import Producto

class Inventario:
    """
    Representa el inventario de la cantina.
    Permite agregar, eliminar, buscar y listar productos.
    """
    def __init__(self):
        self.productos = {}  # clave: id, valor: Producto

    def agregar_producto(self, p):
        """
        Agrega un producto al inventario.
        Si el producto ya existe, suma el stock.
        """
        if not isinstance(p, Producto):
            raise TypeError("El objeto debe ser una instancia de la clase Producto.")
        if p.id in self.productos:
            existente = self.productos[p.id]
            existente.stock += p.stock
        else:
            self.productos[p.id] = p

    def eliminar_producto(self, id):
        """
        Elimina un producto del inventario por su ID.
        """
        if id in self.productos:
            del self.productos[id]
        else:
            raise KeyError(f"Producto con ID {id} no encontrado.")

    def buscar_producto(self, id):
        """
        Busca un producto por su ID.
        """
        return self.productos.get(id)

    def listar_productos(self):
        """
        Devuelve una lista de todos los productos en el inventario.
        """
        return list(self.productos.values())

    def actualizar_stock(self, id, cantidad):
        """
        Actualiza el stock de un producto sumando la cantidad indicada.
        """
        producto = self.buscar_producto(id)
        if producto:
            producto.actualizar_stock(cantidad)
        else:
            raise KeyError(f"Producto con ID {id} no encontrado.")

    def productos_con_stock_bajo(self):
        """
        Devuelve una lista de productos con stock bajo o igual al mínimo.
        """
        return [p for p in self.productos.values() if p.stock_bajo()]

    def valor_total_inventario(self):
        """
        Calcula el valor total del inventario.
        """
        return sum(p.valor_total_stock() for p in self.productos.values())

    def productos_por_categoria(self, categoria):
        """
        Devuelve una lista de productos de una categoría dada.
        """
        return [p for p in self.productos.values() if p.categoria == categoria]

    def __str__(self):
        """
        Representación en texto del inventario.
        """
        if not self.productos:
            return "El inventario está vacío."
        return "\n".join(str(p) for p in self.productos.values())