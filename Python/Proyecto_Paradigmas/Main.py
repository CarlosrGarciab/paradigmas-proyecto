from Menu import Menu
from Inventario import Inventario
from Caja import Caja
from CuentaBanco import CuentaBanco
from Producto import Producto
from Alumno import Alumno
from Profesor import Profesor

def main():
    inventario = Inventario()
    caja = Caja()
    caja.dinero = 100.0
    banco = CuentaBanco()
    clientes = []
    proveedores = []
    ventas = []
    compras = []

    # Productos de ejemplo
    p1 = Producto("Pan", 3.0, 20, 5, "Alimentos")
    p2 = Producto("Empanada", 5.0, 15, 5, "Alimentos")
    p3 = Producto("Jugo", 4.0, 10, 3, "Bebidas")
    inventario.agregar_producto(p1)
    inventario.agregar_producto(p2)
    inventario.agregar_producto(p3)

    # Clientes de ejemplo
    a1 = Alumno("Juan Perez", "3ro A", 20.0, "caja", caja)
    a2 = Alumno("Ana Ruiz", "2do B", 15.0, "banco", None, banco)
    prof1 = Profesor("Carlos Gómez", "Matemática")
    clientes.extend([a1, a2, prof1])

    menu = Menu(inventario, caja, banco, clientes, proveedores, ventas, compras)
    menu.mostrar()

if __name__ == "__main__":
    main()
    
# git add .
# git commit -m "comentario"
# git push

# git pull