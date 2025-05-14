from Caja import Caja
from Producto import Producto
from Inventario import Inventario
from Venta import Venta
from Cliente import Cliente

def main():
    # Crear productos
    producto1 = Producto("Agua", 1.50, 100, 10, "Bebidas")
    producto2 = Producto("Sandwich", 5.00, 50, 5, "Comidas")

    # Crear inventario
    inventario = Inventario()
    inventario.agregar_producto(producto1)
    inventario.agregar_producto(producto2)

    # Crear caja
    caja = Caja()

    # Crear cliente
    cliente = Cliente("Carlos")
    print("\n=== Estado inicial del Cliente ===")
    print(cliente)

    # Recargar saldo prepago desde la caja
    print("\n=== Recarga de Saldo ===")
    cliente.recargar_saldo(10.00, caja=caja)  # Recargar S/10.00 desde la caja
    print(cliente)

    # Mostrar estado de la caja
    print("\n=== Estado de la Caja ===")
    print(caja)

    # Prueba de ventas
    print("\n=== Prueba de Ventas ===")
    productos_vendidos = {1: 2, 2: 1}  # 2 aguas y 1 sandwich
    venta = Venta(productos_vendidos, None, inventario, caja, cliente)

    # Procesar la venta
    print("\n=== Procesar Venta ===")
    if venta.procesar_venta():
        print("Venta realizada con éxito.")
    else:
        print("La venta no pudo completarse.")

    # Mostrar estado del cliente después de la venta
    print("\n=== Estado del Cliente después de la Venta ===")
    print(cliente)

    # Mostrar estado de la caja después de la venta
    print("\n=== Estado de la Caja después de la Venta ===")
    print(caja)

if __name__ == "__main__":
    main()