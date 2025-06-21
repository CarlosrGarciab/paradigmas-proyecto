import pickle

# Cargar inventario desde el archivo .pkl
with open("inventario.pkl", "rb") as f:
    inventario = pickle.load(f)

# Obtener la lista de productos del inventario
productos = inventario.listar_productos()

# Convertir a diccionarios para programación funcional
productos_dict = [
    {
        "nombre": p.nombre,
        "stock": p.stock,
        "stock_minimo": p.stock_minimo
    }
    for p in productos
]

def productos_bajo_stock(productos):
    # Programación funcional: filtra productos con stock menor o igual al mínimo
    return list(filter(lambda p: p["stock"] <= p["stock_minimo"], productos))

if __name__ == "__main__":
    bajos = productos_bajo_stock(productos_dict)
    print("Productos con bajo stock:")
    for p in bajos:
        print(f"- {p['nombre']} (stock: {p['stock']}, mínimo: {p['stock_minimo']})")