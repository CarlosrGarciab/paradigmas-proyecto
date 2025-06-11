import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import PhotoImage
from Inventario import Inventario
from Caja import Caja
from CuentaBanco import CuentaBanco
from Persistencia import Persistencia

class CantinaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cantina")
        self.root.geometry("700x500")
        self.root.configure(bg="#f5f5f5")
        try:
            self.icon = PhotoImage(file="icono_cantina.png")
            self.root.iconphoto(False, self.icon)
        except Exception:
            pass

        # Inicializa los objetos de dominio
        self.inventario = Persistencia.cargar("inventario.pkl") or Inventario()
        self.caja = Persistencia.cargar("caja.pkl") or Caja()
        self.banco = Persistencia.cargar("banco.pkl") or CuentaBanco()
        self.clientes = Persistencia.cargar("clientes.pkl") or []
        self.proveedores = Persistencia.cargar("proveedores.pkl") or []
        self.ventas = Persistencia.cargar("ventas.pkl") or []
        self.compras = Persistencia.cargar("compras.pkl") or []

        self.alerta_bajo_stock()

        self.crear_menu_principal()

    def crear_menu_principal(self):
        """
        Crea la interfaz gráfica del menú principal con botones para cada opción principal.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True)
        tk.Label(frame, text="MENU PRINCIPAL", font=("Arial", 20, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=20)
        btn_style = {"width": 25, "height": 2, "font": ("Arial", 12), "bg": "#3498db", "fg": "white", "activebackground": "#2980b9", "activeforeground": "#ecf0f1", "bd": 0, "relief": "flat"}
        botones = [
            ("Registrar venta", self.registrar_venta, "🛒"),
            ("Registrar compra", self.registrar_compra, "📦"),
            ("Productos", self.menu_productos, "🍔"),
            ("Caja/Banco", self.menu_caja_banco, "💰"),
            ("Proveedores", self.menu_proveedores, "🚚"),
            ("Clientes", self.menu_clientes, "👤"),
            ("Ventas", self.ver_ventas, "📈"),
            ("Compras", self.ver_compras, "📉"),
            ("Salir", self.salir, "❌")
        ]
        for texto, comando, icono in botones:
            tk.Button(frame, text=f"{icono}  {texto}", command=comando, **btn_style).pack(pady=6)

    def _crear_submenu(self, titulo, opciones):
        """
        Crea un submenú gráfico reutilizable con un título y una lista de opciones (texto, función).
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True)
        tk.Label(frame, text=titulo, font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=15)
        btn_style = {"width": 30, "height": 2, "font": ("Arial", 12), "bg": "#27ae60", "fg": "white", "activebackground": "#229954", "activeforeground": "#ecf0f1", "bd": 0, "relief": "flat"}
        for texto, funcion in opciones:
            tk.Button(frame, text=texto, command=funcion, **btn_style).pack(pady=5)

    def ver_productos(self):
        """
        Muestra el inventario de productos en una ventana desplazable, solo los que tienen stock positivo. Permite buscar por nombre/categoría.
        """
        win = tk.Toplevel(self.root)
        win.title("Inventario de Productos")
        win.geometry("600x500")
        win.configure(bg="#f5f5f5")
        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Buscar producto:", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", padx=5, pady=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(frame, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1")
        entry_buscar.pack(fill=tk.X, padx=5, pady=2)
        columns = ("nombre", "precio", "stock", "categoria", "stock_minimo")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=16)
        tree.heading("nombre", text="Nombre")
        tree.heading("precio", text="Precio")
        tree.heading("stock", text="Stock")
        tree.heading("categoria", text="Categoría")
        tree.heading("stock_minimo", text="Stock Mínimo")
        tree.column("nombre", width=150)
        tree.column("precio", width=80, anchor="e")
        tree.column("stock", width=60, anchor="e")
        tree.column("categoria", width=120)
        tree.column("stock_minimo", width=100, anchor="e")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#2980b9", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=26, background="#f5f5f5", fieldbackground="#f5f5f5")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill=tk.Y)
        def mostrar_productos():
            tree.delete(*tree.get_children())
            filtro = var_buscar.get().lower()
            productos = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True) and p.stock > 0]
            if filtro:
                productos = [p for p in productos if filtro in p.nombre.lower() or filtro in getattr(p, 'categoria', '').lower()]
            for p in productos:
                tree.insert('', 'end', values=(p.nombre, f"S/{p.precio:.2f}", p.stock, getattr(p, 'categoria', ''), getattr(p, 'stock_minimo', '')))
        var_buscar.trace('w', lambda *a: mostrar_productos())
        mostrar_productos()
        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

    def eliminar_producto(self):
        productos = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True)]
        if not productos:
            messagebox.showinfo("Eliminar Producto", "No hay productos disponibles para eliminar.")
            return
        def eliminar(producto, win_busqueda):
            win_busqueda.destroy()
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar '{producto.nombre}' del inventario?")
            if confirm:
                self.inventario.eliminar_producto(producto)
                messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' eliminado del inventario.")
                # Persistencia inmediata
                Persistencia.guardar(self.inventario, "inventario.pkl")
        self.seleccionar_elemento_con_busqueda("producto", productos, "nombre", eliminar)

    def editar_producto(self):
        productos = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True)]
        if not productos:
            messagebox.showinfo("Editar Producto", "No hay productos disponibles para editar.")
            return
        def editar(producto, win_busqueda):
            win_busqueda.destroy()
            win_editar = tk.Toplevel(self.root)
            win_editar.title("Editar Producto")
            win_editar.geometry("400x350")
            tk.Label(win_editar, text=f"Editando: {producto.nombre}").pack()
            tk.Label(win_editar, text="Nuevo nombre:").pack()
            entry_nombre = tk.Entry(win_editar)
            entry_nombre.insert(0, producto.nombre)
            entry_nombre.pack()
            tk.Label(win_editar, text="Nuevo precio:").pack()
            entry_precio = tk.Entry(win_editar)
            entry_precio.insert(0, str(producto.precio))
            entry_precio.pack()
            tk.Label(win_editar, text="Nueva categoría:").pack()
            entry_categoria = tk.Entry(win_editar)
            entry_categoria.insert(0, getattr(producto, 'categoria', ''))
            entry_categoria.pack()
            tk.Label(win_editar, text="Nuevo stock mínimo:").pack()
            entry_stock_minimo = tk.Entry(win_editar)
            entry_stock_minimo.insert(0, str(getattr(producto, 'stock_minimo', 1)))
            entry_stock_minimo.pack()
            def guardar():
                nuevo_nombre = entry_nombre.get().strip()
                try:
                    nuevo_precio = float(entry_precio.get())
                    nuevo_stock_minimo = int(entry_stock_minimo.get())
                except Exception:
                    messagebox.showerror("Error", "Datos inválidos.")
                    return
                producto.nombre = nuevo_nombre
                producto.precio = nuevo_precio
                producto.categoria = entry_categoria.get().strip()
                producto.stock_minimo = nuevo_stock_minimo
                messagebox.showinfo("Éxito", "Producto editado correctamente.")
                Persistencia.guardar(self.inventario, "inventario.pkl")
                win_editar.destroy()
            tk.Button(win_editar, text="Guardar cambios", command=guardar).pack(pady=10)
            tk.Button(win_editar, text="Cancelar", command=win_editar.destroy).pack()
        self.seleccionar_elemento_con_busqueda("producto", productos, "nombre", editar)

    def menu_clientes(self):
        """
        Submenú gráfico para gestionar clientes: registrar, ver, recargar, pagar deuda, editar y eliminar.
        """
        self._crear_submenu(
            "MENÚ DE CLIENTES",
            [
                ("Registrar cliente", self.registrar_cliente),
                ("Ver clientes", self.ver_clientes),
                ("Recargar cuenta prepaga", self.recargar_prepago_cliente),
                ("Pagar deuda", self.pagar_deuda_cliente),
                ("Editar cliente", self.editar_cliente),
                ("Eliminar cliente", self.eliminar_cliente),
                ("Volver", self.crear_menu_principal)
            ]
        )

    def menu_caja_banco(self):
        """
        Submenú gráfico para ver y modificar el dinero en caja y banco.
        """
        self._crear_submenu(
            "MENÚ CAJA/BANCO",
            [
                ("Caja", self.ver_caja),
                ("Modificar dinero en caja", self.modificar_caja),
                ("Banco", self.ver_banco),
                ("Modificar dinero en banco", self.modificar_banco),
                ("Volver", self.crear_menu_principal)
            ]
        )
        
    def ver_caja(self):
        """
        Muestra el dinero actual en caja.
        """
        monto = getattr(self.caja, "dinero", 0.0)
        messagebox.showinfo("Caja", f"Dinero en caja: S/{monto:.2f}")

    def menu_proveedores(self):
        """
        Submenú gráfico para gestionar proveedores: ver, agregar, editar y eliminar.
        """
        win = tk.Toplevel(self.root)
        win.title("Gestión de Proveedores")
        win.geometry("350x350")
        tk.Label(win, text="Seleccione una acción:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(win, text="Ver proveedores", width=25, command=self.ver_proveedores_detallado).pack(pady=5)
        tk.Button(win, text="Agregar proveedor", width=25, command=self.agregar_proveedor).pack(pady=5)
        tk.Button(win, text="Editar proveedor", width=25, command=self.editar_proveedor).pack(pady=5)
        tk.Button(win, text="Eliminar proveedor", width=25, command=self.eliminar_proveedor).pack(pady=5)
        tk.Button(win, text="Cerrar", width=25, command=win.destroy).pack(pady=15)

    def _crear_submenu(self, titulo, opciones):
        """
        Crea un submenú gráfico reutilizable con un título y una lista de opciones (texto, función).
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True)
        tk.Label(frame, text=titulo, font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=15)
        btn_style = {"width": 30, "height": 2, "font": ("Arial", 12), "bg": "#27ae60", "fg": "white", "activebackground": "#229954", "activeforeground": "#ecf0f1", "bd": 0, "relief": "flat"}
        for texto, funcion in opciones:
            tk.Button(frame, text=texto, command=funcion, **btn_style).pack(pady=5)

    # Métodos de ejemplo para cada botón
    def registrar_venta(self):
        """
        Abre una ventana para registrar una venta: selección de productos, cantidades, método de pago y cliente si corresponde.
        """
        from datetime import datetime
        from PagoEfectivo import PagoEfectivo
        from PagoPrepago import PagoPrepago
        from PagoTransferencia import PagoTransferencia
        from PagoDeuda import PagoDeuda
        from Venta import Venta
        from Alumno import Alumno
        from Profesor import Profesor

        # Solo productos disponibles para venta
        productos_disponibles = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True) and p.stock > 0]
        if not productos_disponibles:
            messagebox.showinfo("Registrar Venta", "No hay productos con stock disponible para vender.")
            return

        win = tk.Toplevel(self.root)
        win.title("Registrar Venta")
        win.geometry("600x500")

        tk.Label(win, text="Seleccione productos y cantidades:", font=("Arial", 12, "bold")).pack(pady=5)
        frame_prod = tk.Frame(win)
        frame_prod.pack()
        cantidad_vars = {}
        for p in productos_disponibles:
            f = tk.Frame(frame_prod)
            f.pack(anchor="w")
            tk.Label(f, text=f"{p.nombre} (Stock: {p.stock}, S/{p.precio:.2f})").pack(side="left")
            var = tk.IntVar(value=0)
            cantidad_vars[p.nombre] = var
            tk.Spinbox(f, from_=0, to=p.stock, width=5, textvariable=var).pack(side="left", padx=5)

        label_total = tk.Label(win, text="Total: S/0.00", font=("Arial", 12, "bold"))
        label_total.pack(pady=5)

        def actualizar_total(*args):
            total = 0
            for p in productos_disponibles:
                cant = cantidad_vars[p.nombre].get()
                if cant > 0:
                    total += p.precio * cant
            label_total.config(text=f"Total: S/{total:.2f}")
        for var in cantidad_vars.values():
            var.trace_add('write', actualizar_total)

        # Método de pago
        tk.Label(win, text="Método de pago:").pack()
        var_metodo = tk.StringVar()
        metodos = ["Efectivo", "Prepago", "Transferencia", "Deuda"]
        for m in metodos:
            tk.Radiobutton(win, text=m, variable=var_metodo, value=m).pack(anchor="w")

        # Cliente (solo si es prepago o deuda)
        frame_cliente = tk.Frame(win)
        tk.Label(frame_cliente, text="Cliente (solo para prepago o deuda):").pack(side="left")
        var_cliente = tk.StringVar()
        opciones_clientes = [c.nombre for c in self.clientes]
        if opciones_clientes:
            var_cliente.set(opciones_clientes[0])
        dropdown_cliente = tk.OptionMenu(frame_cliente, var_cliente, *opciones_clientes)
        dropdown_cliente.pack(side="left")
        def mostrar_cliente(*args):
            if var_metodo.get() in ("Prepago", "Deuda"):
                frame_cliente.pack(pady=5)
            else:
                frame_cliente.pack_forget()
        var_metodo.trace('w', mostrar_cliente)

        # Botón para registrar venta
        def guardar():
            productos_vendidos = {}
            for p in productos_disponibles:
                cant = cantidad_vars[p.nombre].get()
                if cant > 0:
                    if cant > p.stock:
                        messagebox.showerror("Error", f"No hay suficiente stock de {p.nombre}.")
                        return
                    productos_vendidos[p.nombre] = cant
            if not productos_vendidos:
                messagebox.showerror("Error", "Debe seleccionar al menos un producto.")
                return
            total = sum(self.inventario.buscar_producto_por_nombre(n).precio * c for n, c in productos_vendidos.items())
            metodo = var_metodo.get()
            if metodo not in metodos:
                messagebox.showerror("Error", "Seleccione un método de pago.")
                return
            cliente = None
            metodo_pago = None
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            try:
                if metodo == "Efectivo":
                    monto_entregado = tk.simpledialog.askfloat("Pago en efectivo", f"Total a pagar: S/{total:.2f}\nIngrese el monto entregado por el cliente:")
                    if monto_entregado is None:
                        return  # Cancelado
                    if monto_entregado < total:
                        messagebox.showerror("Error", "El monto entregado es menor al total a pagar.")
                        return
                    vuelto = monto_entregado - total
                    if self.caja.dinero is not None:
                        self.caja.dinero += total
                    metodo_pago = PagoEfectivo(self.caja, total)
                    messagebox.showinfo("Vuelto", f"Vuelto a entregar al cliente: S/{vuelto:.2f}")
                elif metodo == "Prepago":
                    alumnos = [c for c in self.clientes if hasattr(c, 'saldo_prepago')]
                    if not alumnos:
                        messagebox.showerror("Error", "No hay alumnos con cuenta prepaga.")
                        return
                    nombre_sel = var_cliente.get()
                    cliente = next((a for a in alumnos if a.nombre == nombre_sel), None)
                    if not cliente:
                        messagebox.showerror("Error", "Seleccione un alumno válido.")
                        return
                    if cliente.saldo_prepago < total:
                        messagebox.showerror("Error", f"Saldo prepago insuficiente para {cliente.nombre}.")
                        return
                    cliente.saldo_prepago -= total
                    metodo_pago = PagoPrepago(cliente, total)
                elif metodo == "Transferencia":
                    if self.banco.saldo is not None:
                        self.banco.saldo += total
                    metodo_pago = PagoTransferencia(self.banco, total)
                elif metodo == "Deuda":
                    clientes_deuda = [c for c in self.clientes if hasattr(c, 'deuda') or hasattr(c, 'saldo_prepago')]
                    nombre_sel = var_cliente.get()
                    cliente = next((c for c in self.clientes if c.nombre == nombre_sel), None)
                    if not cliente:
                        messagebox.showerror("Error", "Seleccione un cliente válido.")
                        return
                    if not hasattr(cliente, 'deuda'):
                        cliente.deuda = 0
                    cliente.deuda += total
                    metodo_pago = PagoDeuda(cliente, total)
                else:
                    messagebox.showerror("Error", "Método de pago no válido.")
                    return
                # Actualizar stock
                for nombre, cant in productos_vendidos.items():
                    prod = self.inventario.buscar_producto_por_nombre(nombre)
                    prod.stock -= cant
                # Registrar venta
                venta = Venta(productos_vendidos, metodo_pago, self.inventario, self.caja, fecha=fecha)
                venta.calcular_total()  # Asegura que el total se calcule y se guarde en el objeto
                self.ventas.append(venta)
                messagebox.showinfo("Éxito", "Venta registrada correctamente.")
                # Persistencia inmediata
                Persistencia.guardar(self.ventas, "ventas.pkl")
                Persistencia.guardar(self.inventario, "inventario.pkl")
                Persistencia.guardar(self.caja, "caja.pkl")
                Persistencia.guardar(self.banco, "banco.pkl")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")

        tk.Button(win, text="Registrar Venta", command=guardar, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def registrar_compra(self):
        """
        Abre una ventana para registrar una compra: seleccionar proveedor, productos, cantidades, precios y método de pago.
        """
        import tkinter as tk
        from datetime import datetime
        from Compra import Compra
        from Proveedor import Proveedor
        from Producto import Producto

        win = tk.Toplevel(self.root)
        win.title("Registrar Compra")
        win.geometry("700x650")

        # --- Selección o registro de proveedor ---
        tk.Label(win, text="Proveedor:", font=("Arial", 12, "bold")).pack(pady=5)
        frame_prov = tk.Frame(win)
        frame_prov.pack()
        opciones_prov = [p.nombre for p in self.proveedores]
        var_prov = tk.StringVar()
        entry_prov = tk.Entry(frame_prov)
        entry_prov.pack(side="left")
        if opciones_prov:
            var_prov.set(opciones_prov[0])
            dropdown = tk.OptionMenu(frame_prov, var_prov, *opciones_prov)
            dropdown.pack(side="left", padx=5)
        def set_entry_prov(*args):
            entry_prov.delete(0, tk.END)
            entry_prov.insert(0, var_prov.get())
        if opciones_prov:
            var_prov.trace('w', set_entry_prov)

        # --- Selección de productos, cantidades y precios de compra ---
        tk.Label(win, text="Productos a comprar:", font=("Arial", 12, "bold")).pack(pady=5)
        frame_prod = tk.Frame(win)
        frame_prod.pack()
        # Mostrar todos los productos del inventario excepto los hechos por la cantina
        productos_existentes = [p for p in self.inventario.listar_productos() if not getattr(p, 'es_cantina', False)]
        productos_vars = []  # [(producto, cantidad_var, precio_var, disponible_var)]
        for p in productos_existentes:
            f = tk.Frame(frame_prod)
            f.pack(anchor="w")
            tk.Label(f, text=f"{p.nombre}").pack(side="left")
            tk.Label(f, text="Cantidad:").pack(side="left")
            var_cant = tk.IntVar(value=0)
            tk.Spinbox(f, from_=0, to=1000, width=5, textvariable=var_cant).pack(side="left")
            tk.Label(f, text="Precio compra:").pack(side="left")
            var_precio = tk.DoubleVar(value=p.precio)
            tk.Entry(f, width=7, textvariable=var_precio).pack(side="left")
            var_cant = tk.IntVar(value=0)
            tk.Spinbox(f, from_=0, to=1000, width=5, textvariable=var_cant).pack(side="left")
            tk.Label(f, text="Precio compra:").pack(side="left")
            var_precio = tk.DoubleVar(value=p.precio)
            tk.Entry(f, width=7, textvariable=var_precio).pack(side="left")
            var_disponible = tk.BooleanVar(value=getattr(p, 'disponible', True))
            tk.Checkbutton(f, text="Disponible para venta", variable=var_disponible).pack(side="left", padx=5)
            productos_vars.append((p, var_cant, var_precio, var_disponible))

        # Permitir agregar producto nuevo
        tk.Label(win, text="Agregar producto nuevo (opcional):", font=("Arial", 10)).pack(pady=5)
        frame_nuevo = tk.Frame(win)
        frame_nuevo.pack()
        entry_nuevo_nombre = tk.Entry(frame_nuevo, width=15)
        entry_nuevo_nombre.pack(side="left")
        entry_nuevo_cant = tk.Entry(frame_nuevo, width=5)
        entry_nuevo_cant.pack(side="left", padx=2)
        entry_nuevo_precio = tk.Entry(frame_nuevo, width=7)
        entry_nuevo_precio.pack(side="left", padx=2)
        var_nuevo_disponible = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_nuevo, text="Disponible para venta", variable=var_nuevo_disponible).pack(side="left", padx=5)
        tk.Label(frame_nuevo, text="(nombre, cantidad, precio)").pack(side="left")

        # --- Método de pago ---
        tk.Label(win, text="Método de pago:").pack(pady=5)
        var_metodo = tk.StringVar()
        tk.Radiobutton(win, text="Caja", variable=var_metodo, value="Caja").pack(anchor="w")
        tk.Radiobutton(win, text="Banco", variable=var_metodo, value="Banco").pack(anchor="w")

        # --- Botón para registrar compra ---
        def guardar():
            try:
                # Validar proveedor
                nombre_prov = entry_prov.get().strip()
                if not nombre_prov:
                    messagebox.showerror("Error", "Debe ingresar o seleccionar un proveedor.")
                    return
                proveedor = next((p for p in self.proveedores if p.nombre == nombre_prov), None)
                if not proveedor:
                    proveedor = Proveedor(nombre_prov, contacto="", telefono="")
                    self.proveedores.append(proveedor)

                productos_comprados = {}
                # Productos existentes
                for p, var_cant, var_precio, var_disponible in productos_vars:
                    cant = var_cant.get()
                    precio = var_precio.get()
                    disponible = var_disponible.get() if hasattr(var_disponible, 'get') else True
                    if cant > 0:
                        # En vez de modificar el objeto p (que ya está en inventario), crear un nuevo Producto solo para sumar stock
                        from Producto import Producto
                        producto_sumar = Producto(p.nombre, p.precio, cant, p.categoria, p.stock_minimo)
                        producto_sumar.disponible = disponible
                        self.inventario.agregar_producto(producto_sumar)
                        # Actualizar precio/disponible/categoría/stock_minimo en el producto real
                        p.precio = precio
                        p.disponible = disponible
                        p.categoria = getattr(p, 'categoria', None)
                        p.stock_minimo = getattr(p, 'stock_minimo', 1)
                        productos_comprados[p.nombre] = (cant, precio, disponible)
                # Producto nuevo
                nombre_nuevo = entry_nuevo_nombre.get().strip()
                cant_nuevo = entry_nuevo_cant.get().strip()
                precio_nuevo = entry_nuevo_precio.get().strip()
                disponible_nuevo = var_nuevo_disponible.get() if hasattr(var_nuevo_disponible, 'get') else True
                if nombre_nuevo and cant_nuevo and precio_nuevo:
                    try:
                        cant_nuevo = int(cant_nuevo)
                        precio_nuevo = float(precio_nuevo)
                        if cant_nuevo <= 0:
                            messagebox.showerror("Error", f"La cantidad para '{nombre_nuevo}' debe ser mayor a 0.")
                            return
                        if precio_nuevo < 0:
                            messagebox.showerror("Error", f"El precio para '{nombre_nuevo}' no puede ser negativo.")
                            return
                        nuevo = Producto(nombre_nuevo, precio_nuevo, cant_nuevo)
                        nuevo.disponible = disponible_nuevo
                        self.inventario.agregar_producto(nuevo)
                        productos_comprados[nombre_nuevo] = (cant_nuevo, precio_nuevo, disponible_nuevo)
                    except Exception as e:
                        messagebox.showerror("Error", f"Error en producto nuevo: {e}")
                        return
                if not productos_comprados:
                    messagebox.showerror("Error", "Debe seleccionar o agregar al menos un producto.")
                    return
                metodo = var_metodo.get()
                if metodo not in ("Caja", "Banco"):
                    messagebox.showerror("Error", "Seleccione un método de pago.")
                    return
                # Registrar compra
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                compra = Compra(proveedor, fecha, productos_comprados)
                self.compras.append(compra)
                # Actualizar caja/banco
                total = sum(cant * precio for (cant, precio, _) in productos_comprados.values())
                if metodo == "Caja":
                    self.caja.dinero -= total
                else:
                    self.banco.saldo -= total
                messagebox.showinfo("Éxito", "Compra registrada correctamente.")
                # Persistencia inmediata
                from Persistencia import guardar as guardar_p
                guardar_p(self.compras, "compras.pkl")
                guardar_p(self.inventario, "inventario.pkl")
                guardar_p(self.caja, "caja.pkl")
                guardar_p(self.banco, "banco.pkl")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado al registrar la compra: {e}")

        tk.Button(win, text="Registrar Compra", command=guardar, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def ver_productos(self):
        """
        Muestra el inventario de productos en una ventana desplazable, solo los que tienen stock positivo. Permite buscar por nombre/categoría.
        """
        win = tk.Toplevel(self.root)
        win.title("Inventario de Productos")
        win.geometry("600x500")
        win.configure(bg="#f5f5f5")
        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Buscar producto:", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", padx=5, pady=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(frame, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1")
        entry_buscar.pack(fill=tk.X, padx=5, pady=2)
        columns = ("nombre", "precio", "stock", "categoria", "stock_minimo")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=16)
        tree.heading("nombre", text="Nombre")
        tree.heading("precio", text="Precio")
        tree.heading("stock", text="Stock")
        tree.heading("categoria", text="Categoría")
        tree.heading("stock_minimo", text="Stock Mínimo")
        tree.column("nombre", width=150)
        tree.column("precio", width=80, anchor="e")
        tree.column("stock", width=60, anchor="e")
        tree.column("categoria", width=120)
        tree.column("stock_minimo", width=100, anchor="e")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#2980b9", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=26, background="#f5f5f5", fieldbackground="#f5f5f5")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill=tk.Y)
        def mostrar_productos():
            tree.delete(*tree.get_children())
            filtro = var_buscar.get().lower()
            productos = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True) and p.stock > 0]
            if filtro:
                productos = [p for p in productos if filtro in p.nombre.lower() or filtro in getattr(p, 'categoria', '').lower()]
            for p in productos:
                tree.insert('', 'end', values=(p.nombre, f"S/{p.precio:.2f}", p.stock, getattr(p, 'categoria', ''), getattr(p, 'stock_minimo', '')))
        var_buscar.trace('w', lambda *a: mostrar_productos())
        mostrar_productos()
        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

    def registrar_producto(self):
        """
        Abre un formulario para agregar un producto al inventario. Permite seleccionar uno existente para reponer stock o ingresar uno nuevo.
        """
        # Solo productos disponibles para la venta y agregados desde 'Agregar producto'
        productos_existentes = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True) and getattr(p, 'es_cantina', False) == True]
        nombres_existentes = [p.nombre for p in productos_existentes]

        def autocompletar_campos(*args):
            nombre_sel = var_existente.get()
            if nombre_sel:
                producto = self.inventario.buscar_producto_por_nombre(nombre_sel)
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, producto.nombre)
                entry_precio.delete(0, tk.END)
                entry_precio.insert(0, str(producto.precio))
                entry_categoria.delete(0, tk.END)
                entry_categoria.insert(0, getattr(producto, 'categoria', ''))
                entry_stock_minimo.delete(0, tk.END)
                entry_stock_minimo.insert(0, str(getattr(producto, 'stock_minimo', '')))
                entry_nombre.config(state='readonly')
            else:
                entry_nombre.config(state='normal')
                entry_nombre.delete(0, tk.END)
                entry_precio.delete(0, tk.END)
                entry_categoria.delete(0, tk.END)
                entry_stock_minimo.delete(0, tk.END)

        def guardar():
            nombre = entry_nombre.get().strip()
            try:
                precio = float(entry_precio.get()) if entry_precio.get() else None
                stock = int(entry_stock.get()) if entry_stock.get() else 0
                categoria = entry_categoria.get().strip()
                stock_minimo = int(entry_stock_minimo.get()) if entry_stock_minimo.get() else None
            except Exception:
                messagebox.showerror("Error", "Datos inválidos. Verifique los campos.")
                return
            if not nombre or not categoria:
                messagebox.showerror("Error", "Nombre y categoría no pueden estar vacíos.")
                return
            from Producto import Producto
            producto_existente = self.inventario.buscar_producto_por_nombre(nombre)
            if producto_existente:
                if precio is None:
                    precio = producto_existente.precio
                if not categoria:
                    categoria = producto_existente.categoria
                if stock_minimo is None:
                    stock_minimo = producto_existente.stock_minimo
            producto = Producto(nombre, precio, stock, categoria, stock_minimo)
            producto.es_cantina = True
            producto.disponible = True
            self.inventario.agregar_producto(producto)
            if producto_existente:
                messagebox.showinfo("Éxito", f"Stock actualizado para '{nombre}'. Nuevo stock: {producto_existente.stock}")
            else:
                messagebox.showinfo("Éxito", "Producto agregado al inventario.")
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.inventario, "inventario.pkl")
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Agregar Producto")
        win.geometry("400x350")
        tk.Label(win, text="Seleccionar producto existente (opcional):").pack()
        var_existente = tk.StringVar()
        opciones = ["(Nuevo producto)"] + nombres_existentes
        var_existente.set("")
        dropdown = tk.OptionMenu(win, var_existente, *( [""] + nombres_existentes ), command=lambda _: autocompletar_campos())
        dropdown.pack()
        tk.Label(win, text="Nombre:").pack()
        entry_nombre = tk.Entry(win)
        entry_nombre.pack()
        tk.Label(win, text="Precio:").pack()
        entry_precio = tk.Entry(win)
        entry_precio.pack()
        tk.Label(win, text="Stock a agregar:").pack()
        entry_stock = tk.Entry(win)
        entry_stock.pack()
        tk.Label(win, text="Categoría:").pack()
        entry_categoria = tk.Entry(win)
        entry_categoria.pack()
        tk.Label(win, text="Stock mínimo:").pack()
        entry_stock_minimo = tk.Entry(win)
        entry_stock_minimo.pack()
        var_existente.trace('w', autocompletar_campos)
        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def seleccionar_elemento_con_busqueda(self, titulo, lista, atributo="nombre", callback=None):
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.geometry("400x300")
        tk.Label(win, text=f"Buscar {titulo.lower()}: ").pack(anchor="w", padx=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(win, textvariable=var_buscar)
        entry_buscar.pack(fill=tk.X, padx=5)
        frame_lista = tk.Frame(win)
        frame_lista.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        def actualizar_lista(*args):
            filtro = var_buscar.get().lower()
            listbox.delete(0, tk.END)
            for elem in lista:
                valor = getattr(elem, atributo, str(elem))
                if filtro in str(valor).lower():
                    listbox.insert(tk.END, valor)
        var_buscar.trace('w', actualizar_lista)
        actualizar_lista()
        def seleccionar():
            sel = listbox.curselection()
            if not sel:
                messagebox.showerror("Error", f"Debe seleccionar un {titulo.lower()}.")
                return
            valor = listbox.get(sel[0])
            for elem in lista:
                if getattr(elem, atributo, str(elem)) == valor:
                    if callback:
                        callback(elem, win)
                    else:
                        win.destroy()
                    return
        tk.Button(win, text="Seleccionar", command=seleccionar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()
        return win

    # Refactor de editar_cliente para usar búsqueda
    def editar_cliente(self):
        if not self.clientes:
            messagebox.showinfo("Editar Cliente", "No hay clientes registrados.")
            return
        def editar(cliente, win_busqueda):
            win_busqueda.destroy()
            win_editar = tk.Toplevel(self.root)
            win_editar.title("Editar Cliente")
            win_editar.geometry("400x400")
            tk.Label(win_editar, text=f"Editando: {cliente.nombre}").pack()
            tk.Label(win_editar, text="Nuevo nombre:").pack()
            entry_nombre = tk.Entry(win_editar)
            entry_nombre.insert(0, cliente.nombre)
            entry_nombre.pack()
            tk.Label(win_editar, text="Nuevo grado/lugar:").pack()
            entry_grado = tk.Entry(win_editar)
            entry_grado.insert(0, getattr(cliente, 'grado', ''))
            entry_grado.pack()
            tk.Label(win_editar, text="Nuevo saldo prepago (solo alumno, Enter para no cambiar):").pack()
            entry_saldo = tk.Entry(win_editar)
            if hasattr(cliente, 'saldo_prepago'):
                entry_saldo.insert(0, f"{getattr(cliente, 'saldo_prepago', 0):.2f}")
            entry_saldo.pack()
            def guardar():
                nuevo_nombre = entry_nombre.get().strip() or cliente.nombre
                try:
                    nuevo_grado = entry_grado.get().strip() or cliente.grado
                    saldo_str = entry_saldo.get().strip()
                    if saldo_str and hasattr(cliente, 'saldo_prepago'):
                        saldo = float(saldo_str)
                        if saldo < 0:
                            raise ValueError
                        cliente.saldo_prepago = saldo
                    cliente.nombre = nuevo_nombre
                    cliente.grado = nuevo_grado
                except Exception:
                    messagebox.showerror("Error", "Datos inválidos.")
                    return
                messagebox.showinfo("Éxito", "Cliente editado correctamente.")
                from Persistencia import guardar as guardar_p
                guardar_p(self.clientes, "clientes.pkl")
                win_editar.destroy()
            tk.Button(win_editar, text="Guardar cambios", command=guardar).pack(pady=10)
            tk.Button(win_editar, text="Cancelar", command=win_editar.destroy).pack()
        self.seleccionar_elemento_con_busqueda("cliente", self.clientes, "nombre", editar)

    # Refactor de eliminar_cliente para usar búsqueda
    def eliminar_cliente(self):
        if not self.clientes:
            messagebox.showinfo("Eliminar Cliente", "No hay clientes registrados.")
            return
        def eliminar(cliente, win_busqueda):
            win_busqueda.destroy()
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar a '{cliente.nombre}'?")
            if confirm:
                self.clientes.remove(cliente)
                messagebox.showinfo("Éxito", f"Cliente '{cliente.nombre}' eliminado.")
                from Persistencia import guardar as guardar_p
                guardar_p(self.clientes, "clientes.pkl")
        self.seleccionar_elemento_con_busqueda("cliente", self.clientes, "nombre", eliminar)

    # Refactor de editar_proveedor para usar búsqueda
    def editar_proveedor(self):
        proveedores = self.proveedores if hasattr(self, "proveedores") else []
        if not proveedores:
            messagebox.showinfo("Editar Proveedor", "No hay proveedores registrados.")
            return
        def editar(proveedor, win_busqueda):
            win_busqueda.destroy()
            win_editar = tk.Toplevel(self.root)
            win_editar.title("Editar Proveedor")
            win_editar.geometry("400x300")
            tk.Label(win_editar, text=f"Editando: {proveedor.nombre}").pack()
            tk.Label(win_editar, text="Nuevo nombre:").pack()
            entry_nombre = tk.Entry(win_editar)
            entry_nombre.insert(0, proveedor.nombre)
            entry_nombre.pack()
            tk.Label(win_editar, text="Nuevo contacto:").pack()
            entry_contacto = tk.Entry(win_editar)
            entry_contacto.insert(0, getattr(proveedor, 'contacto', ''))
            entry_contacto.pack()
            tk.Label(win_editar, text="Nuevo teléfono:").pack()
            entry_telefono = tk.Entry(win_editar)
            entry_telefono.insert(0, getattr(proveedor, 'telefono', ''))
            entry_telefono.pack()
            def guardar():
                nuevo_nombre = entry_nombre.get().strip()
                proveedor.nombre = nuevo_nombre
                nuevo_contacto = entry_contacto.get().strip()
                if hasattr(proveedor, 'contacto'):
                    proveedor.contacto = nuevo_contacto
                nuevo_telefono = entry_telefono.get().strip()
                if hasattr(proveedor, 'telefono'):
                    proveedor.telefono = nuevo_telefono
                messagebox.showinfo("Éxito", "Proveedor editado correctamente.")
                from Persistencia import guardar as guardar_p
                guardar_p(self.proveedores, "proveedores.pkl")
                win_editar.destroy()
            tk.Button(win_editar, text="Guardar cambios", command=guardar).pack(pady=10)
            tk.Button(win_editar, text="Cancelar", command=win_editar.destroy).pack()
        self.seleccionar_elemento_con_busqueda("proveedor", proveedores, "nombre", editar)

    # Refactor de eliminar_proveedor para usar búsqueda
    def eliminar_proveedor(self):
        proveedores = self.proveedores if hasattr(self, "proveedores") else []
        if not proveedores:
            messagebox.showinfo("Eliminar Proveedor", "No hay proveedores registrados.")
            return
        def eliminar(proveedor, win_busqueda):
            win_busqueda.destroy()
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar a '{proveedor.nombre}'?")
            if confirm:
                self.proveedores.remove(proveedor)
                messagebox.showinfo("Éxito", f"Proveedor '{proveedor.nombre}' eliminado.")
                from Persistencia import guardar as guardar_p
                guardar_p(self.proveedores, "proveedores.pkl")
        self.seleccionar_elemento_con_busqueda("proveedor", proveedores, "nombre", eliminar)

    def ver_ventas(self):
        """
        Muestra el historial de ventas en una ventana con tabla y detalle.
        """
        if not hasattr(self, 'ventas') or not self.ventas:
            messagebox.showinfo("Ventas", "No hay ventas registradas.")
            return
        win = tk.Toplevel(self.root)
        win.title("Historial de Ventas")
        win.geometry("800x500")
        tk.Label(win, text="Historial de Ventas", font=("Arial", 14, "bold")).pack(pady=5)
        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True)
        columns = ("fecha", "cliente", "metodo", "total")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        tree.heading("fecha", text="Fecha/Hora")
        tree.heading("cliente", text="Cliente")
        tree.heading("metodo", text="Método de Pago")
        tree.heading("total", text="Total (S/)")
        tree.column("fecha", width=160)
        tree.column("cliente", width=180)
        tree.column("metodo", width=120)
        tree.column("total", width=100, anchor="e")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)
        # Llenar la tabla
        for idx, v in enumerate(self.ventas):
            fecha = getattr(v, 'fecha', '')
            cliente = getattr(v, 'cliente', None)
            if cliente and hasattr(cliente, 'nombre'):
                cliente_nombre = cliente.nombre
            else:
                cliente_nombre = str(cliente) if cliente else ''
            metodo_pago = getattr(v, 'metodo_pago', None)
            metodo = metodo_pago.__class__.__name__ if metodo_pago else ''
            total = getattr(v, 'total', None)
            if total is None and hasattr(v, 'calcular_total'):
                total = v.calcular_total()
            tree.insert('', 'end', iid=idx, values=(fecha, cliente_nombre, metodo, f"{total:.2f}" if total is not None else ""))
        # Panel de detalle
        frame_det = tk.Frame(win)
        frame_det.pack(fill=tk.X, padx=10, pady=5)
        label_det = tk.Label(frame_det, text="Seleccione una venta para ver detalles", justify="left", anchor="w")
        label_det.pack(fill=tk.X)
        def mostrar_detalle(event):
            sel = tree.selection()
            if not sel:
                return
            idx = int(sel[0])
            v = self.ventas[idx]
            fecha = getattr(v, 'fecha', '')
            cliente = getattr(v, 'cliente', None)
            if cliente and hasattr(cliente, 'nombre'):
                cliente_nombre = cliente.nombre
            else:
                cliente_nombre = str(cliente) if cliente else ''
            metodo_pago = getattr(v, 'metodo_pago', None)
            metodo = metodo_pago.__class__.__name__ if metodo_pago else ''
            productos = getattr(v, 'productos_vendidos', {})
            total = getattr(v, 'total', None)
            if total is None and hasattr(v, 'calcular_total'):
                total = v.calcular_total()
            detalle = f"Fecha/Hora: {fecha}\nCliente: {cliente_nombre}\nMétodo de pago: {metodo}\n\nProductos vendidos:\n"
            for nombre, cant in productos.items():
                detalle += f"- {nombre}: {cant}\n"
            detalle += f"\nTOTAL: S/{total:.2f}" if total is not None else ""
            label_det.config(text=detalle)
        tree.bind('<<TreeviewSelect>>', mostrar_detalle)
        tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)

    def ver_compras(self):
        """
        Muestra el historial de compras en una ventana con tabla y detalle.
        """
        if not hasattr(self, 'compras') or not self.compras:
            messagebox.showinfo("Compras", "No hay compras registradas.")
            return
        win = tk.Toplevel(self.root)
        win.title("Historial de Compras")
        win.geometry("850x500")
        tk.Label(win, text="Historial de Compras", font=("Arial", 14, "bold")).pack(pady=5)
        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True)
        columns = ("fecha", "proveedor", "total")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        tree.heading("fecha", text="Fecha/Hora")
        tree.heading("proveedor", text="Proveedor")
        tree.heading("total", text="Total (S/)")
        tree.column("fecha", width=160)
        tree.column("proveedor", width=220)
        tree.column("total", width=100, anchor="e")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)
        # Llenar la tabla
        for idx, c in enumerate(self.compras):
            fecha = getattr(c, 'fecha', '')
            proveedor = getattr(getattr(c, 'proveedor', None), 'nombre', '')
            productos = getattr(c, 'productos_comprados', {})
            total = 0
            for datos in productos.values():
                if len(datos) == 3:
                    cant, precio, _ = datos
                else:
                    cant, precio = datos
                total += cant * precio
            tree.insert('', 'end', iid=idx, values=(fecha, proveedor, f"{total:.2f}"))
        # Panel de detalle
        frame_det = tk.Frame(win)
        frame_det.pack(fill=tk.X, padx=10, pady=5)
        label_det = tk.Label(frame_det, text="Seleccione una compra para ver detalles", justify="left", anchor="w")
        label_det.pack(fill=tk.X)
        def mostrar_detalle(event):
            sel = tree.selection()
            if not sel:
                return
            idx = int(sel[0])
            c = self.compras[idx]
            fecha = getattr(c, 'fecha', '')
            proveedor = getattr(getattr(c, 'proveedor', None), 'nombre', '')
            productos = getattr(c, 'productos_comprados', {})
            detalle = f"Fecha/Hora: {fecha}\nProveedor: {proveedor}\n\nProductos comprados:\n"
            total = 0
            for nombre, datos in productos.items():
                if len(datos) == 3:
                    cant, precio, _ = datos
                else:
                    cant, precio = datos
                detalle += f"- {nombre}: {cant} x S/{precio:.2f} = S/{cant*precio:.2f}\n"
                total += cant * precio
            detalle += f"\nTOTAL: S/{total:.2f}"
            label_det.config(text=detalle)
        tree.bind('<<TreeviewSelect>>', mostrar_detalle)
        tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)

    def salir(self):
        # Guarda los datos antes de salir
        Persistencia.guardar(self.inventario, "inventario.pkl")
        Persistencia.guardar(self.caja, "caja.pkl")
        Persistencia.guardar(self.banco, "banco.pkl")
        Persistencia.guardar(self.clientes, "clientes.pkl")
        Persistencia.guardar(self.proveedores, "proveedores.pkl")
        Persistencia.guardar(self.ventas, "ventas.pkl")
        Persistencia.guardar(self.compras, "compras.pkl")
        self.root.destroy()

    def registrar_cliente(self):
        """
        Abre un formulario para registrar un nuevo cliente (alumno o profesor) con validación.
        """
        def guardar():
            tipo = var_tipo.get()
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return
            if any(c.nombre == nombre for c in self.clientes):
                messagebox.showerror("Error", f"El cliente '{nombre}' ya existe.")
                return
            if tipo == "Alumno":
                grado = entry_grado.get().strip()
                try:
                    saldo_prepago = float(entry_saldo.get())
                    if saldo_prepago < 0:
                        raise ValueError
                except Exception:
                    messagebox.showerror("Error", "Saldo prepago inválido.")
                    return
                metodo = var_metodo.get()
                if metodo not in ("Caja", "Banco"):
                    messagebox.showerror("Error", "Seleccione dónde se deposita el saldo prepago.")
                    return
                caja = self.caja if metodo == "Caja" else None
                banco = self.banco if metodo == "Banco" else None
                from Alumno import Alumno
                alumno = Alumno(nombre, grado, saldo_prepago, metodo.lower(), caja, banco)
                self.clientes.append(alumno)
                messagebox.showinfo("Éxito", "Alumno registrado con éxito.")
            elif tipo == "Profesor":
                grado = entry_grado.get().strip()
                from Profesor import Profesor
                profesor = Profesor(nombre, grado)
                self.clientes.append(profesor)
                messagebox.showinfo("Éxito", "Profesor registrado con éxito.")
            else:
                messagebox.showerror("Error", "Seleccione el tipo de cliente.")
                return
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.clientes, "clientes.pkl")
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Registrar Cliente")
        win.geometry("400x400")
        tk.Label(win, text="Tipo de cliente:").pack()
        var_tipo = tk.StringVar(value="Alumno")
        tk.Radiobutton(win, text="Alumno", variable=var_tipo, value="Alumno").pack(anchor="w")
        tk.Radiobutton(win, text="Profesor", variable=var_tipo, value="Profesor").pack(anchor="w")
        tk.Label(win, text="Nombre:").pack()
        entry_nombre = tk.Entry(win)
        entry_nombre.pack()
        tk.Label(win, text="Grado (o lugar donde enseña):").pack()
        entry_grado = tk.Entry(win)
        entry_grado.pack()
        # Para alumno: saldo prepago y método
        tk.Label(win, text="Saldo inicial en cuenta prepaga (solo alumno):").pack()
        entry_saldo = tk.Entry(win)
        entry_saldo.pack()
        tk.Label(win, text="¿Dónde se deposita el saldo prepago? (solo alumno):").pack()
        var_metodo = tk.StringVar()
        tk.Radiobutton(win, text="Caja", variable=var_metodo, value="Caja").pack(anchor="w")
        tk.Radiobutton(win, text="Banco", variable=var_metodo, value="Banco").pack(anchor="w")

        tk.Button(win, text="Registrar", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def recargar_prepago_cliente(self):
        """
        Permite recargar la cuenta prepaga de un alumno desde la GUI, con búsqueda de alumno.
        """
        alumnos = [c for c in self.clientes if hasattr(c, 'saldo_prepago')]
        if not alumnos:
            messagebox.showinfo("Recargar Cuenta Prepaga", "No hay alumnos con cuenta prepaga registrados.")
            return
        win = tk.Toplevel(self.root)
        win.title("Recargar Cuenta Prepaga")
        win.geometry("400x300")
        tk.Label(win, text="Buscar alumno:").pack(anchor="w", padx=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(win, textvariable=var_buscar)
        entry_buscar.pack(fill=tk.X, padx=5)
        tk.Label(win, text="Seleccione el alumno a recargar:").pack()
        var_alumno = tk.StringVar(win)
        lista_nombres = [a.nombre for a in alumnos]
        var_alumno.set(lista_nombres[0])
        dropdown = tk.OptionMenu(win, var_alumno, *lista_nombres)
        dropdown.pack()
        def filtrar_alumnos(*args):
            filtro = var_buscar.get().lower()
            nombres_filtrados = [a.nombre for a in alumnos if filtro in a.nombre.lower()]
            menu = dropdown['menu']
            menu.delete(0, 'end')
            for n in nombres_filtrados:
                menu.add_command(label=n, command=lambda v=n: var_alumno.set(v))
            if nombres_filtrados:
                var_alumno.set(nombres_filtrados[0])
        var_buscar.trace('w', filtrar_alumnos)
        # --- Campos y botones para monto y método de pago ---
        tk.Label(win, text="Monto a recargar:").pack()
        entry_monto = tk.Entry(win)
        entry_monto.pack()
        tk.Label(win, text="¿Dónde se deposita la recarga?").pack()
        var_metodo = tk.StringVar()
        tk.Radiobutton(win, text="Caja", variable=var_metodo, value="Caja").pack(anchor="w")
        tk.Radiobutton(win, text="Banco", variable=var_metodo, value="Banco").pack(anchor="w")
        def guardar():
            nombre_sel = var_alumno.get()
            alumno = next((a for a in alumnos if a.nombre == nombre_sel), None)
            if not alumno:
                messagebox.showerror("Error", "Alumno no encontrado.")
                return
            try:
                monto = float(entry_monto.get())
                if monto < 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Monto inválido.")
                return
            metodo = var_metodo.get()
            if metodo == "Caja":
                if self.caja.dinero < monto:
                    messagebox.showerror("Error", "No hay suficiente dinero en CAJA.")
                    return
                self.caja.dinero -= monto
                alumno.saldo_prepago += monto
                messagebox.showinfo("Éxito", f"Recarga realizada desde CAJA. Nuevo saldo prepago: S/{alumno.saldo_prepago:.2f}")
            elif metodo == "Banco":
                if self.banco.saldo < monto:
                    messagebox.showerror("Error", "No hay suficiente dinero en BANCO.")
                    return
                self.banco.saldo -= monto
                alumno.saldo_prepago += monto
                messagebox.showinfo("Éxito", f"Recarga realizada desde BANCO. Nuevo saldo prepago: S/{alumno.saldo_prepago:.2f}")
            else:
                messagebox.showerror("Error", "Seleccione el origen de la recarga.")
                return
            win.destroy()
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.clientes, "clientes.pkl")
            guardar_p(self.caja, "caja.pkl")
            guardar_p(self.banco, "banco.pkl")
        tk.Button(win, text="Recargar", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def pagar_deuda_cliente(self):
        """
        Permite pagar la deuda de un cliente desde la GUI, con búsqueda de cliente.
        """
        clientes_con_deuda = [c for c in self.clientes if getattr(c, "deuda", 0) > 0]
        if not clientes_con_deuda:
            messagebox.showinfo("Pagar Deuda", "No hay clientes con deuda.")
            return
        win = tk.Toplevel(self.root)
        win.title("Pagar Deuda de Cliente")
        win.geometry("400x300")
        tk.Label(win, text="Buscar cliente:").pack(anchor="w", padx=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(win, textvariable=var_buscar)
        entry_buscar.pack(fill=tk.X, padx=5)
        tk.Label(win, text="Seleccione el cliente a pagar deuda:").pack()
        var_cliente = tk.StringVar(win)
        lista_nombres = [c.nombre for c in clientes_con_deuda]
        var_cliente.set(lista_nombres[0])
        dropdown = tk.OptionMenu(win, var_cliente, *lista_nombres)
        dropdown.pack()
        label_deuda = tk.Label(win, text=f"Deuda actual: S/{getattr(clientes_con_deuda[0], 'deuda', 0):.2f}")
        label_deuda.pack()
        def filtrar_clientes(*args):
            filtro = var_buscar.get().lower()
            nombres_filtrados = [c.nombre for c in clientes_con_deuda if filtro in c.nombre.lower()]
            menu = dropdown['menu']
            menu.delete(0, 'end')
            for n in nombres_filtrados:
                menu.add_command(label=n, command=lambda v=n: var_cliente.set(v))
            if nombres_filtrados:
                var_cliente.set(nombres_filtrados[0])
        var_buscar.trace('w', filtrar_clientes)
        def actualizar_deuda(*args):
            nombre_sel = var_cliente.get()
            cliente = next((c for c in clientes_con_deuda if c.nombre == nombre_sel), None)
            if cliente:
                label_deuda.config(text=f"Deuda actual: S/{getattr(cliente, 'deuda', 0):.2f}")
        var_cliente.trace('w', actualizar_deuda)
        tk.Label(win, text="Monto a pagar:").pack()
        entry_monto = tk.Entry(win)
        entry_monto.pack()
        tk.Label(win, text="¿Dónde se recibe el pago?").pack()
        var_metodo = tk.StringVar()
        tk.Radiobutton(win, text="Caja", variable=var_metodo, value="Caja").pack(anchor="w")
        tk.Radiobutton(win, text="Banco", variable=var_metodo, value="Banco").pack(anchor="w")
        def guardar():
            nombre_sel = var_cliente.get()
            cliente = next((c for c in clientes_con_deuda if c.nombre == nombre_sel), None)
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado.")
                return
            try:
                monto = float(entry_monto.get())
                if monto < 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Monto inválido.")
                return
            if monto > cliente.deuda:
                messagebox.showerror("Error", "El monto no puede ser mayor a la deuda actual.")
                return
            metodo = var_metodo.get()
            if metodo == "Caja":
                self.caja.dinero += monto
                cliente.deuda -= monto
                messagebox.showinfo("Éxito", f"Pago recibido en CAJA. Deuda restante: S/{cliente.deuda:.2f}")
            elif metodo == "Banco":
                self.banco.saldo += monto
                cliente.deuda -= monto
                messagebox.showinfo("Éxito", f"Pago recibido en BANCO. Deuda restante: S/{cliente.deuda:.2f}")
            else:
                messagebox.showerror("Error", "Seleccione el origen del pago.")
                return
            win.destroy()
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.clientes, "clientes.pkl")
            guardar_p(self.caja, "caja.pkl")
            guardar_p(self.banco, "banco.pkl")
        tk.Button(win, text="Pagar", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def modificar_caja(self):
        """
        Permite modificar el dinero en caja mediante un formulario.
        """
        def guardar():
            try:
                nuevo_monto = float(entry_monto.get())
                if nuevo_monto < 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Ingrese un monto válido (mayor o igual a 0).")
                return
            self.caja.dinero = nuevo_monto
            messagebox.showinfo("Éxito", f"Dinero en caja actualizado a S/{nuevo_monto:.2f}")
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.caja, "caja.pkl")
            win.destroy()
        win = tk.Toplevel(self.root)
        win.title("Modificar dinero en caja")
        win.geometry("300x150")
        tk.Label(win, text=f"Dinero actual en caja: S/{self.caja.dinero:.2f}").pack(pady=5)
        tk.Label(win, text="Nuevo monto:").pack()
        entry_monto = tk.Entry(win)
        entry_monto.pack()
        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def ver_banco(self):
        """
        Muestra el saldo actual en banco.
        """
        saldo = self.banco.saldo if hasattr(self.banco, "saldo") else 0.0
        messagebox.showinfo("Banco", f"Dinero en banco: S/{saldo:.2f}")

    def modificar_banco(self):
        """
        Permite modificar el saldo en banco mediante un formulario.
        """
        def guardar():
            try:
                nuevo_monto = float(entry_monto.get())
                if nuevo_monto < 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Ingrese un monto válido (mayor o igual a 0).")
                return
            self.banco.saldo = nuevo_monto
            messagebox.showinfo("Éxito", f"Dinero en banco actualizado a S/{nuevo_monto:.2f}")
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.banco, "banco.pkl")
            win.destroy()
        win = tk.Toplevel(self.root)
        win.title("Modificar dinero en banco")
        win.geometry("300x150")
        tk.Label(win, text=f"Dinero actual en banco: S/{self.banco.saldo:.2f}").pack(pady=5)
        tk.Label(win, text="Nuevo monto:").pack()
        entry_monto = tk.Entry(win)
        entry_monto.pack()
        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def alerta_bajo_stock(self):
        """
        Muestra una alerta visual si hay productos con stock por debajo del mínimo.
        """
        if not hasattr(self, 'inventario'):
            return
        bajo_stock = []
        if hasattr(self.inventario, 'productos_bajo_stock'):
            bajo_stock = self.inventario.productos_bajo_stock()
        elif hasattr(self.inventario, 'productos'):
            bajo_stock = [p for p in self.inventario.productos if hasattr(p, 'stock_minimo') and p.stock <= p.stock_minimo]
        if bajo_stock:
            mensaje = 'ALERTA: Productos con bajo stock\n\n'
            for p in bajo_stock:
                mensaje += f"- {p.nombre} (Stock: {p.stock}, Mínimo: {p.stock_minimo})\n"
            messagebox.showwarning("Alerta de bajo stock", mensaje)

    def editar_cliente(self):
        """
        Permite editar el nombre, grado/lugar y saldo prepago (si es alumno) de un cliente desde la GUI, con búsqueda.
        """
        if not self.clientes:
            messagebox.showinfo("Editar Cliente", "No hay clientes registrados.")
            return
        win = tk.Toplevel(self.root)
        win.title("Editar Cliente")
        win.geometry("400x400")
        tk.Label(win, text="Seleccione un cliente a editar:").pack()
        var_cliente = tk.StringVar(win)
        lista_nombres = [c.nombre for c in self.clientes]
        var_cliente.set(lista_nombres[0])
        dropdown = tk.OptionMenu(win, var_cliente, *lista_nombres)
        dropdown.pack(fill=tk.X, padx=5)
        # Campos de edición
        tk.Label(win, text="Nuevo nombre:").pack()
        entry_nombre = tk.Entry(win)
        entry_nombre.pack()
        tk.Label(win, text="Nuevo grado/lugar:").pack()
        entry_grado = tk.Entry(win)
        entry_grado.pack()
        # Solo para alumnos: saldo prepago
        tk.Label(win, text="Nuevo saldo prepago (solo alumno, Enter para no cambiar):").pack()
        entry_saldo = tk.Entry(win)
        entry_saldo.pack()
        def cargar_datos(*args):
            nombre_sel = var_cliente.get()
            cliente = next((c for c in self.clientes if c.nombre == nombre_sel), None)
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, cliente.nombre)
            entry_grado.delete(0, tk.END)
            entry_grado.insert(0, getattr(cliente, 'grado', ''))
            if hasattr(cliente, 'saldo_prepago'):
                entry_saldo.delete(0, tk.END)
                entry_saldo.insert(0, f"{getattr(cliente, 'saldo_prepago', 0):.2f}")
            else:
                entry_saldo.delete(0, tk.END)
        var_cliente.trace('w', cargar_datos)
        cargar_datos()
        def guardar():
            nombre_sel = var_cliente.get()
            cliente = next((c for c in self.clientes if c.nombre == nombre_sel), None)
            nuevo_nombre = entry_nombre.get().strip() or cliente.nombre
            try:
                nuevo_grado = entry_grado.get().strip() or cliente.grado
                saldo_str = entry_saldo.get().strip()
                if saldo_str and hasattr(cliente, 'saldo_prepago'):
                    saldo = float(saldo_str)
                    if saldo < 0:
                        raise ValueError
                    cliente.saldo_prepago = saldo
                cliente.nombre = nuevo_nombre
                cliente.grado = nuevo_grado
            except Exception:
                messagebox.showerror("Error", "Datos inválidos.")
                return
            messagebox.showinfo("Éxito", "Cliente editado correctamente.")
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.clientes, "clientes.pkl")
            win.destroy()
        tk.Button(win, text="Guardar cambios", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def eliminar_cliente(self):
        """
        Permite eliminar un cliente del sistema desde la GUI, solicitando confirmación y con búsqueda por nombre.
        """
        if not self.clientes:
            messagebox.showinfo("Eliminar Cliente", "No hay clientes registrados.")
            return
        win = tk.Toplevel(self.root)
        win.title("Eliminar Cliente")
        win.geometry("400x250")
        tk.Label(win, text="Buscar cliente:").pack(anchor="w", padx=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(win, textvariable=var_buscar)
        entry_buscar.pack(fill=tk.X, padx=5)
        tk.Label(win, text="Seleccione un cliente a eliminar:").pack()
        var_cliente = tk.StringVar(win)
        lista_nombres = [c.nombre for c in self.clientes]
        var_cliente.set(lista_nombres[0])
        dropdown = tk.OptionMenu(win, var_cliente, *lista_nombres)
        dropdown.pack(fill=tk.X, padx=5)
        def filtrar_clientes(*args):
            filtro = var_buscar.get().lower()
            nombres_filtrados = [c.nombre for c in self.clientes if filtro in c.nombre.lower()]
            menu = dropdown['menu']
            menu.delete(0, 'end')
            for n in nombres_filtrados:
                menu.add_command(label=n, command=lambda v=n: var_cliente.set(v))
            if nombres_filtrados:
                var_cliente.set(nombres_filtrados[0])
        var_buscar.trace('w', filtrar_clientes)
        def eliminar():
            nombre_sel = var_cliente.get()
            cliente = next((c for c in self.clientes if c.nombre == nombre_sel), None)
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado.")
                return
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar a '{cliente.nombre}'?")
            if confirm:
                self.clientes.remove(cliente)
                messagebox.showinfo("Éxito", f"Cliente '{cliente.nombre}' eliminado.")
                # Persistencia inmediata
                from Persistencia import guardar as guardar_p
                guardar_p(self.clientes, "clientes.pkl")
                win.destroy()
        tk.Button(win, text="Eliminar", command=eliminar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def ver_proveedores_detallado(self):
        """
        Muestra la lista de proveedores con detalles (nombre, contacto, teléfono) en una sola línea por proveedor en una ventana desplazable. Permite buscar por nombre/contacto/teléfono.
        """
        win = tk.Toplevel(self.root)
        win.title("Proveedores Registrados")
        win.geometry("500x450")
        tk.Label(win, text="Buscar proveedor:").pack(anchor="w", padx=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(win, textvariable=var_buscar)
        entry_buscar.pack(fill=tk.X, padx=5)
        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        proveedores = self.proveedores if hasattr(self, "proveedores") else []
        def mostrar_proveedores():
            text.delete(1.0, tk.END)
            filtro = var_buscar.get().lower()
            lista = proveedores
            if filtro:
                lista = [p for p in proveedores if filtro in p.nombre.lower() or filtro in str(getattr(p, 'contacto', '')).lower() or filtro in str(getattr(p, 'telefono', '')).lower()]
            if lista:
                for idx, p in enumerate(lista, 1):
                    info = f"{idx}. {p.nombre}"
                    contacto = getattr(p, 'contacto', None)
                    telefono = getattr(p, 'telefono', None)
                    if contacto and str(contacto).strip():
                        info += f" | Contacto: {contacto}"
                    if telefono and str(telefono).strip():
                        info += f" | Tel: {telefono}"
                    text.insert(tk.END, info + "\n")
            else:
                text.insert(tk.END, "No hay proveedores registrados.")
        var_buscar.trace('w', lambda *a: mostrar_proveedores())
        mostrar_proveedores()
        tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)

    def agregar_proveedor(self):
        """
        Abre un formulario para agregar un nuevo proveedor.
        """
        def guardar():
            nombre = entry_nombre.get().strip()
            contacto = entry_contacto.get().strip()
            telefono = entry_telefono.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return
            if any(p.nombre == nombre for p in self.proveedores):
                messagebox.showerror("Error", f"El proveedor '{nombre}' ya existe.")
                return
            from Proveedor import Proveedor
            proveedor = Proveedor(nombre)
            if hasattr(proveedor, 'contacto'):
                proveedor.contacto = contacto
            if hasattr(proveedor, 'telefono'):
                proveedor.telefono = telefono
            self.proveedores.append(proveedor)
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
            # Persistencia inmediata
            from Persistencia import guardar as guardar_p
            guardar_p(self.proveedores, "proveedores.pkl")
            win.destroy()
        win = tk.Toplevel(self.root)
        win.title("Agregar Proveedor")
        win.geometry("350x250")
        tk.Label(win, text="Nombre:").pack()
        entry_nombre = tk.Entry(win)
        entry_nombre.pack()
        tk.Label(win, text="Contacto (opcional):").pack()
        entry_contacto = tk.Entry(win)
        entry_contacto.pack()
        tk.Label(win, text="Teléfono (opcional):").pack()
        entry_telefono = tk.Entry(win)
        entry_telefono.pack()
        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def editar_proveedor(self):
        """
        Permite seleccionar y editar los datos de un proveedor.
        """
        proveedores = self.proveedores if hasattr(self, "proveedores") else []
        if not proveedores:
            messagebox.showinfo("Editar Proveedor", "No hay proveedores registrados.")
            return
        def editar(proveedor, win_busqueda):
            win_busqueda.destroy()
            win_editar = tk.Toplevel(self.root)
            win_editar.title("Editar Proveedor")
            win_editar.geometry("400x300")
            tk.Label(win_editar, text=f"Editando: {proveedor.nombre}").pack()
            tk.Label(win_editar, text="Nuevo nombre:").pack()
            entry_nombre = tk.Entry(win_editar)
            entry_nombre.insert(0, proveedor.nombre)
            entry_nombre.pack()
            tk.Label(win_editar, text="Nuevo contacto:").pack()
            entry_contacto = tk.Entry(win_editar)
            entry_contacto.insert(0, getattr(proveedor, 'contacto', ''))
            entry_contacto.pack()
            tk.Label(win_editar, text="Nuevo teléfono:").pack()
            entry_telefono = tk.Entry(win_editar)
            entry_telefono.insert(0, getattr(proveedor, 'telefono', ''))
            entry_telefono.pack()
            def guardar():
                nuevo_nombre = entry_nombre.get().strip()
                proveedor.nombre = nuevo_nombre
                nuevo_contacto = entry_contacto.get().strip()
                if hasattr(proveedor, 'contacto'):
                    proveedor.contacto = nuevo_contacto
                nuevo_telefono = entry_telefono.get().strip()
                if hasattr(proveedor, 'telefono'):
                    proveedor.telefono = nuevo_telefono
                messagebox.showinfo("Éxito", "Proveedor editado correctamente.")
                from Persistencia import guardar as guardar_p
                guardar_p(self.proveedores, "proveedores.pkl")
                win_editar.destroy()
            tk.Button(win_editar, text="Guardar cambios", command=guardar).pack(pady=10)
            tk.Button(win_editar, text="Cancelar", command=win_editar.destroy).pack()
        self.seleccionar_elemento_con_busqueda("proveedor", proveedores, "nombre", editar)

    def eliminar_proveedor(self):
        """
        Permite eliminar un proveedor del sistema desde la GUI, solicitando confirmación.
        """
        proveedores = self.proveedores if hasattr(self, "proveedores") else []
        if not proveedores:
            messagebox.showinfo("Eliminar Proveedor", "No hay proveedores registrados.")
            return
        def eliminar(proveedor, win_busqueda):
            win_busqueda.destroy()
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar a '{proveedor.nombre}'?")
            if confirm:
                self.proveedores.remove(proveedor)
                messagebox.showinfo("Éxito", f"Proveedor '{proveedor.nombre}' eliminado.")
                # Persistencia inmediata
                from Persistencia import guardar as guardar_p
                guardar_p(self.proveedores, "proveedores.pkl")
        self.seleccionar_elemento_con_busqueda("proveedor", proveedores, "nombre", eliminar)

    def ver_clientes(self):
        """
        Muestra la lista de clientes en una ventana con búsqueda y detalles.
        """
        if not self.clientes:
            messagebox.showinfo("Clientes", "No hay clientes registrados.")
            return
        win = tk.Toplevel(self.root)
        win.title("Lista de Clientes")
        win.geometry("700x450")
        tk.Label(win, text="Lista de Clientes", font=("Arial", 14, "bold")).pack(pady=5)
        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True)
        # Campo de búsqueda
        tk.Label(frame, text="Buscar cliente:").pack(anchor="w", padx=5)
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(frame, textvariable=var_buscar)
        entry_buscar.pack(fill=tk.X, padx=5)
        columns = ("nombre", "tipo", "grado", "prepago", "deuda")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        tree.heading("nombre", text="Nombre")
        tree.heading("tipo", text="Tipo")
        tree.heading("grado", text="Grado/Lugar")
        tree.heading("prepago", text="Saldo Prepago")
        tree.heading("deuda", text="Deuda")
        tree.column("nombre", width=180)
        tree.column("tipo", width=80)
        tree.column("grado", width=120)
        tree.column("prepago", width=100, anchor="e")
        tree.column("deuda", width=100, anchor="e")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)
        def cargar_clientes():
            tree.delete(*tree.get_children())
            filtro = var_buscar.get().lower()
            for c in self.clientes:
                nombre = getattr(c, "nombre", "")
                tipo = c.__class__.__name__
                grado = getattr(c, "grado", getattr(c, "lugar", ""))
                prepago = f"S/{getattr(c, 'saldo_prepago', 0):.2f}" if hasattr(c, 'saldo_prepago') else "-"
                deuda = f"S/{getattr(c, 'deuda', 0):.2f}" if hasattr(c, 'deuda') and getattr(c, 'deuda', 0) > 0 else "-"
                if filtro in nombre.lower() or filtro in tipo.lower() or filtro in str(grado).lower():
                    tree.insert('', 'end', values=(nombre, tipo, grado, prepago, deuda))
        var_buscar.trace('w', lambda *a: cargar_clientes())
        cargar_clientes()
        # Panel de detalle
        frame_det = tk.Frame(win)
        frame_det.pack(fill=tk.X, padx=10, pady=5)
        label_det = tk.Label(frame_det, text="Seleccione un cliente para ver detalles", justify="left", anchor="w")
        label_det.pack(fill=tk.X)
        def mostrar_detalle(event):
            sel = tree.selection()
            if not sel:
                return
           
            item = tree.item(sel[0])
            nombre = item['values'][0]
            cliente = next((c for c in self.clientes if getattr(c, 'nombre', '') == nombre), None)
            if not cliente:
                return
            tipo = cliente.__class__.__name__
            grado = getattr(cliente, "grado", getattr(cliente, "lugar", ""))
            prepago = f"S/{getattr(cliente, 'saldo_prepago', 0):.2f}" if hasattr(cliente, 'saldo_prepago') else "-"
            deuda = f"S/{getattr(cliente, 'deuda', 0):.2f}" if hasattr(cliente, 'deuda') and getattr(cliente, 'deuda', 0) > 0 else "-"
            detalle = f"Nombre: {nombre}\nTipo: {tipo}\nGrado/Lugar: {grado}\nSaldo prepago: {prepago}\nDeuda: {deuda}"
            label_det.config(text=detalle)
        tree.bind('<<TreeviewSelect>>', mostrar_detalle)
        tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)

    def menu_productos(self):
        """
        Submenú gráfico para gestionar productos: ver, agregar, editar y eliminar.
        """
        self._crear_submenu(
            "MENÚ DE PRODUCTOS",
            [
                ("Ver productos", self.ver_productos),
                ("Agregar producto", self.registrar_producto),
                ("Editar producto", self.editar_producto),
                ("Eliminar producto", self.eliminar_producto),
                ("Volver", self.crear_menu_principal)
            ]
        )