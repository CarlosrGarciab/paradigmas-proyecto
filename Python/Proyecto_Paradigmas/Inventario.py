from Producto import Producto

class Inventario:
    def __init__(self):
        self.productos = {}  # clave: id, valor: Producto

    def agregar_producto(self, p):
        if not isinstance(p, Producto):
            raise TypeError("El objeto debe ser una instancia de la clase Producto.")
        if p.id in self.productos:
            existente = self.productos[p.id]
            existente.stock += p.stock
        else:
            self.productos[p.id] = p

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
        else:
            raise KeyError(f"Producto con ID {id} no encontrado.")

    def buscar_producto(self, id):
        return self.productos.get(id)

    def listar_productos(self):
        return list(self.productos.values())

    def actualizar_stock(self, id, cantidad):
        producto = self.buscar_producto(id)
        if producto:
            producto.actualizar_stock(cantidad)
        else:
            raise KeyError(f"Producto con ID {id} no encontrado.")

    def productos_con_stock_bajo(self):
        return [p for p in self.productos.values() if p.stock_bajo()]

    def valor_total_inventario(self):
        return sum(p.valor_total_stock() for p in self.productos.values())

    def productos_por_categoria(self, categoria):
        return [p for p in self.productos.values() if p.categoria == categoria]

    def __str__(self):
        if not self.productos:
            return "El inventario está vacío."
        return "\n".join(str(p) for p in self.productos.values())