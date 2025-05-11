class Inventario:
    def __init__(self):
        self.productos = {}  # clave: id, valor: Producto

    def agregar_producto(self, p):
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
