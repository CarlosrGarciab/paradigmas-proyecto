import pickle
from functools import reduce

# Cargar ventas y productos desde los archivos .pkl
with open("ventas.pkl", "rb") as f:
    ventas = pickle.load(f)
with open("inventario.pkl", "rb") as f:
    inventario = pickle.load(f)

productos = inventario.listar_productos()
productos_dict = {p.nombre: p for p in productos}

def resumen_ventas_por_producto(ventas):
    # Extrae todas las ventas de productos como lista de tuplas (nombre, cantidad)
    vendidos = reduce(
        lambda acc, venta: acc + list(venta.productos_vendidos.items()),
        ventas,
        []
    )
    # Agrupa y suma cantidades por producto
    resumen = {}
    for nombre, cantidad in vendidos:
        resumen[nombre] = resumen.get(nombre, 0) + cantidad
    # Calcula ingreso por producto
    resultado = [
        {
            "nombre": nombre,
            "cantidad_vendida": cantidad,
            "ingreso": productos_dict[nombre].precio * cantidad if nombre in productos_dict else 0
        }
        for nombre, cantidad in resumen.items()
    ]
    # Ordena por ingreso descendente
    return sorted(resultado, key=lambda x: x["ingreso"], reverse=True)

if __name__ == "__main__":
    resumen = resumen_ventas_por_producto(ventas)
    print("Resumen de ventas por producto:")
    for r in resumen:
        print(f"- {r['nombre']}: {r['cantidad_vendida']} unidades, ingreso S/{r['ingreso']:.2f}")