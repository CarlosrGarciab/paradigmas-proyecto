from Producto import Producto
from Venta import Venta
from Compra import Compra
from Proveedor import Proveedor

class Menu:
    """
    Clase que gestiona la interacción con el usuario a través de menús.
    Permite registrar ventas, compras, gestionar clientes, proveedores, caja, banco e inventario.
    """
    def __init__(self, inventario, caja, banco, clientes, proveedores, ventas, compras):
        """
        Inicializa el menú con las entidades principales del sistema.
        """
        self._inventario = inventario
        self._caja = caja
        self._banco = banco
        self._clientes = clientes
        self._proveedores = proveedores
        self._ventas = ventas
        self._compras = compras

    def mostrar(self):
        """
        Muestra el menú principal y gestiona la navegación entre opciones.
        """
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Registrar venta")
            print("2. Registrar compra")
            print("3. Ver inventario")
            print("4. Ver caja")
            print("5. Ver banco")
            print("6. Clientes (Submenu)")
            print("7. Ver proveedores")
            print("8. Ver historial de ventas")
            print("9. Ver historial de compras")
            print("0. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_venta()
                input("Presione Enter para continuar...")
            elif opcion == "2":
                self.registrar_compra()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                print("\n=== Inventario ===")
                print(self._inventario)
                input("Presione Enter para continuar...")
            elif opcion == "4":
                print("\n=== Caja ===")
                print(self._caja)
                input("Presione Enter para continuar...")
            elif opcion == "5":
                print("\n=== Banco ===")
                print(self._banco)
                input("Presione Enter para continuar...")
            elif opcion == "6":
                self.menu_clientes()
            elif opcion == "7":
                print("\n=== Proveedores ===")
                for proveedor in self._proveedores:
                    print(proveedor)
                input("Presione Enter para continuar...")
            elif opcion == "8":
                print("\n=== Historial de Ventas ===")
                for venta in self._ventas:
                    print(venta)
                    print()
                input("Presione Enter para continuar...")
            elif opcion == "9":
                print("\n=== Historial de Compras ===")
                for compra in self._compras:
                    print(compra)
                    print()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                print("Cerrando el programa...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
    
    # Submenu de clientes                
    def menu_clientes(self):
        """
        Muestra el submenu de clientes y gestiona sus acciones.
        """
        while True:
            print("\n=== MENU DE CLIENTES ===")
            print("1. Registrar cliente")
            print("2. Ver clientes")
            print("3. Recargar cuenta prepaga")
            print("4. Pagar deuda")
            print("0. Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_cliente()
                input("Presione Enter para continuar...")
            elif opcion == "2":
                print("\n=== Clientes ===")
                for cliente in self._clientes:
                    print(cliente)
                    print()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                self.recargar_prepago_cliente()
                input("Presione Enter para continuar...")
            elif opcion == "4":
                self.pagar_deuda_cliente()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    # Método para registrar ventas
    def registrar_venta(self):
        """
        Permite registrar una venta, seleccionando productos, cantidades y método de pago.
        """
        print("\n=== Registrar Venta ===")
        if not self._inventario.listar_productos():
            print("No hay productos en el inventario.")
            return
        productos_vendidos = {}
        while True:
            print("\nProductos disponibles:")
            for p in self._inventario.listar_productos():
                seleccionados = productos_vendidos.get(p._id, 0)
                disponible = p._stock - seleccionados
                print(f"{p._id}: {p._nombre} (Stock disponible: {disponible}, Precio: S/{p._precio:.2f})")
            id_str = input("Ingrese el ID del producto a vender (o '0' para terminar): ")
            if id_str == "0":
                break
            try:
                id_producto = int(id_str)
                producto = self._inventario.buscar_producto(id_producto)
                if not producto:
                    print("Producto no encontrado.")
                    continue
                seleccionados = productos_vendidos.get(id_producto, 0)
                disponible = producto._stock - seleccionados
                cantidad = int(input(f"Ingrese la cantidad de '{producto._nombre}' a vender (disponible: {disponible}): "))
                if cantidad <= 0 or cantidad > disponible:
                    print("Cantidad inválida o insuficiente stock.")
                    continue
                productos_vendidos[id_producto] = seleccionados + cantidad
            except ValueError:
                print("Entrada inválida.")
        if not productos_vendidos:
            print("No se seleccionaron productos para la venta.")
            return

        # Calcular el total de la venta
        total = 0
        for id_producto, cantidad in productos_vendidos.items():
            producto = self._inventario.buscar_producto(id_producto)
            total += producto._precio * cantidad

        print(f"\nTotal de la venta: S/{total:.2f}")
        print("Seleccione el método de pago:")
        print("1. Efectivo")
        print("2. Prepago")
        print("3. Transferencia bancaria")
        print("4. Deuda")

        metodo = input("Opción: ")
        metodo_pago = None
        cliente = None

        # Efectivo
        if metodo == "1":
            monto_pago = float(input("Ingrese el monto recibido en efectivo: "))
            from PagoEfectivo import PagoEfectivo
            metodo_pago = PagoEfectivo(self._caja, monto_pago)
            venta = Venta(productos_vendidos, metodo_pago, self._inventario, self._caja)
            if venta.procesar_venta():
                vuelto = monto_pago - total
                print("Venta realizada con éxito.")
                print(f"Vuelto a entregar: S/{vuelto:.2f}")
                self._ventas.append(venta)
            else:
                print("La venta no pudo completarse.")
            return

        # Prepago
        elif metodo == "2":
            alumnos = [c for c in self._clientes if c.__class__.__name__ == "Alumno"]
            if not alumnos:
                print("No hay alumnos registrados para prepago.")
                return
            print("Alumnos disponibles:")
            for idx, a in enumerate(alumnos):
                print(f"{idx+1}. {a._nombre} (Saldo prepago: S/{a._saldo_prepago:.2f})")
            idx_cliente = int(input("Seleccione el alumno: ")) - 1
            alumno = alumnos[idx_cliente]
            from PagoPrepago import PagoPrepago
            metodo_pago = PagoPrepago(alumno, total)
            venta = Venta(productos_vendidos, metodo_pago, self._inventario, self._caja, alumno)
            if venta.procesar_venta():
                print("Venta realizada con éxito.")
                self._ventas.append(venta)
            else:
                print("La venta no pudo completarse.")
            return
        
        # Transferencia bancaria
        elif metodo == "3":
            from PagoTransferencia import PagoTransferencia
            metodo_pago = PagoTransferencia(self._banco, total)
        
        # Deuda
        elif metodo == "4":
            if not self._clientes:
                print("No hay clientes registrados para deuda.")
                return
            print("Clientes disponibles:")
            for idx, c in enumerate(self._clientes):
                print(f"{idx+1}. {c._nombre} (Deuda actual: S/{c._deuda:.2f})")
            idx_cliente = int(input("Seleccione el cliente: ")) - 1
            cliente = self._clientes[idx_cliente]
            from PagoDeuda import PagoDeuda
            metodo_pago = PagoDeuda(cliente, total)
        else:
            print("Método de pago no válido.")
            return

        venta = Venta(productos_vendidos, metodo_pago, self._inventario, self._caja, cliente)
        if venta.procesar_venta():
            print("Venta realizada con éxito.")
            self._ventas.append(venta)
        else:
            print("La venta no pudo completarse.")
    
    # Método para registrar compras            
    def registrar_compra(self):
        """
        Permite registrar una compra a un proveedor y actualizar el inventario.
        """
        print("\n=== Registrar Compra ===")
        nombre_proveedor = input("Ingrese el nombre del proveedor: ")
        proveedor = next((p for p in self._proveedores if p._nombre == nombre_proveedor), None)
        if not proveedor:
            proveedor = Proveedor(nombre_proveedor)
            self._proveedores.append(proveedor)
        productos_comprados = {}
        while True:
            nombre_producto = input("Nombre del producto a comprar (o '0' para terminar): ")
            if nombre_producto == "0":
                break
            try:
                while True:
                    precio_compra = float(input("Precio unitario de compra: "))
                    if precio_compra > 0:
                        break
                    print("El precio de compra debe ser mayor a 0.")
                while True:
                    cantidad = int(input("Cantidad a comprar: "))
                    if cantidad > 0:
                        break
                    print("La cantidad debe ser mayor a 0.")
                categoria = input("Categoría del producto: ")
                producto = next((p for p in self._inventario.listar_productos() if p._nombre == nombre_producto), None)
                if not producto:
                    while True:
                        precio_venta = float(input("Precio de venta al público: "))
                        if precio_venta > 0:
                            break
                        print("El precio de venta debe ser mayor a 0.")
                    # CORREGIDO: solo pasar nombre, precio, stock, categoria
                    producto = Producto(nombre_producto, precio_venta, 0, categoria)
                else:
                    actualizar = input(f"El precio de venta actual es S/{producto._precio:.2f}. ¿Desea actualizarlo? (s/n): ")
                    if actualizar.lower() == "s":
                        while True:
                            nuevo_precio = float(input("Nuevo precio de venta al público: "))
                            if nuevo_precio > 0:
                                break
                            print("El precio de venta debe ser mayor a 0.")
                        producto._precio = nuevo_precio
                productos_comprados[nombre_producto] = (producto, cantidad, precio_compra)
            except ValueError:
                print("Entrada inválida.")
        if not productos_comprados:
            print("No se ingresaron productos para la compra.")
            return
        fecha = input("Ingrese la fecha de la compra (ej: 21/05/2025): ")
        compra = Compra(proveedor, fecha, productos_comprados)
        try:
            compra.registrar_compra(self._caja, self._inventario)
            print("Compra registrada con éxito.")
            self._compras.append(compra)
        except Exception as e:
            print(f"Error al registrar la compra: {e}")
    
    # Método para registrar clientes                
    def registrar_cliente(self):
        """
        Permite registrar un nuevo cliente (alumno o profesor).
        """
        print("\n=== Registrar Cliente ===")
        print("Seleccione el tipo de cliente:")
        print("1. Alumno")
        print("2. Profesor")
        tipo = input("Opción: ")

        if tipo not in ("1", "2"):
            print("Tipo de cliente no válido.")
            return

        nombre = input("Nombre del cliente: ")

        # Alumno
        if tipo == "1":
            grado = input("Grado del alumno: ")
            saldo_prepago = float(input("Saldo inicial en cuenta prepaga: "))
            print("¿Dónde se deposita el saldo prepago?")
            print("1. Caja")
            print("2. Banco")
            metodo_pago = input("Opción: ")
            caja = self._caja if metodo_pago == "1" else None
            banco = self._banco if metodo_pago == "2" else None
            from Alumno import Alumno
            alumno = Alumno(nombre, grado, saldo_prepago, "caja" if caja else "banco", caja, banco)
            self._clientes.append(alumno)
            print("Alumno registrado con éxito.")
        # Profesor
        elif tipo == "2":
            grado = input("Donde enseña el profesor: ")
            from Profesor import Profesor
            profesor = Profesor(nombre, grado)
            self._clientes.append(profesor)
            print("Profesor registrado con éxito.")
    
    # Método para pagar deuda del cliente        
    def pagar_deuda_cliente(self):
        print("\n=== Pagar deuda de cliente ===")
        clientes_con_deuda = [c for c in self._clientes if c._deuda > 0]
        if not clientes_con_deuda:
            print("No hay clientes con deuda.")
            return
        for idx, c in enumerate(clientes_con_deuda):
            print(f"{idx+1}. {c._nombre} (Deuda actual: S/{c._deuda:.2f})")
        try:
            idx_cliente = int(input("Seleccione el cliente: ")) - 1
            if idx_cliente < 0 or idx_cliente >= len(clientes_con_deuda):
                print("Selección inválida.")
                return
            cliente = clientes_con_deuda[idx_cliente]
            monto = float(input(f"Ingrese el monto a pagar (deuda actual: S/{cliente._deuda:.2f}): "))
            if monto <= 0 or monto > cliente._deuda:
                print("Monto inválido.")
                return
            print("¿Dónde se recibe el pago?")
            print("1. Caja")
            print("2. Banco")
            metodo_pago = input("Opción: ")
            if metodo_pago == "1":
                self._caja._dinero += monto
            elif metodo_pago == "2":
                self._banco._saldo += monto
            else:
                print("Opción no válida.")
                return
            cliente._deuda -= monto
            print(f"Deuda pagada correctamente. Deuda restante: S/{cliente._deuda:.2f}")
        except (ValueError, IndexError):
            print("Selección inválida.")
    
    # Método para recargar cuenta prepaga del cliente (Solo para alumnos)                
    def recargar_prepago_cliente(self):
        print("\n=== Recargar cuenta prepaga ===")
        alumnos = [c for c in self._clientes if c.__class__.__name__ == "Alumno"]
        if not alumnos:
            print("No hay alumnos registrados.")
            return
        for idx, a in enumerate(alumnos):
            print(f"{idx+1}. {a._nombre} (Saldo prepago: S/{a._saldo_prepago:.2f})")
        try:
            idx_cliente = int(input("Seleccione el alumno: ")) - 1
            if idx_cliente < 0 or idx_cliente >= len(alumnos):
                print("Selección inválida.")
                return
            alumno = alumnos[idx_cliente]
            monto = float(input("Monto a recargar: "))
            if monto <= 0:
                print("Monto inválido.")
                return
            print("¿Dónde se deposita el saldo prepago?")
            print("1. Caja")
            print("2. Banco")
            metodo_pago = input("Opción: ")
            if metodo_pago == "1":
                self._caja._dinero += monto
            elif metodo_pago == "2":
                self._banco._saldo += monto
            else:
                print("Opción no válida.")
                return
            alumno._saldo_prepago += monto
            print(f"Saldo recargado correctamente. Nuevo saldo prepago: S/{alumno._saldo_prepago:.2f}")
        except (ValueError, IndexError):
            print("Selección inválida.")