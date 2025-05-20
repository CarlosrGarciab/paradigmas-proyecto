from Producto import Producto
from DetalleVenta import DetalleVenta
from Venta import Venta
from DetalleCompra import DetalleCompra
from Compra import Compra
from Proveedor import Proveedor
from PagoEfectivo import PagoEfectivo

class Menu:
    def __init__(self, inventario, caja, banco, clientes, proveedores, ventas, compras):
        self.inventario = inventario
        self.caja = caja
        self.banco = banco
        self.clientes = clientes
        self.proveedores = proveedores
        self.ventas = ventas
        self.compras = compras

    def mostrar(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
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
                print(self.inventario)
                input("Presione Enter para continuar...")
            elif opcion == "4":
                print("\n=== Caja ===")
                print(self.caja)
                input("Presione Enter para continuar...")
            elif opcion == "5":
                print("\n=== Banco ===")
                print(self.banco)
                input("Presione Enter para continuar...")
            elif opcion == "6":
                self.menu_clientes()
            elif opcion == "7":
                print("\n=== Proveedores ===")
                for proveedor in self.proveedores:
                    print(proveedor)
                input("Presione Enter para continuar...")
            elif opcion == "8":
                print("\n=== Historial de Ventas ===")
                for venta in self.ventas:
                    print(venta)
                    print()
                input("Presione Enter para continuar...")
            elif opcion == "9":
                print("\n=== Historial de Compras ===")
                for compra in self.compras:
                    print(compra)
                    print()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                print("Cerrando el programa...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                    
    def menu_clientes(self):
        while True:
            print("\n=== MENÚ DE CLIENTES ===")
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
                for cliente in self.clientes:
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

    def registrar_venta(self):
        print("\n=== Registrar Venta ===")
        if not self.inventario.productos:
            print("No hay productos en el inventario.")
            return
        productos_vendidos = {}
        while True:
            print("\nProductos disponibles:")
            for p in self.inventario.productos.values():
                seleccionados = productos_vendidos.get(p.id, 0)
                disponible = p.stock - seleccionados
                print(f"{p.id}: {p.nombre} (Stock disponible: {disponible}, Precio: S/{p.precio:.2f})")
            id_str = input("Ingrese el ID del producto a vender (o 'fin' para terminar): ")
            if id_str.lower() == "fin":
                break
            try:
                id_producto = int(id_str)
                producto = self.inventario.buscar_producto(id_producto)
                if not producto:
                    print("Producto no encontrado.")
                    continue
                seleccionados = productos_vendidos.get(id_producto, 0)
                disponible = producto.stock - seleccionados
                cantidad = int(input(f"Ingrese la cantidad de '{producto.nombre}' a vender (disponible: {disponible}): "))
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
            producto = self.inventario.buscar_producto(id_producto)
            total += producto.precio * cantidad

        print(f"\nTotal de la venta: S/{total:.2f}")
        print("Seleccione el método de pago:")
        print("1. Efectivo")
        print("2. Prepago (cliente)")
        print("3. Transferencia bancaria")
        print("4. Deuda (cliente)")

        metodo = input("Opción: ")
        metodo_pago = None
        cliente = None

        if metodo == "1":  # Efectivo
            monto_pago = float(input("Ingrese el monto recibido en efectivo: "))
            from PagoEfectivo import PagoEfectivo
            metodo_pago = PagoEfectivo(self.caja, monto_pago)
            venta = Venta(productos_vendidos, metodo_pago, self.inventario, self.caja)
            if venta.procesar_venta():
                vuelto = monto_pago - total
                print("Venta realizada con éxito.")
                print(f"Vuelto a entregar: S/{vuelto:.2f}")
                self.ventas.append(venta)
            else:
                print("La venta no pudo completarse.")
            return  # Salir para no repetir el flujo

        elif metodo == "2":
            # Solo mostrar alumnos
            alumnos = [c for c in self.clientes if c.__class__.__name__ == "Alumno"]
            if not alumnos:
                print("No hay alumnos registrados para prepago.")
                return
            print("Alumnos disponibles:")
            for idx, a in enumerate(alumnos):
                print(f"{idx+1}. {a.nombre} (Saldo prepago: S/{a.saldo_prepago:.2f})")
            idx_cliente = int(input("Seleccione el alumno: ")) - 1
            cliente = alumnos[idx_cliente]
            from PagoPrepago import PagoPrepago
            metodo_pago = PagoPrepago(cliente, total)
            venta = Venta(productos_vendidos, metodo_pago, self.inventario, self.caja, cliente)
            if venta.procesar_venta():
                print("Venta realizada con éxito.")
                self.ventas.append(venta)
            else:
                print("La venta no pudo completarse.")
            return  # Salir para no repetir el flujo
        elif metodo == "3":
            from PagoTransferencia import PagoTransferencia
            metodo_pago = PagoTransferencia(self.banco, total)
        elif metodo == "4":
            if not self.clientes:
                print("No hay clientes registrados para deuda.")
                return
            print("Clientes disponibles:")
            for idx, c in enumerate(self.clientes):
                print(f"{idx+1}. {c.nombre} (Deuda actual: S/{c.deuda:.2f})")
            idx_cliente = int(input("Seleccione el cliente: ")) - 1
            cliente = self.clientes[idx_cliente]
            from PagoDeuda import PagoDeuda
            metodo_pago = PagoDeuda(cliente, total)
        else:
            print("Método de pago no válido.")
            return

        venta = Venta(productos_vendidos, metodo_pago, self.inventario, self.caja, cliente)
        if venta.procesar_venta():
            print("Venta realizada con éxito.")
            self.ventas.append(venta)
        else:
            print("La venta no pudo completarse.")
                
    def registrar_compra(self):
        print("\n=== Registrar Compra ===")
        nombre_proveedor = input("Ingrese el nombre del proveedor: ")
        proveedor = next((p for p in self.proveedores if p.nombre == nombre_proveedor), None)
        if not proveedor:
            proveedor = Proveedor(nombre_proveedor)
            self.proveedores.append(proveedor)
        detalles = []
        while True:
            nombre_producto = input("Nombre del producto a comprar (o 'fin' para terminar): ")
            if nombre_producto.lower() == "fin":
                break
            try:
                precio_compra = float(input("Precio unitario de compra: "))
                cantidad = int(input("Cantidad a comprar: "))
                categoria = input("Categoría del producto: ")
                # Buscar producto existente por nombre
                producto = next((p for p in self.inventario.productos.values() if p.nombre == nombre_producto), None)
                if not producto:
                    # Producto nuevo: pedir precio de venta
                    precio_venta = float(input("Precio de venta al público: "))
                    producto = Producto(nombre_producto, precio_venta, 0, 1, categoria)
                else:
                    # Producto existente: preguntar si quiere actualizar el precio de venta
                    actualizar = input(f"El precio de venta actual es S/{producto.precio:.2f}. ¿Desea actualizarlo? (s/n): ")
                    if actualizar.lower() == "s":
                        nuevo_precio = float(input("Nuevo precio de venta al público: "))
                        producto.precio = nuevo_precio
                detalle = DetalleCompra(producto, cantidad, precio_compra)
                detalles.append(detalle)
            except ValueError:
                print("Entrada inválida.")
        if not detalles:
            print("No se ingresaron productos para la compra.")
            return
        fecha = input("Ingrese la fecha de la compra (ej: 2024-06-01): ")
        compra = Compra(len(self.compras)+1, proveedor, fecha, detalles)
        try:
            compra.registrar_compra(self.caja, self.inventario)
            print("Compra registrada con éxito.")
            self.compras.append(compra)
        except Exception as e:
            print(f"Error al registrar la compra: {e}")
            
    def registrar_cliente(self):
        print("\n=== Registrar Cliente ===")
        print("Seleccione el tipo de cliente:")
        print("1. Alumno")
        print("2. Profesor")
        tipo = input("Opción: ")

        nombre = input("Nombre del cliente: ")

        if tipo == "1":
            grado = input("Grado del alumno: ")
            saldo_prepago = float(input("Saldo inicial en cuenta prepaga: "))
            print("¿Dónde se deposita el saldo prepago?")
            print("1. Caja")
            print("2. Banco")
            metodo_pago = input("Opción: ")
            caja = self.caja if metodo_pago == "1" else None
            banco = self.banco if metodo_pago == "2" else None
            from Alumno import Alumno
            alumno = Alumno(nombre, grado, saldo_prepago, "caja" if caja else "banco", caja, banco)
            self.clientes.append(alumno)
            print("Alumno registrado con éxito.")
        elif tipo == "2":
            grado = input("Grado donde enseña el profesor: ")
            from Profesor import Profesor
            profesor = Profesor(nombre, grado)
            self.clientes.append(profesor)
            print("Profesor registrado con éxito.")
        else:
            print("Tipo de cliente no válido.")
            
    def pagar_deuda_cliente(self):
        print("\n=== Pagar deuda de cliente ===")
        clientes_con_deuda = [c for c in self.clientes if c.deuda > 0]
        if not clientes_con_deuda:
            print("No hay clientes con deuda.")
            return
        for idx, c in enumerate(clientes_con_deuda):
            print(f"{idx+1}. {c.nombre} (Deuda actual: S/{c.deuda:.2f})")
        try:
            idx_cliente = int(input("Seleccione el cliente: ")) - 1
            cliente = clientes_con_deuda[idx_cliente]
            monto = float(input(f"Ingrese el monto a pagar (deuda actual: S/{cliente.deuda:.2f}): "))
            if monto <= 0 or monto > cliente.deuda:
                print("Monto inválido.")
                return
            print("¿Dónde se recibe el pago?")
            print("1. Caja")
            print("2. Banco")
            metodo_pago = input("Opción: ")
            if metodo_pago == "1":
                self.caja.dinero += monto
            elif metodo_pago == "2":
                self.banco.saldo += monto
            else:
                print("Opción no válida.")
                return
            cliente.deuda -= monto
            print(f"Deuda pagada correctamente. Deuda restante: S/{cliente.deuda:.2f}")
        except (ValueError, IndexError):
            print("Selección inválida.")
            
    def recargar_prepago_cliente(self):
        print("\n=== Recargar cuenta prepaga ===")
        alumnos = [c for c in self.clientes if c.__class__.__name__ == "Alumno"]
        if not alumnos:
            print("No hay alumnos registrados.")
            return
        for idx, a in enumerate(alumnos):
            print(f"{idx+1}. {a.nombre} (Saldo prepago: S/{a.saldo_prepago:.2f})")
        try:
            idx_cliente = int(input("Seleccione el alumno: ")) - 1
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
                self.caja.dinero += monto
            elif metodo_pago == "2":
                self.banco.saldo += monto
            else:
                print("Opción no válida.")
                return
            alumno.saldo_prepago += monto
            print(f"Saldo recargado correctamente. Nuevo saldo prepago: S/{alumno.saldo_prepago:.2f}")
        except (ValueError, IndexError):
            print("Selección inválida.")