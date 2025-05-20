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

    menu = Menu(inventario, caja, banco, clientes, proveedores, ventas, compras)
    menu.mostrar()

if __name__ == "__main__":
    main()
    
# git add .
# git commit -m "comentario"
# git push

# git pull