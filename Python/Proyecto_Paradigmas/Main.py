from Persistencia import Persistencia
from Menu import Menu
from Inventario import Inventario
from Caja import Caja
from CuentaBanco import CuentaBanco

def main():
    # Cargar datos o inicializar si no existen
    inventario = Persistencia.cargar("inventario.pkl") or Inventario()
    caja = Persistencia.cargar("caja.pkl") or Caja()
    banco = Persistencia.cargar("banco.pkl") or CuentaBanco()
    clientes = Persistencia.cargar("clientes.pkl") or []
    proveedores = Persistencia.cargar("proveedores.pkl") or []
    ventas = Persistencia.cargar("ventas.pkl") or []
    compras = Persistencia.cargar("compras.pkl") or []

    # El nuevo Menu ya incluye submenús y toda la lógica
    menu = Menu(inventario, caja, banco, clientes, proveedores, ventas, compras)
    menu.mostrar()

    # Guardar datos al salir
    Persistencia.guardar(inventario, "inventario.pkl")
    Persistencia.guardar(caja, "caja.pkl")
    Persistencia.guardar(banco, "banco.pkl")
    Persistencia.guardar(clientes, "clientes.pkl")
    Persistencia.guardar(proveedores, "proveedores.pkl")
    Persistencia.guardar(ventas, "ventas.pkl")
    Persistencia.guardar(compras, "compras.pkl")

if __name__ == "__main__":
    main()
    
# git add .
# git commit -m "comentario"
# git push

# git pull