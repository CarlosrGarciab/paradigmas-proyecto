from Producto import Producto
from Venta import Venta
from Compra import Compra
from Proveedor import Proveedor

def input_sn(mensaje):
    while True:
        resp = input(mensaje + " (s/n): ").strip().lower()
        if resp in ("s", "n"):
            return resp == "s"
        print("Por favor, ingrese 's' para sí o 'n' para no.")

class Menu:
    def __init__(self, inventario, caja, banco, clientes, proveedores, ventas, compras):
        self._inventario = inventario
        self._caja = caja
        self._banco = banco
        self._clientes = clientes
        self._proveedores = proveedores
        self._ventas = ventas
        self._compras = compras

    def mostrar(self):
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Registrar venta")
            print("2. Registrar compra")
            print("3. Productos")
            print("4. Caja/Banco")
            print("5. Proveedores")
            print("6. Clientes")
            print("7. Ventas")
            print("8. Compras")
            print("0. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_venta()
                input("Presione Enter para continuar...")
            elif opcion == "2":
                self.registrar_compra()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                self.menu_productos()
            elif opcion == "4":
                self.menu_caja_banco()
            elif opcion == "5":
                self.menu_proveedores()
            elif opcion == "6":
                self.menu_clientes()
            elif opcion == "7":
                self.ver_ventas()
                input("Presione Enter para continuar...")
            elif opcion == "8":
                self.ver_compras()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                self.alerta_bajo_stock()
                input("Cerrando Sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                
    def ver_ventas(self):
        print("\n=== HISTORIAL DE VENTAS Y TOTAL ===")
        total = 0
        for venta in self._ventas:
            print(venta)
            print()
            total += venta.total
        print(f"Total vendido: S/{total:.2f}")

    def ver_compras(self):
        print("\n=== HISTORIAL DE COMPRAS Y TOTAL ===")
        total = 0
        for compra in self._compras:
            print(compra)
            print()
            total += compra.total
        print(f"Total comprado: S/{total:.2f}")


    # Submenú de productos
    def menu_productos(self):
        while True:
            print("\n=== MENÚ DE PRODUCTOS ===")
            print("1. Ver inventario")
            print("2. Agregar producto")
            print("3. Editar producto")
            print("4. Eliminar producto")
            print("0. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(self._inventario)
                input("Presione Enter para continuar...")
            elif opcion == "2":
                self.agregar_producto()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                self.editar_producto()
                input("Presione Enter para continuar...")
            elif opcion == "4":
                self.eliminar_producto()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

    # Submenú de caja y banco
    def menu_caja_banco(self):
        while True:
            print("\n=== MENÚ DE CAJA Y BANCO ===")
            print("1. Ver caja")
            print("2. Ver banco")
            print("3. Editar dinero en caja")
            print("0. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(self._caja)
                input("Presione Enter para continuar...")
            elif opcion == "2":
                print(self._banco)
                input("Presione Enter para continuar...")
            elif opcion == "3":
                self.editar_dinero_caja()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

    def editar_dinero_caja(self):
        print("\n=== Editar Dinero en Caja ===")
        print(f"Dinero actual en caja: S/{self._caja._dinero:.2f}")
        try:
            nuevo_monto = float(input("Nuevo monto en caja: "))
            descripcion = input("Motivo del cambio: ")
            self._caja._dinero = nuevo_monto
            print(f"Dinero en caja actualizado. Motivo: {descripcion}")
        except ValueError:
            print("Monto inválido.")

    # Submenú de proveedores
    def menu_proveedores(self):
        while True:
            print("\n=== MENÚ DE PROVEEDORES ===")
            print("1. Ver proveedores")
            print("2. Editar proveedor")
            print("3. Eliminar proveedor")
            print("0. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                for proveedor in self._proveedores:
                    print(proveedor)
                input("Presione Enter para continuar...")
            elif opcion == "2":
                self.editar_proveedor()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                self.eliminar_proveedor()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

    # Submenú de clientes                
    def menu_clientes(self):
        while True:
            print("\n=== MENU DE CLIENTES ===")
            print("1. Registrar cliente")
            print("2. Ver clientes")
            print("3. Recargar cuenta prepaga")
            print("4. Pagar deuda")
            print("5. Editar cliente")
            print("6. Eliminar cliente")
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
            elif opcion == "5":
                self.editar_cliente()
                input("Presione Enter para continuar...")
            elif opcion == "6":
                self.eliminar_cliente()
                input("Presione Enter para continuar...")
            elif opcion == "0":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    # Método para registrar ventas
    def registrar_venta(self):
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
        
        elif metodo == "3":
            from PagoTransferencia import PagoTransferencia
            metodo_pago = PagoTransferencia(self._banco, total)
        
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

    def registrar_compra(self):
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
                # Buscar producto existente por nombre (ignorando mayúsculas/minúsculas)
                producto_existente = None
                for prod in self._inventario.listar_productos():
                    if prod._nombre.lower() == nombre_producto.lower():
                        producto_existente = prod
                        break

                if producto_existente:
                    print(f"\nProducto '{producto_existente._nombre}' ya registrado en inventario.")
                    print(f"Precio de compra anterior: S/{producto_existente._precio:.2f}")
                    actualizar_precio_compra = input_sn("¿Desea actualizar el precio de compra?")
                    if actualizar_precio_compra:
                        precio_compra = float(input("Nuevo precio unitario de compra: "))
                    else:
                        precio_compra = producto_existente._precio

                    cantidad = int(input("Cantidad a comprar: "))

                    # Solo sumamos stock, no cambiamos nada más
                    producto = Producto(
                        producto_existente._nombre,
                        producto_existente._precio,
                        cantidad,
                        producto_existente._categoria,
                        producto_existente._stock_minimo
                    )
                    self._inventario.agregar_producto(producto)
                    productos_comprados[nombre_producto] = (producto, cantidad, precio_compra, True)
                else:
                    disponible_venta = input_sn("¿El producto estará disponible para la venta?")
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
                    if disponible_venta:
                        while True:
                            precio_venta = float(input("Precio de venta al público: "))
                            if precio_venta > 0:
                                break
                            print("El precio de venta debe ser mayor a 0.")
                        categoria = input("Categoría del producto: ")
                        stock_minimo = int(input("Stock mínimo para alerta: "))
                        producto = Producto(nombre_producto, precio_venta, cantidad, categoria, stock_minimo)
                        self._inventario.agregar_producto(producto)
                        productos_comprados[nombre_producto] = (producto, cantidad, precio_compra, disponible_venta)
                    else:
                        # No se crea ni agrega producto al inventario, solo se registra la compra
                        productos_comprados[nombre_producto] = (None, cantidad, precio_compra, disponible_venta)
            except ValueError:
                print("Entrada inválida.")
        if not productos_comprados:
            print("No se ingresaron productos para la compra.")
            return
        fecha = input("Ingrese la fecha de la compra (ej: 21/05/2025): ")
        total_compra = sum(cantidad * precio_compra for _, cantidad, precio_compra, _ in productos_comprados.values())
        if self._caja._dinero < total_compra:
            print("No hay suficiente dinero en caja para pagar al proveedor.")
            return
        self._caja._dinero -= total_compra
        proveedor.recibir_pago(total_compra)
        compra = Compra(proveedor, fecha, productos_comprados)
        self._compras.append(compra)
        print(f"Compra registrada y pagada a {proveedor._nombre} por S/{total_compra:.2f}")    
        
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

    def agregar_producto(self):
        print("\n=== Agregar Producto para la Venta ===")
        nombre = input("Nombre del producto: ")
        # Buscar producto existente por nombre (ignorando mayúsculas/minúsculas)
        producto_existente = None
        for prod in self._inventario.listar_productos():
            if prod._nombre.lower() == nombre.lower():
                producto_existente = prod
                break

        if producto_existente:
            print(f"\nProducto '{producto_existente._nombre}' ya registrado en inventario.")
            print(f"Precio actual: S/{producto_existente._precio:.2f}")
            actualizar_precio = input_sn("¿Desea actualizar el precio de venta?")
            if actualizar_precio:
                precio = float(input("Nuevo precio de venta: "))
            else:
                precio = producto_existente._precio

            print(f"Categoría actual: {producto_existente._categoria}")
            actualizar_categoria = input_sn("¿Desea actualizar la categoría?")
            if actualizar_categoria:
                categoria = input("Nueva categoría: ")
            else:
                categoria = producto_existente._categoria

            print(f"Stock mínimo actual: {producto_existente._stock_minimo}")
            actualizar_stock_minimo = input_sn("¿Desea actualizar el stock mínimo?")
            if actualizar_stock_minimo:
                stock_minimo = int(input("Nuevo stock mínimo para alerta: "))
            else:
                stock_minimo = producto_existente._stock_minimo

            stock = int(input("Cantidad a agregar al stock: "))
            # Creamos un producto temporal solo para pasar a agregar_producto (sumará stock)
            producto = Producto(producto_existente._nombre, precio, stock, categoria, stock_minimo)
            self._inventario.agregar_producto(producto)
            print("Stock sumado al producto existente.")
        else:
            precio = float(input("Precio de venta: "))
            stock = int(input("Stock inicial: "))
            categoria = input("Categoría: ")
            stock_minimo = int(input("Stock mínimo para alerta: "))
            producto = Producto(nombre, precio, stock, categoria, stock_minimo)
            self._inventario.agregar_producto(producto)
            print("Producto agregado al inventario.")

    # --- NUEVAS FUNCIONES DE EDICIÓN Y ELIMINACIÓN ---

    def editar_cliente(self):
        print("\n=== Editar Cliente ===")
        if not self._clientes:
            print("No hay clientes registrados.")
            return
        for idx, cliente in enumerate(self._clientes):
            print(f"{idx+1}. {cliente._nombre}")
        try:
            idx_cliente = int(input("Seleccione el cliente a editar: ")) - 1
            cliente = self._clientes[idx_cliente]
            nuevo_nombre = input(f"Nuevo nombre (actual: {cliente._nombre}): ") or cliente._nombre
            nuevo_grado = input(f"Nuevo grado (actual: {cliente._grado}): ") or cliente._grado
            cliente._nombre = nuevo_nombre
            cliente._grado = nuevo_grado
            print("Cliente editado correctamente.")
        except (ValueError, IndexError):
            print("Selección inválida.")

    def eliminar_cliente(self):
        print("\n=== Eliminar Cliente ===")
        if not self._clientes:
            print("No hay clientes registrados.")
            return
        for idx, cliente in enumerate(self._clientes):
            print(f"{idx+1}. {cliente._nombre}")
        try:
            idx_cliente = int(input("Seleccione el cliente a eliminar: ")) - 1
            cliente = self._clientes.pop(idx_cliente)
            print(f"Cliente '{cliente._nombre}' eliminado correctamente.")
        except (ValueError, IndexError):
            print("Selección inválida.")

    def editar_producto(self):
        print("\n=== Editar Producto ===")
        productos = self._inventario.listar_productos()
        if not productos:
            print("No hay productos en el inventario.")
            return
        for p in productos:
            print(f"{p._id}: {p._nombre} (Stock: {p._stock}, Precio: S/{p._precio:.2f})")
        try:
            id_producto = int(input("Ingrese el ID del producto a editar: "))
            producto = self._inventario.buscar_producto(id_producto)
            if not producto:
                print("Producto no encontrado.")
                return
            nuevo_nombre = input(f"Nuevo nombre (actual: {producto._nombre}): ") or producto._nombre
            nuevo_precio = input(f"Nuevo precio (actual: {producto._precio}): ")
            nuevo_stock = input(f"Nuevo stock (actual: {producto._stock}): ")
            nueva_categoria = input(f"Nueva categoría (actual: {producto._categoria}): ") or producto._categoria
            producto._nombre = nuevo_nombre
            if nuevo_precio:
                producto._precio = float(nuevo_precio)
            if nuevo_stock:
                producto._stock = int(nuevo_stock)
            producto._categoria = nueva_categoria
            print("Producto editado correctamente.")
        except ValueError:
            print("Entrada inválida.")

    def eliminar_producto(self):
        print("\n=== Eliminar Producto ===")
        productos = self._inventario.listar_productos()
        if not productos:
            print("No hay productos en el inventario.")
            return
        for p in productos:
            print(f"{p._id}: {p._nombre} (Stock: {p._stock})")
        try:
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            self._inventario.eliminar_producto(id_producto)
            print("Producto eliminado correctamente.")
        except (ValueError, KeyError):
            print("Producto no encontrado o entrada inválida.")

    def editar_proveedor(self):
        print("\n=== Editar Proveedor ===")
        if not self._proveedores:
            print("No hay proveedores registrados.")
            return
        for idx, proveedor in enumerate(self._proveedores):
            print(f"{idx+1}. {proveedor._nombre}")
        try:
            idx_prov = int(input("Seleccione el proveedor a editar: ")) - 1
            proveedor = self._proveedores[idx_prov]
            nuevo_nombre = input(f"Nuevo nombre (actual: {proveedor._nombre}): ") or proveedor._nombre
            proveedor._nombre = nuevo_nombre
            print("Proveedor editado correctamente.")
        except (ValueError, IndexError):
            print("Selección inválida.")

    def eliminar_proveedor(self):
        print("\n=== Eliminar Proveedor ===")
        if not self._proveedores:
            print("No hay proveedores registrados.")
            return
        for idx, proveedor in enumerate(self._proveedores):
            print(f"{idx+1}. {proveedor._nombre}")
        try:
            idx_prov = int(input("Seleccione el proveedor a eliminar: ")) - 1
            proveedor = self._proveedores.pop(idx_prov)
            print(f"Proveedor '{proveedor._nombre}' eliminado correctamente.")
        except (ValueError, IndexError):
            print("Selección inválida.")
    
    def reporte_ventas(self):
        print("\n=== REPORTE DE VENTAS ===")
        total = 0
        for venta in self._ventas:
            print(venta)
            total += venta.total
        print(f"Total vendido: S/{total:.2f}")

    def reporte_compras(self):
        print("\n=== REPORTE DE COMPRAS ===")
        total = 0
        for compra in self._compras:
            print(compra)
            total += compra.total
        print(f"Total comprado: S/{total:.2f}")
        
    def alerta_bajo_stock(self):
        bajo_stock = self._inventario.productos_bajo_stock()
        if bajo_stock:
            print("\nALERTA: Productos con bajo stock")
            for p in bajo_stock:
                print(f"- {p._nombre} (Stock: {p._stock}, Mínimo: {p._stock_minimo})")
            input("Presione Enter para continuar...")