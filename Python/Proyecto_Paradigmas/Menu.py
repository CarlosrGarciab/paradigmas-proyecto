from Producto import Producto
from Venta import Venta
from Compra import Compra
from Proveedor import Proveedor

class MenuClientes:
    def __init__(self, menu):
        self.menu = menu

    def mostrar(self):
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
                self.menu.registrar_cliente()
            elif opcion == "2":
                print("\n=== Clientes ===")
                self.menu._mostrar_lista(self.menu._clientes)
            elif opcion == "3":
                self.menu.recargar_prepago_cliente()
            elif opcion == "4":
                self.menu.pagar_deuda_cliente()
            elif opcion == "5":
                self.menu.editar_cliente()
            elif opcion == "6":
                self.menu.eliminar_cliente()
            elif opcion == "0":
                break
            else:
                print("Opción no válida. Intente de nuevo.")
            self.menu.pausar()

class MenuProductos:
    def __init__(self, menu):
        self.menu = menu

    def mostrar(self):
        while True:
            print("\n=== MENÚ DE PRODUCTOS ===")
            print("1. Ver inventario")
            print("2. Agregar producto")
            print("3. Editar producto")
            print("4. Eliminar producto")
            print("0. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(self.menu._inventario)
            elif opcion == "2":
                self.menu.agregar_producto()
            elif opcion == "3":
                self.menu.editar_producto()
            elif opcion == "4":
                self.menu.eliminar_producto()
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")
            self.menu.pausar()

class Menu:
    """
    Clase principal para la interacción con el usuario.
    Gestiona el flujo de la aplicación y delega la lógica de negocio a las clases de dominio.
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
        self.menu_clientes = MenuClientes(self)
        self.menu_productos = MenuProductos(self)

    # Funciones auxiliares para validación de entradas
    def pedir_float(self, mensaje, minimo=None, maximo=None, permitir_vacio=False):
        while True:
            valor = input(mensaje)
            if permitir_vacio and valor.strip() == "":
                return None
            try:
                f = float(valor)
                if minimo is not None and f < minimo:
                    print(f"El valor debe ser mayor o igual a {minimo}.")
                    continue
                if maximo is not None and f > maximo:
                    print(f"El valor debe ser menor o igual a {maximo}.")
                    continue
                return f
            except ValueError:
                print("Debe ingresar un número válido.")

    def pedir_int(self, mensaje, minimo=None, maximo=None, permitir_vacio=False):
        while True:
            valor = input(mensaje)
            if permitir_vacio and valor.strip() == "":
                return None
            try:
                i = int(valor)
                if minimo is not None and i < minimo:
                    print(f"El valor debe ser mayor o igual a {minimo}.")
                    continue
                if maximo is not None and i > maximo:
                    print(f"El valor debe ser menor o igual a {maximo}.")
                    continue
                return i
            except ValueError:
                print("Debe ingresar un número entero válido.")

    def pedir_fecha(self, mensaje):
        while True:
            fecha = input(mensaje)
            if fecha.strip() == "":
                print("La fecha no puede estar vacía.")
                continue
            # Aquí podrías validar formato si lo deseas
            return fecha

    def pausar(self):
        input("Presione Enter para continuar...")

    def mostrar(self):
        """
        Muestra el menú principal y gestiona la navegación entre opciones.
        Usa un diccionario para mapear opciones a funciones.
        """
        def pausar():
            self.pausar()

        opciones = {
            "1": lambda: (self.registrar_venta(), self.alerta_bajo_stock(), pausar()),
            "2": lambda: (self.registrar_compra(), self.alerta_bajo_stock(), pausar()),
            "3": self.menu_productos.mostrar,
            "4": self.menu_caja_banco,
            "5": self.menu_proveedores,
            "6": self.menu_clientes.mostrar,
            "7": lambda: (self.ver_ventas(), pausar()),
            "8": lambda: (self.ver_compras(), pausar()),
            "0": self.salir
        }

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
            accion = opciones.get(opcion)
            if accion:
                accion()
            else:
                print("Opción no válida. Intente de nuevo.")

    def salir(self):
        self.alerta_bajo_stock()
        print("Saliendo del sistema...")
        exit()

    def ver_ventas(self):
        """
        Muestra el historial de ventas y el total vendido.
        """
        print("\n=== HISTORIAL DE VENTAS Y TOTAL ===")
        total = 0
        for venta in self._ventas:
            print(venta)
            print()
            total += venta.total
        print(f"Total vendido: S/{total:.2f}")
        self.pausar()

    def ver_compras(self):
        """
        Muestra el historial de compras y el total comprado.
        """
        print("\n=== HISTORIAL DE COMPRAS Y TOTAL ===")
        total = 0
        for compra in self._compras:
            print(compra)
            print()
            total += compra.total
        print(f"Total comprado: S/{total:.2f}")
        self.pausar()

    def menu_caja_banco(self):
        """
        Submenú para ver y modificar el dinero en caja y banco.
        """
        while True:
            print("\n=== MENÚ CAJA/BANCO ===")
            print("1. Caja")
            print("2. Modificar dinero en caja")
            print("3. Banco")
            print("4. Modificar dinero en banco")
            print("0. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(f"Dinero en caja: S/{self._caja.dinero:.2f}")
                self.pausar()
            elif opcion == "2":
                print(f"Dinero actual en caja: S/{self._caja.dinero:.2f}")
                nuevo_monto = self.pedir_float("Ingrese el nuevo monto para la caja: ", minimo=0)
                if nuevo_monto is not None:
                    self._caja.dinero = nuevo_monto
                    print("Monto de caja actualizado.")
                self.pausar()
            elif opcion == "3":
                print(f"Dinero en banco: S/{self._banco.saldo:.2f}")
                self.pausar()
            elif opcion == "4":
                print(f"Dinero actual en banco: S/{self._banco.saldo:.2f}")
                nuevo_monto = self.pedir_float("Ingrese el nuevo monto para el banco: ", minimo=0)
                if nuevo_monto is not None:
                    self._banco.saldo = nuevo_monto
                    print("Monto de banco actualizado.")
                self.pausar()
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

    def _mostrar_lista(self, lista, attr="nombre"):
        """
        Muestra una lista de objetos por un atributo dado.
        """
        for idx, elem in enumerate(lista, 1):
            print(f"{idx}. {getattr(elem, attr)}")

    def _seleccionar_elemento(self, lista, prompt="Seleccione un elemento: "):
        """
        Permite seleccionar un elemento de una lista por índice.
        Devuelve el elemento seleccionado o None si la selección es inválida.
        Permite reintentar en caso de error.
        """
        while True:
            try:
                idx = int(input(prompt)) - 1
                if 0 <= idx < len(lista):
                    return lista[idx]
                else:
                    print("Selección inválida.")
            except ValueError as e:
                print(f"Debe ingresar un número válido. ({e})")
            except Exception as e:
                print(f"Error inesperado: {e}")
            retry = input("¿Desea intentar de nuevo? (s/n): ").strip().lower()
            if retry != "s":
                break
        return None

    def agregar_producto(self):
        """
        Permite agregar un nuevo producto o sumar stock a uno existente.
        Valida todos los datos ingresados.
        """
        print("\n=== Agregar Producto para la Venta ===")
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            return
        producto_existente = self._inventario.buscar_producto_por_nombre(nombre)
        if producto_existente:
            print(f"\nProducto '{producto_existente.nombre}' ya registrado en inventario.")
            print(f"Precio actual: S/{producto_existente.precio:.2f}")
            print(f"Categoría actual: {producto_existente.categoria}")
            print(f"Stock mínimo actual: {producto_existente.stock_minimo}")
            # Validar entrada de stock
            stock = self.pedir_int("Cantidad a agregar al stock: ", minimo=1)
            if stock is not None:
                try:
                    producto_existente.agregar_stock(stock)
                    print("Stock sumado al producto existente.")
                except ValueError as e:
                    print(f"Error: {e}")
        else:
            # Validar precio
            precio = self.pedir_float("Precio de venta: ", minimo=0)
            # Validar stock
            stock = self.pedir_int("Stock inicial: ", minimo=1)
            categoria = input("Categoría: ").strip()
            if not categoria:
                print("La categoría no puede estar vacía.")
                return
            # Validar stock mínimo
            stock_minimo = self.pedir_int("Stock mínimo para alerta: ", minimo=0)
            producto = Producto(nombre, precio, stock, categoria, stock_minimo)
            self._inventario.agregar_producto(producto)
            print("Producto agregado al inventario.")

    def editar_producto(self):
        """
        Permite editar los datos de un producto existente.
        Valida todos los datos ingresados.
        """
        print("\n=== Editar Producto ===")
        productos = self._inventario.listar_productos()
        if not productos:
            print("No hay productos en el inventario.")
            return
        self._mostrar_lista(productos)
        producto = self._seleccionar_elemento(productos, "Seleccione el número del producto a editar: ")
        if not producto:
            return
        nuevo_nombre = input(f"Nuevo nombre (actual: {producto.nombre}): ").strip() or producto.nombre
        if not nuevo_nombre:
            print("El nombre no puede estar vacío. No se realizaron cambios.")
            return
        nuevo_precio = self.pedir_float(f"Nuevo precio (actual: {producto.precio}, Enter para no cambiar): ", minimo=0, permitir_vacio=True)
        nuevo_stock = self.pedir_int(f"Nuevo stock (actual: {producto.stock}, Enter para no cambiar): ", minimo=0, permitir_vacio=True)
        nueva_categoria = input(f"Nueva categoría (actual: {producto.categoria}): ").strip() or producto.categoria
        try:
            producto.actualizar_datos(
                nombre=nuevo_nombre,
                precio=nuevo_precio,
                categoria=nueva_categoria,
                stock_minimo=None  # Puedes agregar si lo pides al usuario
            )
            if nuevo_stock is not None:
                producto.stock = nuevo_stock
            print("Producto editado correctamente.")
        except ValueError as e:
            print(f"Error al editar producto: {e}")

    def eliminar_producto(self):
        """
        Permite eliminar un producto del inventario.
        """
        print("\n=== Eliminar Producto ===")
        productos = self._inventario.listar_productos()
        if not productos:
            print("No hay productos en el inventario.")
            return
        self._mostrar_lista(productos)
        producto = self._seleccionar_elemento(productos, "Seleccione el número del producto a eliminar: ")
        if not producto:
            return
        self._inventario.eliminar_producto(producto.nombre)
        print("Producto eliminado correctamente.")

    def registrar_venta(self):
        """
        Permite registrar una venta, seleccionando productos y método de pago.
        Solo recopila datos y delega la lógica a la clase Venta.
        """
        print("\n=== Registrar Venta ===")
        productos_disponibles = [p for p in self._inventario.listar_productos() if p.stock > 0]
        if not productos_disponibles:
            print("No hay productos con stock disponible para vender.")
            return
        productos_vendidos = {}
        while True:
            print("\nProductos disponibles:")
            for idx, p in enumerate(productos_disponibles, 1):
                seleccionados = productos_vendidos.get(p.nombre, 0)
                disponible = p.stock - seleccionados
                print(f"{idx}. {p.nombre} (Stock disponible: {disponible}, Precio: S/{p.precio:.2f})")
            idx_str = input("Ingrese el número del producto a vender (o '0' para terminar): ")
            if idx_str == "0":
                break
            try:
                idx_producto = int(idx_str) - 1
                if 0 <= idx_producto < len(productos_disponibles):
                    producto = productos_disponibles[idx_producto]
                    seleccionados = productos_vendidos.get(producto.nombre, 0)
                    disponible = producto.stock - seleccionados
                    cantidad = self.pedir_int(f"Ingrese la cantidad de '{producto.nombre}' a vender (disponible: {disponible}): ", minimo=1, maximo=disponible)
                    if cantidad is None:
                        continue
                    productos_vendidos[producto.nombre] = seleccionados + cantidad
                else:
                    print("Selección inválida.")
            except ValueError:
                print("Entrada inválida.")
        if not productos_vendidos:
            print("No se seleccionaron productos para la venta.")
            return

        total = 0
        for nombre_producto, cantidad in productos_vendidos.items():
            producto = self._inventario.buscar_producto_por_nombre(nombre_producto)
            total += producto.precio * cantidad

        print(f"\nTotal de la venta: S/{total:.2f}")
        print("Seleccione el método de pago:")
        print("1. Efectivo")
        print("2. Prepago")
        print("3. Transferencia bancaria")
        print("4. Deuda")

        metodo = input("Opción: ")
        metodo_pago = None
        cliente = None

        try:
            if metodo == "1":
                monto_pago = self.pedir_float("Ingrese el monto recibido en efectivo: ", minimo=total)
                from PagoEfectivo import PagoEfectivo
                metodo_pago = PagoEfectivo(self._caja, monto_pago)
                venta = Venta(productos_vendidos, metodo_pago, self._inventario, self._caja)
            elif metodo == "2":
                from Alumno import Alumno
                alumnos = [c for c in self._clientes if isinstance(c, Alumno)]
                if not alumnos:
                    print("No hay alumnos registrados para prepago.")
                    return
                print("Alumnos disponibles:")
                for idx, a in enumerate(alumnos):
                    print(f"{idx+1}. {a.nombre} (Saldo prepago: S/{a.saldo_prepago:.2f})")
                idx_cliente = self.pedir_int("Seleccione el alumno: ", minimo=1, maximo=len(alumnos))
                if idx_cliente is None:
                    print("Selección inválida.")
                    return
                alumno = alumnos[idx_cliente-1]
                from PagoPrepago import PagoPrepago
                metodo_pago = PagoPrepago(alumno, total)
                venta = Venta(productos_vendidos, metodo_pago, self._inventario, self._caja, alumno)
            elif metodo == "3":
                from PagoTransferencia import PagoTransferencia
                metodo_pago = PagoTransferencia(self._banco, total)
                venta = Venta(productos_vendidos, metodo_pago, self._inventario, self._caja)
            elif metodo == "4":
                if not self._clientes:
                    print("No hay clientes registrados para deuda.")
                    return
                print("Clientes disponibles:")
                for idx, c in enumerate(self._clientes):
                    print(f"{idx+1}. {c.nombre} (Deuda actual: S/{c.deuda:.2f})")
                idx_cliente = self.pedir_int("Seleccione el cliente: ", minimo=1, maximo=len(self._clientes))
                if idx_cliente is None:
                    print("Selección inválida.")
                    return
                cliente = self._clientes[idx_cliente-1]
                from PagoDeuda import PagoDeuda
                metodo_pago = PagoDeuda(cliente, total)
                venta = Venta(productos_vendidos, metodo_pago, self._inventario, self._caja, cliente)
            else:
                print("Método de pago no válido.")
                return

            # Solo delega la lógica de negocio a Venta
            if venta.procesar_venta():
                print("Venta realizada con éxito.")
                if metodo == "1":
                    vuelto = monto_pago - total
                    print(f"Vuelto a entregar: S/{vuelto:.2f}")
                self._ventas.append(venta)
            else:
                print("La venta no pudo completarse. Verifique stock o saldo.")
        except Exception as e:
            print(f"Error al procesar la venta: {e}")
        self.pausar()

    def registrar_compra(self):
        """
        Permite registrar una compra a un proveedor, agregando productos al inventario.
        Solo recopila datos y delega la lógica a la clase Compra.
        """
        def input_sn(mensaje):
            while True:
                resp = input(mensaje + " (s/n): ").strip().lower()
                if resp in ("s", "n"):
                    return resp == "s"
                print("Por favor, ingrese 's' para sí o 'n' para no.")

        print("\n=== Registrar Compra ===")
        nombre_proveedor = input("Ingrese el nombre del proveedor: ").strip()
        if not nombre_proveedor:
            print("El nombre del proveedor no puede estar vacío.")
            return
        proveedor = next((p for p in self._proveedores if p.nombre == nombre_proveedor), None)
        if not proveedor:
            proveedor = Proveedor(nombre_proveedor)
            self._proveedores.append(proveedor)
        productos_comprados = {}
        while True:
            nombre_producto = input("Nombre del producto a comprar (o '0' para terminar): ").strip()
            if nombre_producto == "0":
                break
            if not nombre_producto:
                print("El nombre del producto no puede estar vacío.")
                continue
            try:
                producto_existente = self._inventario.buscar_producto_por_nombre(nombre_producto)
                if producto_existente:
                    precio_compra = self.pedir_float("Precio unitario de compra: ", minimo=0)
                    cantidad = self.pedir_int("Cantidad a comprar: ", minimo=1)
                    productos_comprados[producto_existente] = (cantidad, precio_compra)
                else:
                    disponible_venta = input_sn("¿El producto estará disponible para la venta?")
                    precio_compra = self.pedir_float("Precio unitario de compra: ", minimo=0)
                    cantidad = self.pedir_int("Cantidad a comprar: ", minimo=1)
                    if disponible_venta:
                        precio_venta = self.pedir_float("Precio de venta al público: ", minimo=0)
                        categoria = input("Categoría del producto: ").strip()
                        if not categoria:
                            print("La categoría no puede estar vacía.")
                            continue
                        stock_minimo = self.pedir_int("Stock mínimo para alerta: ", minimo=0)
                        producto = Producto(nombre_producto, precio_venta, cantidad, categoria, stock_minimo)
                        self._inventario.agregar_producto(producto)
                        productos_comprados[producto] = (cantidad, precio_compra)
                    else:
                        productos_comprados[None] = (cantidad, precio_compra)
            except Exception as e:
                print(f"Error al ingresar producto: {e}")
        if not productos_comprados:
            print("No se ingresaron productos para la compra.")
            return

        fecha = self.pedir_fecha("Ingrese la fecha de la compra (ej: 21/05/2025): ")
        total_compra = sum(cantidad * precio_compra for _, (cantidad, precio_compra) in productos_comprados.items())

        print("¿Cómo desea pagar al proveedor?")
        print("1. Caja")
        print("2. Transferencia bancaria")
        metodo_pago = input("Opción: ")

        if metodo_pago == "1":
            if self._caja.dinero < total_compra:
                print("No hay suficiente dinero en caja para pagar al proveedor.")
                return
            self._caja.dinero -= total_compra
            proveedor.recibir_pago(total_compra)
            print(f"Compra registrada y pagada a {proveedor.nombre} por S/{total_compra:.2f} desde CAJA")
        elif metodo_pago == "2":
            if self._banco.saldo < total_compra:
                print("No hay suficiente saldo en banco para pagar al proveedor.")
                return
            self._banco.saldo -= total_compra
            proveedor.recibir_pago(total_compra)
            print(f"Compra registrada y pagada a {proveedor.nombre} por S/{total_compra:.2f} desde BANCO")
        else:
            print("Opción de pago no válida.")
            return

        compra = Compra(proveedor, fecha, productos_comprados)
        self._compras.append(compra)
        self.pausar()

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

        while True:
            nombre = input("Nombre del cliente: ").strip()
            if not nombre:
                print("El nombre no puede estar vacío.")
                continue
            if any(c.nombre == nombre for c in self._clientes):
                print("Ya existe un cliente con ese nombre.")
                return
            break

        # Alumno
        if tipo == "1":
            grado = input("Grado del alumno: ")
            # Validar saldo prepago
            saldo_prepago = self.pedir_float("Saldo inicial en cuenta prepaga: ", minimo=0)
            print("¿Dónde se deposita el saldo prepago?")
            print("1. Caja")
            print("2. Banco")
            metodo_pago = input("Opción: ")
            if metodo_pago not in ("1", "2"):
                print("Opción de depósito no válida. Registro cancelado.")
                return
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
    
    def editar_cliente(self):
        """
        Permite editar el nombre o datos básicos de un cliente.
        """
        if not self._clientes:
            print("No hay clientes registrados.")
            return
        print("\n=== Editar Cliente ===")
        self._mostrar_lista(self._clientes)
        cliente = self._seleccionar_elemento(self._clientes, "Seleccione el número del cliente a editar: ")
        if not cliente:
            return
        nuevo_nombre = input(f"Nuevo nombre (actual: {cliente.nombre}): ").strip()
        if nuevo_nombre:
            cliente.nombre = nuevo_nombre
            print("Nombre actualizado.")
        else:
            print("El nombre no puede estar vacío. No se realizaron cambios.")

        # Edición específica según tipo de cliente
        # Alumno
        try:
            from Alumno import Alumno
            from Profesor import Profesor
        except ImportError:
            Alumno = None
            Profesor = None

        if Alumno and isinstance(cliente, Alumno):
            nuevo_grado = input(f"Nuevo grado (actual: {cliente.grado}): ").strip()
            if nuevo_grado:
                cliente.grado = nuevo_grado
                print("Grado actualizado.")
            # Editar saldo prepago
            saldo = self.pedir_float(f"Nuevo saldo prepago (actual: S/{cliente.saldo_prepago:.2f}, Enter para no cambiar): ", minimo=0, permitir_vacio=True)
            if saldo is not None:
                cliente.saldo_prepago = saldo
                print("Saldo prepago actualizado.")
        elif Profesor and isinstance(cliente, Profesor):
            nuevo_grado = input(f"Nuevo lugar donde enseña (actual: {cliente.grado}): ").strip()
            if nuevo_grado:
                cliente.grado = nuevo_grado
                print("Lugar actualizado.")

    def eliminar_cliente(self):
        """
        Permite eliminar un cliente del sistema.
        """
        cliente = self.seleccionar_y_confirmar(
            self._clientes,
            "Seleccione el número del cliente a eliminar: ",
            "¿Está seguro que desea eliminar este cliente?"
        )
        if cliente:
            self._clientes.remove(cliente)
            print(f"Cliente '{cliente.nombre}' eliminado.")

    def alerta_bajo_stock(self):
        """
        Muestra una alerta si hay productos con stock por debajo del mínimo.
        """
        bajo_stock = self._inventario.productos_bajo_stock()
        if bajo_stock:
            print("\nALERTA: Productos con bajo stock")
            for p in bajo_stock:
                print(f"- {p.nombre} (Stock: {p.stock}, Mínimo: {p.stock_minimo})")
            input("Presione Enter para continuar...")
    
    def recargar_prepago_cliente(self):
        """
        Permite recargar la cuenta prepaga de un alumno.
        """
        from Alumno import Alumno
        alumnos = [c for c in self._clientes if isinstance(c, Alumno)]
        if not alumnos:
            print("No hay alumnos con cuenta prepaga registrados.")
            return
        print("\n=== Recargar Cuenta Prepaga ===")
        self._mostrar_lista(alumnos)
        alumno = self._seleccionar_elemento(alumnos, "Seleccione el alumno a recargar: ")
        if not alumno:
            return
        monto = self.pedir_float("Monto a recargar: ", minimo=0)
        if monto is None:
            return
        print("¿Dónde se deposita la recarga?")
        print("1. Caja")
        print("2. Banco")
        metodo = input("Opción: ")
        if metodo == "1":
            if self._caja.dinero < monto:
                print("No hay suficiente dinero en caja para la recarga.")
                return
            self._caja.dinero -= monto
            alumno.saldo_prepago += monto
            print(f"Recarga realizada desde CAJA. Nuevo saldo prepago: S/{alumno.saldo_prepago:.2f}")
        elif metodo == "2":
            if self._banco.saldo < monto:
                print("No hay suficiente saldo en banco para la recarga.")
                return
            self._banco.saldo -= monto
            alumno.saldo_prepago += monto
            print(f"Recarga realizada desde BANCO. Nuevo saldo prepago: S/{alumno.saldo_prepago:.2f}")
        else:
            print("Opción de depósito no válida.")

    def pagar_deuda_cliente(self):
        """
        Permite pagar la deuda de un cliente.
        """
        clientes_con_deuda = [c for c in self._clientes if getattr(c, "deuda", 0) > 0]
        if not clientes_con_deuda:
            print("No hay clientes con deuda.")
            return
        print("\n=== Pagar Deuda de Cliente ===")
        self._mostrar_lista(clientes_con_deuda)
        cliente = self._seleccionar_elemento(clientes_con_deuda, "Seleccione el cliente a pagar deuda: ")
        if not cliente:
            return
        print(f"Deuda actual: S/{cliente.deuda:.2f}")
        monto = self.pedir_float("Monto a pagar: ", minimo=0)
        if monto is None:
            return
        print("¿Dónde se recibe el pago?")
        print("1. Caja")
        print("2. Banco")
        metodo = input("Opción: ")
        if metodo == "1":
            self._caja.dinero += monto
            cliente.deuda -= monto
            print(f"Pago recibido en CAJA. Deuda restante: S/{cliente.deuda:.2f}")
        elif metodo == "2":
            self._banco.saldo += monto
            cliente.deuda -= monto
            print(f"Pago recibido en BANCO. Deuda restante: S/{cliente.deuda:.2f}")
        else:
            print("Opción de recepción no válida.")

    def menu_proveedores(self):
        """
        Submenú para gestionar proveedores.
        """
        while True:
            print("\n=== MENÚ DE PROVEEDORES ===")
            print("1. Ver proveedores")
            print("2. Registrar proveedor")
            print("0. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                if not self._proveedores:
                    print("No hay proveedores registrados.")
                else:
                    self._mostrar_lista(self._proveedores)
                self.pausar()
            elif opcion == "2":
                nombre = input("Nombre del proveedor: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacío.")
                elif any(p.nombre == nombre for p in self._proveedores):
                    print("Ya existe un proveedor con ese nombre.")
                else:
                    proveedor = Proveedor(nombre)
                    self._proveedores.append(proveedor)
                    print("Proveedor registrado con éxito.")
                self.pausar()
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")