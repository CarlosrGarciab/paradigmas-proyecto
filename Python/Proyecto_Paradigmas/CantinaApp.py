import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, PhotoImage
from Inventario import Inventario
from Caja import Caja
from CuentaBanco import CuentaBanco
from Persistencia import Persistencia
from datetime import datetime

# --- Importaciones de clases propias ---
from PagoEfectivo import PagoEfectivo
from PagoPrepago import PagoPrepago
from PagoTransferencia import PagoTransferencia
from PagoDeuda import PagoDeuda
from Venta import Venta
from Compra import Compra
from Proveedor import Proveedor
from Producto import Producto
from Alumno import Alumno
from Profesor import Profesor

class CantinaApp:
    """
    Clase principal de la aplicación de Cantina. Gestiona la interfaz gráfica y la lógica de negocio para ventas, compras, productos, clientes, proveedores, caja y banco.
    """
    def __init__(self, root):
        """
        Inicializa la aplicación, carga los datos persistentes y configura la ventana principal.
        """
        self.root = root
        self.root.title("Sistema Cantina")
        self.root.configure(bg="#f5f5f5")
        self.root.state("zoomed")
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
            productos = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True)]
            if filtro:
                productos = [p for p in productos if filtro in p.nombre.lower() or filtro in getattr(p, 'categoria', '').lower()]
            for p in productos:
                tree.insert('', 'end', values=(p.nombre, f"S/{p.precio:.2f}", p.stock, getattr(p, 'categoria', ''), getattr(p, 'stock_minimo', '')))
        var_buscar.trace('w', lambda *a: mostrar_productos())
        mostrar_productos()
        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

    def eliminar_elemento(self, lista, tipo, atributo="nombre", callback_post=None):
        """
        Elimina un elemento de una lista (producto, cliente o proveedor) tras confirmación del usuario.
        """
        if not lista:
            messagebox.showinfo(f"Eliminar {tipo.title()}", f"No hay {tipo}s registrados.")
            return

        def eliminar(elem, win_busqueda):
            win_busqueda.destroy()
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar '{getattr(elem, atributo, str(elem))}'?")
            if confirm:
                if tipo == "producto":
                    # Elimina por nombre, no por objeto
                    self.inventario.eliminar_producto(elem.nombre)
                elif tipo == "cliente":
                    self.clientes.remove(elem)
                elif tipo == "proveedor":
                    self.proveedores.remove(elem)
                messagebox.showinfo("Éxito", f"{tipo.title()} eliminado correctamente.")
                if callback_post:
                    callback_post()

        self.seleccionar_elemento_con_busqueda(tipo, lista, atributo, eliminar)
        
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
        Submenú gráfico para ver y modificar el dinero en caja y banco, con mejor estética y orden.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True)
        tk.Label(frame, text="💰 MENÚ CAJA/BANCO", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=18)

        btn_style = {
            "width": 32,
            "height": 2,
            "font": ("Arial", 12),
            "bg": "#27ae60",
            "fg": "white",
            "activebackground": "#229954",
            "activeforeground": "#ecf0f1",
            "bd": 0,
            "relief": "flat"
        }

        # Caja
        tk.Label(frame, text="🟩 Caja", font=("Arial", 13, "bold"), fg="#145a32", bg="#f5f5f5").pack(pady=(10, 2))
        tk.Button(frame, text="Ver dinero en caja", command=self.ver_caja, **btn_style).pack(pady=2)
        tk.Button(frame, text="Modificar dinero en caja", command=self.modificar_caja, **btn_style).pack(pady=2)

        # Separador visual
        tk.Label(frame, text="", bg="#f5f5f5").pack(pady=5)

        # Banco
        tk.Label(frame, text="🟦 Banco", font=("Arial", 13, "bold"), fg="#154360", bg="#f5f5f5").pack(pady=(10, 2))
        tk.Button(frame, text="Ver dinero en banco", command=self.ver_banco, **btn_style).pack(pady=2)
        tk.Button(frame, text="Modificar dinero en banco", command=self.modificar_banco, **btn_style).pack(pady=2)

        # Volver
        tk.Label(frame, text="", bg="#f5f5f5").pack(pady=8)
        tk.Button(frame, text="Volver", command=self.crear_menu_principal, bg="#e74c3c", fg="white",
                font=("Arial", 12, "bold"), activebackground="#922b21", activeforeground="#ecf0f1",
                bd=0, relief="flat", width=32, height=2).pack(pady=2)
            
    def ver_caja(self):
        """
        Muestra el dinero actual en caja con una ventana más estética.
        """
        monto = getattr(self.caja, "dinero", 0.0)
        win = tk.Toplevel(self.root)
        win.title("Dinero en Caja")
        win.geometry("320x160")
        win.configure(bg="#f5f5f5")
        tk.Label(win, text="🟩 Dinero en Caja", font=("Arial", 16, "bold"), fg="#145a32", bg="#f5f5f5").pack(pady=(22, 10))
        tk.Label(win, text=f"S/ {monto:.2f}", font=("Arial", 28, "bold"), fg="#229954", bg="#f5f5f5").pack(pady=(0, 18))
        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack()

    def menu_proveedores(self):
        """
        Submenú gráfico para gestionar proveedores: ver, agregar, editar y eliminar.
        """
        self._crear_submenu(
            "MENÚ DE PROVEEDORES",
            [
                ("Ver proveedores", self.ver_proveedores_detallado),
                ("Agregar proveedor", self.agregar_proveedor),
                ("Editar proveedor", self.editar_proveedor),
                ("Eliminar proveedor", self.eliminar_proveedor),
                ("Volver", self.crear_menu_principal)
            ]
        )
        
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

    def registrar_venta(self):
        """
        Abre una ventana para registrar una venta: selección de productos, cantidades, método de pago y cliente si corresponde.
        """
        productos_disponibles = [p for p in self.inventario.listar_productos() if getattr(p, 'disponible', True) and p.stock > 0]
        if not productos_disponibles:
            messagebox.showinfo("Registrar Venta", "No hay productos con stock disponible para vender.")
            return

        win = tk.Toplevel(self.root)
        win.title("Registrar Venta")
        self.posicionar_ventana_arriba(win, 900, 650)
        win.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')

        frame_prod = ttk.LabelFrame(win, text="Productos a vender", padding=10)
        frame_prod.pack(fill="both", expand=True, padx=10, pady=8)

        canvas = tk.Canvas(frame_prod, height=220)
        scrollbar = ttk.Scrollbar(frame_prod, orient="vertical", command=canvas.yview)
        productos_frame = ttk.Frame(canvas)
        productos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=productos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        cantidad_vars = {}
        seleccionados = {}

        def seleccionar_producto():
            def on_select(producto, win_busqueda):
                win_busqueda.destroy()
                if producto.nombre not in cantidad_vars:
                    cantidad_vars[producto.nombre] = tk.IntVar(value=1)
                    seleccionados[producto.nombre] = producto
                    actualizar_lista_productos()
            self.seleccionar_elemento_con_busqueda("producto", productos_disponibles, "nombre", on_select)

        def actualizar_lista_productos():
            for widget in productos_frame.winfo_children():
                widget.destroy()
            for nombre, var in cantidad_vars.items():
                p = self.inventario.buscar_producto_por_nombre(nombre)
                f = ttk.Frame(productos_frame)
                f.pack(fill="x", pady=2)
                ttk.Label(f, text=f"{p.nombre}", width=18).pack(side="left")
                ttk.Label(f, text=f"Stock: {p.stock}", width=10).pack(side="left")
                ttk.Label(f, text=f"Precio: S/{p.precio:.2f}", width=15).pack(side="left")
                ttk.Label(f, text="Cantidad:").pack(side="left")
                spin = ttk.Spinbox(f, from_=0, to=p.stock, width=5, textvariable=var)
                spin.pack(side="left", padx=5)
                # Subtotal por producto
                label_subtotal = ttk.Label(f, text=f"Subtotal: S/{p.precio * var.get():.2f}", width=18)
                label_subtotal.pack(side="left", padx=5)
                def on_cantidad_change(*args, nombre=nombre, var=var, label=label_subtotal):
                    prod = self.inventario.buscar_producto_por_nombre(nombre)
                    cantidad = var.get()
                    label.config(text=f"Subtotal: S/{prod.precio * cantidad:.2f}")
                    actualizar_total()
                var.trace_add('write', on_cantidad_change)
                def quitar(n=nombre):
                    cantidad_vars.pop(n)
                    seleccionados.pop(n)
                    actualizar_lista_productos()
                ttk.Button(f, text="Quitar", command=quitar).pack(side="left", padx=5)
            actualizar_total()

        ttk.Button(frame_prod, text="Agregar producto", command=seleccionar_producto).pack(pady=4)

        label_total = ttk.Label(win, text="Total: S/0.00", font=("Arial", 13, "bold"))
        label_total.pack(pady=5)

        def actualizar_total(*args):
            total = 0
            for nombre, var in cantidad_vars.items():
                p = self.inventario.buscar_producto_por_nombre(nombre)
                cant = var.get()
                if cant > 0:
                    total += p.precio * cant
            label_total.config(text=f"Total: S/{total:.2f}")

        # --- Método de pago ---
        frame_pago = ttk.LabelFrame(win, text="Método de pago", padding=10)
        frame_pago.pack(fill="x", padx=10, pady=8)
        var_metodo = tk.StringVar()
        metodos = ["Efectivo", "Prepago", "Transferencia", "Deuda"]
        for m in metodos:
            ttk.Radiobutton(frame_pago, text=m, variable=var_metodo, value=m).pack(side="left", padx=10)

        # --- Cliente (solo si es prepago o deuda) ---
        frame_cliente = ttk.LabelFrame(win, text="Cliente (solo para prepago o deuda)", padding=10)
        var_cliente_nombre = tk.StringVar()
        ttk.Label(frame_cliente, text="Cliente:").pack(side="left")
        def seleccionar_cliente():
            alumnos = [c for c in self.clientes if hasattr(c, 'saldo_prepago')] if var_metodo.get() == "Prepago" else self.clientes
            if not alumnos:
                messagebox.showinfo("Clientes", "No hay clientes registrados.")
                return
            def on_select(cliente, win_busq):
                win_busq.destroy()
                var_cliente_nombre.set(cliente.nombre)
            self.seleccionar_elemento_con_busqueda("cliente", alumnos, "nombre", on_select)
        ttk.Button(frame_cliente, text="Seleccionar cliente", command=seleccionar_cliente).pack(side="left")
        ttk.Label(frame_cliente, textvariable=var_cliente_nombre).pack(side="left", padx=5)
        def mostrar_cliente(*args):
            if var_metodo.get() in ("Prepago", "Deuda"):
                frame_cliente.pack(fill="x", padx=10, pady=8)
            else:
                frame_cliente.pack_forget()
        var_metodo.trace('w', mostrar_cliente)

        # --- Botones de acción ---
        frame_btns = ttk.Frame(win)
        frame_btns.pack(pady=15)
        ttk.Button(frame_btns, text="Registrar Venta", command=lambda: guardar(), style="Accent.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btns, text="Cancelar", command=win.destroy).pack(side="left", padx=10)

        def guardar():
            productos_vendidos = {}
            for nombre, var in cantidad_vars.items():
                cant = var.get()
                p = self.inventario.buscar_producto_por_nombre(nombre)
                if cant > 0:
                    if cant > p.stock:
                        messagebox.showerror("Error", f"No hay suficiente stock de {p.nombre}.")
                        return
                    productos_vendidos[nombre] = cant
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
                    monto_entregado = simpledialog.askfloat("Pago en efectivo", f"Total a pagar: S/{total:.2f}\nIngrese el monto entregado por el cliente:")
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
                    nombre_sel = var_cliente_nombre.get()
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
                    nombre_sel = var_cliente_nombre.get()
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
                    if cant > prod.stock:
                        messagebox.showerror("Error", f"No hay suficiente stock de {prod.nombre}.")
                        return
                    prod.stock -= cant
                # Registrar venta
                venta = Venta(productos_vendidos, metodo_pago, self.inventario, self.caja, fecha=fecha)
                venta.calcular_total()
                self.ventas.append(venta)
                Persistencia.guardar(self.ventas, "ventas.pkl")
                Persistencia.guardar(self.inventario, "inventario.pkl")
                Persistencia.guardar(self.caja, "caja.pkl")
                Persistencia.guardar(self.banco, "banco.pkl")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")

        # Inicializa la lista vacía
        actualizar_lista_productos()
    
    def registrar_compra(self):
        """
        Abre una ventana para registrar una compra: seleccionar proveedor, productos, cantidades, precios y método de pago.
        Solo muestra productos asociados al proveedor seleccionado.
        """
        win = tk.Toplevel(self.root)
        win.title("Registrar Compra")
        self.posicionar_ventana_arriba(win, 950, 600)
        win.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')

        # --- Proveedor ---
        frame_prov = ttk.LabelFrame(win, text="Proveedor", padding=10)
        frame_prov.pack(fill="x", padx=10, pady=8)

        var_prov_nombre = tk.StringVar()
        ttk.Label(frame_prov, text="Proveedor:").pack(side="left")
        ttk.Label(frame_prov, textvariable=var_prov_nombre, font=("Arial", 11, "bold")).pack(side="left", padx=8)

        def seleccionar_proveedor():
            if not self.proveedores:
                ("Proveedores", "No hay proveedores registrados.")
                return
            def on_select(prov, win_busq):
                win_busq.destroy()
                var_prov_nombre.set(prov.nombre)
                actualizar_productos()
            self.seleccionar_elemento_con_busqueda("proveedor", self.proveedores, "nombre", on_select)
        ttk.Button(frame_prov, text="Seleccionar proveedor", command=seleccionar_proveedor).pack(side="right")

        # --- Productos asociados ---
        frame_prod = ttk.LabelFrame(win, text="Productos del proveedor", padding=10)
        frame_prod.pack(fill="both", expand=True, padx=10, pady=8)

        # Scroll para productos
        canvas = tk.Canvas(frame_prod, height=220)
        scrollbar = ttk.Scrollbar(frame_prod, orient="vertical", command=canvas.yview)
        productos_frame = ttk.Frame(canvas)
        productos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=productos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        productos_vars = []

        def actualizar_productos():
            for widget in productos_frame.winfo_children():
                widget.destroy()
            productos_vars.clear()
            nombre_prov = var_prov_nombre.get().strip()
            if not nombre_prov:
                return
            proveedor = next((p for p in self.proveedores if p.nombre == nombre_prov), None)
            if not proveedor:
                return
            productos_asociados = set()
            for compra in self.compras:
                if hasattr(compra, 'proveedor') and getattr(compra, 'proveedor', None) and compra.proveedor.nombre == nombre_prov:
                    for nombre_prod in compra.productos_comprados.keys():
                        prod = self.inventario.buscar_producto_por_nombre(nombre_prod)
                        if prod:
                            productos_asociados.add(prod)
            productos_asociados = list(productos_asociados)
            if not productos_asociados:
                ttk.Label(productos_frame, text="Este proveedor no tiene productos registrados en compras previas.").pack()
                return
            for p in productos_asociados:
                f = ttk.Frame(productos_frame)
                f.pack(fill="x", pady=2)
                ttk.Label(f, text=f"{p.nombre}", width=20).pack(side="left")
                ttk.Label(f, text="Cantidad:").pack(side="left")
                var_cant = tk.IntVar(value=0)
                ttk.Spinbox(f, from_=0, to=1000, width=5, textvariable=var_cant).pack(side="left")
                ttk.Label(f, text="Precio compra:").pack(side="left")
                var_precio = tk.DoubleVar(value=p.precio)
                ttk.Entry(f, width=7, textvariable=var_precio).pack(side="left")
                var_disponible = tk.BooleanVar(value=getattr(p, 'disponible', True))
                ttk.Checkbutton(f, text="Disponible", variable=var_disponible).pack(side="left", padx=5)
                productos_vars.append((p, var_cant, var_precio, var_disponible))

        # --- Agregar producto nuevo ---
        frame_nuevo = ttk.LabelFrame(win, text="Agregar producto nuevo (opcional)", padding=10)
        frame_nuevo.pack(fill="x", padx=10, pady=8)
        entry_nuevo_nombre = ttk.Entry(frame_nuevo, width=14)
        entry_nuevo_nombre.pack(side="left", padx=2)
        entry_nuevo_cant = ttk.Entry(frame_nuevo, width=5)
        entry_nuevo_cant.pack(side="left", padx=2)
        entry_nuevo_precio_compra = ttk.Entry(frame_nuevo, width=7)
        entry_nuevo_precio_compra.pack(side="left", padx=2)
        entry_nuevo_precio_venta = ttk.Entry(frame_nuevo, width=7)
        entry_nuevo_precio_venta.pack(side="left", padx=2)
        entry_nuevo_categoria = ttk.Entry(frame_nuevo, width=10)
        entry_nuevo_categoria.pack(side="left", padx=2)
        entry_nuevo_stock_min = ttk.Entry(frame_nuevo, width=6)
        entry_nuevo_stock_min.pack(side="left", padx=2)
        var_nuevo_disponible = tk.BooleanVar(value=True)
        chk_nuevo_disponible = ttk.Checkbutton(frame_nuevo, text="Disponible", variable=var_nuevo_disponible)
        chk_nuevo_disponible.pack(side="left", padx=5)
        ttk.Label(frame_nuevo, text="(nombre, cant, $compra, $venta, cat, min)").pack(side="left", padx=5)

        # --- Ocultar campos de venta si no es disponible ---
        def actualizar_campos_nuevo_producto(*args):
            if var_nuevo_disponible.get():
                entry_nuevo_precio_venta.config(state="normal")
                entry_nuevo_stock_min.config(state="normal")
            else:
                entry_nuevo_precio_venta.delete(0, tk.END)
                entry_nuevo_stock_min.delete(0, tk.END)
                entry_nuevo_precio_venta.config(state="disabled")
                entry_nuevo_stock_min.config(state="disabled")
        var_nuevo_disponible.trace('w', lambda *a: actualizar_campos_nuevo_producto())
        actualizar_campos_nuevo_producto()

        # --- Método de pago ---
        frame_pago = ttk.LabelFrame(win, text="Método de pago", padding=10)
        frame_pago.pack(fill="x", padx=10, pady=8)
        var_metodo = tk.StringVar()
        ttk.Radiobutton(frame_pago, text="Caja", variable=var_metodo, value="Caja").pack(side="left", padx=10)
        ttk.Radiobutton(frame_pago, text="Banco", variable=var_metodo, value="Banco").pack(side="left", padx=10)

        # --- Botones de acción ---
        frame_btns = ttk.Frame(win)
        frame_btns.pack(pady=15)
        ttk.Button(frame_btns, text="Registrar Compra", command=lambda: guardar(), style="Accent.TButton").pack(side="left", padx=10)
        ttk.Button(frame_btns, text="Cancelar", command=win.destroy).pack(side="left", padx=10)

        def guardar():
            try:
                nombre_prov = var_prov_nombre.get().strip()
                if not nombre_prov:
                    messagebox.showerror("Error", "Debe seleccionar un proveedor.")
                    return
                proveedor = next((p for p in self.proveedores if p.nombre == nombre_prov), None)
                if not proveedor:
                    proveedor = Proveedor(nombre_prov, contacto="", telefono="")
                    self.proveedores.append(proveedor)

                productos_comprados = {}
                for p, var_cant, var_precio, var_disponible in productos_vars:
                    cant = var_cant.get()
                    precio = var_precio.get()
                    disponible = var_disponible.get() if hasattr(var_disponible, 'get') else True
                    if cant > 0:
                        if disponible:
                            # Solo si es vendible, agrega al inventario
                            producto_sumar = Producto(p.nombre, precio, cant, getattr(p, 'categoria', None), getattr(p, 'stock_minimo', 1))
                            producto_sumar.disponible = True
                            self.inventario.agregar_producto(producto_sumar)
                        # Siempre registra la compra para control de gastos
                        productos_comprados[p.nombre] = (cant, precio, disponible)

                nombre_nuevo = entry_nuevo_nombre.get().strip()
                cant_nuevo = entry_nuevo_cant.get().strip()
                precio_compra_nuevo = entry_nuevo_precio_compra.get().strip()
                precio_venta_nuevo = entry_nuevo_precio_venta.get().strip()
                categoria_nuevo = entry_nuevo_categoria.get().strip()
                stock_min_nuevo = entry_nuevo_stock_min.get().strip()
                disponible_nuevo = var_nuevo_disponible.get() if hasattr(var_nuevo_disponible, 'get') else True
                if nombre_nuevo and cant_nuevo and precio_compra_nuevo and categoria_nuevo:
                    try:
                        cant_nuevo = int(cant_nuevo)
                        precio_compra_nuevo = float(precio_compra_nuevo)
                        if cant_nuevo <= 0:
                            messagebox.showerror("Error", f"La cantidad para '{nombre_nuevo}' debe ser mayor a 0.")
                            return
                        if precio_compra_nuevo < 0:
                            messagebox.showerror("Error", f"El precio de compra no puede ser negativo.")
                            return
                        if disponible_nuevo:
                            # Solo pide y valida precio de venta y stock mínimo si es vendible
                            if not precio_venta_nuevo or not stock_min_nuevo:
                                messagebox.showerror("Error", "Debe ingresar precio de venta y stock mínimo para productos disponibles.")
                                return
                            precio_venta_nuevo = float(precio_venta_nuevo)
                            stock_min_nuevo = int(stock_min_nuevo)
                            if precio_venta_nuevo < 0:
                                messagebox.showerror("Error", f"El precio de venta no puede ser negativo.")
                                return
                            if stock_min_nuevo < 0:
                                messagebox.showerror("Error", f"El stock mínimo no puede ser negativo.")
                                return
                            nuevo = Producto(nombre_nuevo, precio_venta_nuevo, cant_nuevo, categoria_nuevo, stock_min_nuevo)
                            nuevo.disponible = True
                            self.inventario.agregar_producto(nuevo)
                            productos_comprados[nombre_nuevo] = (cant_nuevo, precio_compra_nuevo, True)
                        else:
                            # No agregues al inventario, solo registra la compra
                            productos_comprados[nombre_nuevo] = (cant_nuevo, precio_compra_nuevo, False)
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
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                compra = Compra(proveedor, fecha, productos_comprados)
                self.compras.append(compra)
                total = sum(cant * precio for (cant, precio, _) in productos_comprados.values())
                if metodo == "Caja":
                    self.caja.dinero -= total
                else:
                    self.banco.saldo -= total
                Persistencia.guardar(self.compras, "compras.pkl")
                Persistencia.guardar(self.inventario, "inventario.pkl")
                Persistencia.guardar(self.caja, "caja.pkl")
                Persistencia.guardar(self.banco, "banco.pkl")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado al registrar la compra: {e}")
            
    def ver_productos(self):
        """
        Muestra el inventario de productos en una ventana desplazable, resaltando en rojo los productos con stock 0
        y en amarillo los que están en su stock mínimo.
        """
        win = tk.Toplevel(self.root)
        win.title("Inventario de Productos")
        win.geometry("700x520")
        win.configure(bg="#f5f5f5")

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="Inventario de Productos", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(0, 10))

        buscador_frame = tk.Frame(frame, bg="#f5f5f5")
        buscador_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(buscador_frame, text="🔍 Buscar:", font=("Arial", 12), bg="#f5f5f5").pack(side="left", padx=(0, 5))
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(buscador_frame, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(side="left", fill=tk.X, expand=True)
        entry_buscar.focus_set()

        columns = ("nombre", "precio", "stock", "categoria", "stock_minimo")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=16)
        tree.heading("nombre", text="Nombre")
        tree.heading("precio", text="Precio")
        tree.heading("stock", text="Stock")
        tree.heading("categoria", text="Categoría")
        tree.heading("stock_minimo", text="Stock Mínimo")
        tree.column("nombre", width=180)
        tree.column("precio", width=90, anchor="e")
        tree.column("stock", width=70, anchor="e")
        tree.column("categoria", width=140)
        tree.column("stock_minimo", width=110, anchor="e")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#3498db", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#f5f5f5", fieldbackground="#f5f5f5")
        style.map("Treeview", background=[("selected", "#d0e6fa")])

        # --- TAG para stock 0 y stock mínimo ---
        tree.tag_configure('stock_cero', background='#ffcccc')      # rojo claro
        tree.tag_configure('stock_minimo', background='#fff7b2')    # amarillo claro

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True, padx=(0, 0), pady=5)
        scrollbar.pack(side="right", fill=tk.Y)

        def mostrar_productos():
            tree.delete(*tree.get_children())
            filtro = var_buscar.get().lower()
            productos = self.inventario.listar_productos()
            if filtro:
                productos = [p for p in productos if filtro in p.nombre.lower() or filtro in getattr(p, 'categoria', '').lower()]
            for p in productos:
                valores = (
                    p.nombre,
                    f"S/{p.precio:.2f}",
                    p.stock,
                    getattr(p, 'categoria', ''),
                    getattr(p, 'stock_minimo', '')
                )
                # Aplica el tag correspondiente
                if p.stock == 0:
                    tag = 'stock_cero'
                elif hasattr(p, 'stock_minimo') and p.stock == getattr(p, 'stock_minimo', 1) and p.stock > 0:
                    tag = 'stock_minimo'
                else:
                    tag = ''
                tree.insert('', 'end', values=valores, tags=(tag,))
            if not productos:
                tree.insert('', 'end', values=("No hay productos que coincidan", "", "", "", ""))

        var_buscar.trace('w', lambda *a: mostrar_productos())
        mostrar_productos()

        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat").pack(pady=12)
            
    def registrar_producto(self):
        """
        Abre un formulario para agregar un producto hecho por la cantina (sin precio de compra).
        Solo permite autocompletar productos agregados manualmente (no por compra a proveedor).
        """
        import tkinter as tk
        from tkinter import ttk, messagebox

        win = tk.Toplevel(self.root)
        win.title("Agregar Producto de Cantina")
        win.geometry("420x370")
        win.resizable(False, False)
        win.configure(bg="#f5f5f5")

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame, text="Agregar Producto de Cantina", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(0, 15))

        # Solo productos agregados manualmente (marcados con manual=True)
        productos_disponibles = [p for p in self.inventario.listar_productos() if getattr(p, 'manual', False) and getattr(p, 'disponible', True)]
        nombres_productos = [p.nombre for p in productos_disponibles]

        campos = [
            ("Nombre", "nombre"),
            ("Precio de venta", "precio_venta"),
            ("Stock", "stock"),
            ("Categoría", "categoria"),
            ("Stock mínimo", "stock_minimo"),
            ("Disponible", "disponible")
        ]
        entradas = {}

        # --- Nombre con autocompletado ---
        fr_nombre = tk.Frame(frame, bg="#f5f5f5")
        fr_nombre.pack(fill=tk.X, pady=5)
        tk.Label(fr_nombre, text="Nombre:", font=("Arial", 11), width=15, anchor="w", bg="#f5f5f5").pack(side="left")
        var_nombre = tk.StringVar()
        entry_nombre = ttk.Combobox(fr_nombre, textvariable=var_nombre, values=nombres_productos, font=("Arial", 11))
        entry_nombre.pack(side="left", fill=tk.X, expand=True)
        entradas["nombre"] = entry_nombre

        # --- Resto de campos ---
        for label, key in campos[1:]:
            fr = tk.Frame(frame, bg="#f5f5f5")
            fr.pack(fill=tk.X, pady=5)
            tk.Label(fr, text=label + ":", font=("Arial", 11), width=15, anchor="w", bg="#f5f5f5").pack(side="left")
            if key == "disponible":
                entradas[key] = tk.BooleanVar(value=True)
                ttk.Checkbutton(fr, variable=entradas[key], text="Sí").pack(side="left")
            else:
                ent = ttk.Entry(fr, font=("Arial", 11))
                ent.pack(side="left", fill=tk.X, expand=True)
                entradas[key] = ent

        # --- Autocompletar campos si el nombre existe ---
        def autocompletar_campos(*args):
            nombre = var_nombre.get().strip()
            producto = next((p for p in productos_disponibles if p.nombre.lower() == nombre.lower()), None)
            if producto:
                entradas["precio_venta"].delete(0, tk.END)
                entradas["precio_venta"].insert(0, f"{getattr(producto, 'precio', 0):.2f}")
                entradas["stock"].delete(0, tk.END)
                entradas["stock"].insert(0, "0")
                entradas["categoria"].delete(0, tk.END)
                entradas["categoria"].insert(0, getattr(producto, 'categoria', ''))
                entradas["stock_minimo"].delete(0, tk.END)
                entradas["stock_minimo"].insert(0, getattr(producto, 'stock_minimo', 1))
                entradas["disponible"].set(getattr(producto, 'disponible', True))
            else:
                # Limpiar campos excepto nombre
                for key in ["precio_venta", "stock", "categoria", "stock_minimo"]:
                    entradas[key].delete(0, tk.END)
                entradas["disponible"].set(True)

        var_nombre.trace('w', autocompletar_campos)

        def guardar():
            nombre = entradas["nombre"].get().strip()
            precio_venta = entradas["precio_venta"].get().strip()
            stock = entradas["stock"].get().strip()
            categoria = entradas["categoria"].get().strip()
            stock_minimo = entradas["stock_minimo"].get().strip()
            disponible = entradas["disponible"].get()

            # Validaciones
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.", parent=win)
                return
            # --- Validación de duplicados por nombre ---
            if any(p.nombre.lower() == nombre.lower() for p in self.inventario.listar_productos()):
                messagebox.showerror("Error", f"Ya existe un producto con el nombre '{nombre}'.", parent=win)
                return
            try:
                precio_venta = float(precio_venta)
                stock = int(stock)
                stock_minimo = int(stock_minimo)
            except Exception:
                messagebox.showerror("Error", "Precio y stock deben ser números válidos.", parent=win)
                return
            if precio_venta < 0 or stock < 0 or stock_minimo < 0:
                messagebox.showerror("Error", "Ningún valor puede ser negativo.", parent=win)
                return

            from Producto import Producto
            nuevo = Producto(nombre, precio_venta, stock, categoria, stock_minimo)
            nuevo.disponible = disponible
            nuevo.manual = True  # Marca como producto hecho por la cantina
            self.inventario.agregar_producto(nuevo)
            Persistencia.guardar(self.inventario, "inventario.pkl")
            win.destroy()

        btn_frame = tk.Frame(frame, bg="#f5f5f5")
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Guardar", command=guardar, style="Accent.TButton").pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side="left", padx=10)

    def seleccionar_elemento_con_busqueda(self, titulo, lista, atributo="nombre", callback=None):
        """
        Abre una ventana para buscar y seleccionar un elemento de una lista, usando un campo de búsqueda.
        """
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.geometry("400x320")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text=f"Buscar {titulo.lower()}:", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(anchor="w", padx=12, pady=(12, 2))
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(win, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(fill=tk.X, padx=12, pady=4)
        entry_buscar.focus_set()

        frame_lista = tk.Frame(win, bg="#f5f5f5")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = tk.Listbox(
            frame_lista,
            yscrollcommand=scrollbar.set,
            font=("Arial", 11),
            bg="#f5f5f5",
            relief="flat",
            selectbackground="#d0e6fa",
            activestyle="none"
        )
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

        def seleccionar(event=None):
            sel = listbox.curselection()
            if not sel:
                messagebox.showerror("Error", f"Debe seleccionar un {titulo.lower()}.", parent=win)
                return
            valor = listbox.get(sel[0])
            for elem in lista:
                if getattr(elem, atributo, str(elem)) == valor:
                    if callback:
                        callback(elem, win)
                    else:
                        win.destroy()
                    return

        # Permite seleccionar con doble clic o Enter
        listbox.bind('<Double-1>', seleccionar)
        listbox.bind('<Return>', seleccionar)

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Seleccionar", command=seleccionar, bg="#27ae60", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12).pack(side="left", padx=8)

        return win
 
    def ver_ventas(self):
        """
        Muestra el historial de ventas en una ventana con tabla, búsqueda y detalle moderno.
        """
        if not hasattr(self, 'ventas') or not self.ventas:
            messagebox.showinfo("Ventas", "No hay ventas registradas.")
            return
        win = tk.Toplevel(self.root)
        win.title("Historial de Ventas")
        win.geometry("900x520")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="📈 Historial de Ventas", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=8)

        # Buscador
        buscador_frame = tk.Frame(win, bg="#f5f5f5")
        buscador_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(buscador_frame, text="🔍 Buscar:", font=("Arial", 12), bg="#f5f5f5").pack(side="left", padx=(0, 5))
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(buscador_frame, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(side="left", fill=tk.X, expand=True)
        entry_buscar.focus_set()

        columns = ("fecha", "cliente", "metodo", "total")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=14)
        tree.heading("fecha", text="Fecha/Hora")
        tree.heading("cliente", text="Cliente")
        tree.heading("metodo", text="Método de Pago")
        tree.heading("total", text="Total (S/)")
        tree.column("fecha", width=170)
        tree.column("cliente", width=220)
        tree.column("metodo", width=140)
        tree.column("total", width=120, anchor="e")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#27ae60", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#f5f5f5", fieldbackground="#f5f5f5")
        style.map("Treeview", background=[("selected", "#d0e6fa")])
        scrollbar = tk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True, padx=(0, 0), pady=5)
        scrollbar.pack(side="right", fill=tk.Y)

        # Llenar la tabla con filtro
        def mostrar_ventas():
            tree.delete(*tree.get_children())
            filtro = var_buscar.get().lower()
            for idx, v in enumerate(self.ventas):
                fecha = getattr(v, 'fecha', '')
                cliente = getattr(v, 'cliente', None)
                cliente_nombre = cliente.nombre if cliente and hasattr(cliente, 'nombre') else (str(cliente) if cliente else '')
                metodo_pago = getattr(v, 'metodo_pago', None)
                metodo = metodo_pago.__class__.__name__ if metodo_pago else ''
                total = getattr(v, 'total', None)
                if total is None and hasattr(v, 'calcular_total'):
                    total = v.calcular_total()
                if (filtro in fecha.lower() or filtro in cliente_nombre.lower() or filtro in metodo.lower() or filtro in f"{total:.2f}"):
                    tree.insert('', 'end', iid=idx, values=(fecha, cliente_nombre, metodo, f"{total:.2f}" if total is not None else ""))
            if not tree.get_children():
                tree.insert('', 'end', values=("No hay ventas que coincidan", "", "", ""))

        var_buscar.trace('w', lambda *a: mostrar_ventas())
        mostrar_ventas()

        # Panel de detalle
        frame_det = tk.Frame(win, bg="#f5f5f5")
        frame_det.pack(fill=tk.X, padx=10, pady=5)
        label_det = tk.Label(frame_det, text="Seleccione una venta para ver detalles", justify="left", anchor="w", bg="#f5f5f5")
        label_det.pack(fill=tk.X)

        def mostrar_detalle(event):
            sel = tree.selection()
            if not sel:
                return
            idx = int(sel[0])
            v = self.ventas[idx]
            fecha = getattr(v, 'fecha', '')
            cliente = getattr(v, 'cliente', None)
            cliente_nombre = cliente.nombre if cliente and hasattr(cliente, 'nombre') else (str(cliente) if cliente else '')
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

        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat").pack(pady=10)

    def ver_compras(self):
        """
        Muestra el historial de compras en una ventana con tabla, búsqueda y detalle moderno.
        """
        if not hasattr(self, 'compras') or not self.compras:
            messagebox.showinfo("Compras", "No hay compras registradas.")
            return
        win = tk.Toplevel(self.root)
        win.title("Historial de Compras")
        win.geometry("900x520")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="📉 Historial de Compras", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=8)

        # Buscador
        buscador_frame = tk.Frame(win, bg="#f5f5f5")
        buscador_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(buscador_frame, text="🔍 Buscar:", font=("Arial", 12), bg="#f5f5f5").pack(side="left", padx=(0, 5))
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(buscador_frame, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(side="left", fill=tk.X, expand=True)
        entry_buscar.focus_set()

        columns = ("fecha", "proveedor", "total")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=14)
        tree.heading("fecha", text="Fecha/Hora")
        tree.heading("proveedor", text="Proveedor")
        tree.heading("total", text="Total (S/)")
        tree.column("fecha", width=170)
        tree.column("proveedor", width=220)
        tree.column("total", width=120, anchor="e")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#8e44ad", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#f5f5f5", fieldbackground="#f5f5f5")
        style.map("Treeview", background=[("selected", "#d0e6fa")])
        scrollbar = tk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True, padx=(0, 0), pady=5)
        scrollbar.pack(side="right", fill=tk.Y)

        # Llenar la tabla con filtro
        def mostrar_compras():
            tree.delete(*tree.get_children())
            filtro = var_buscar.get().lower()
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
                if (filtro in fecha.lower() or filtro in proveedor.lower() or filtro in f"{total:.2f}"):
                    tree.insert('', 'end', iid=idx, values=(fecha, proveedor, f"{total:.2f}"))
            if not tree.get_children():
                tree.insert('', 'end', values=("No hay compras que coincidan", "", ""))

        var_buscar.trace('w', lambda *a: mostrar_compras())
        mostrar_compras()

        # Panel de detalle
        frame_det = tk.Frame(win, bg="#f5f5f5")
        frame_det.pack(fill=tk.X, padx=10, pady=5)
        label_det = tk.Label(frame_det, text="Seleccione una compra para ver detalles", justify="left", anchor="w", bg="#f5f5f5")
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

        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat").pack(pady=10)

    def salir(self):
        """
        Guarda los datos antes de salir y muestra una alerta si hay productos con bajo stock.
        """
        self.alerta_bajo_stock()  # Muestra la alerta antes de cerrar
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
        Abre un formulario moderno para registrar un nuevo cliente (alumno o profesor) con validación y mejor estética.
        """
        win = tk.Toplevel(self.root)
        win.title("Registrar Cliente")
        win.geometry("420x420")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="👤 Registrar Cliente", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(18, 10))

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        tk.Label(frame, text="Tipo de cliente *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        var_tipo = tk.StringVar(value="Alumno")
        tipo_frame = tk.Frame(frame, bg="#f5f5f5")
        tipo_frame.pack(anchor="w", pady=(0, 8))
        tk.Radiobutton(tipo_frame, text="Alumno", variable=var_tipo, value="Alumno", bg="#f5f5f5").pack(side="left")
        tk.Radiobutton(tipo_frame, text="Profesor", variable=var_tipo, value="Profesor", bg="#f5f5f5").pack(side="left")

        tk.Label(frame, text="Nombre *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_nombre = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_nombre.pack(fill=tk.X, pady=(0, 8))

        tk.Label(frame, text="Grado/Lugar *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_grado = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_grado.pack(fill=tk.X, pady=(0, 8))

        # Para alumno: saldo prepago y método
        frame_alumno = tk.Frame(frame, bg="#f5f5f5")
        tk.Label(frame_alumno, text="Saldo inicial prepago *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_saldo = tk.Entry(frame_alumno, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_saldo.pack(fill=tk.X, pady=(0, 8))
        tk.Label(frame_alumno, text="¿Dónde se deposita el saldo prepago? *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        var_metodo = tk.StringVar()
        metodo_frame = tk.Frame(frame_alumno, bg="#f5f5f5")
        metodo_frame.pack(anchor="w", pady=(0, 8))
        tk.Radiobutton(metodo_frame, text="Caja", variable=var_metodo, value="Caja", bg="#f5f5f5").pack(side="left")
        tk.Radiobutton(metodo_frame, text="Banco", variable=var_metodo, value="Banco", bg="#f5f5f5").pack(side="left")

        def actualizar_campos(*args):
            if var_tipo.get() == "Alumno":
                frame_alumno.pack(fill=tk.X, pady=(0, 8))
            else:
                frame_alumno.pack_forget()
        var_tipo.trace('w', actualizar_campos)
        actualizar_campos()

        def guardar():
            tipo = var_tipo.get()
            nombre = entry_nombre.get().strip()
            grado = entry_grado.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.", parent=win)
                return
            if any(c.nombre == nombre for c in self.clientes):
                messagebox.showerror("Error", f"El cliente '{nombre}' ya existe.", parent=win)
                return
            if not grado:
                messagebox.showerror("Error", "El grado/lugar no puede estar vacío.", parent=win)
                return
            if tipo == "Alumno":
                try:
                    saldo_prepago = float(entry_saldo.get())
                    if saldo_prepago < 0:
                        raise ValueError
                except Exception:
                    messagebox.showerror("Error", "Saldo prepago inválido.", parent=win)
                    return
                metodo = var_metodo.get()
                if metodo not in ("Caja", "Banco"):
                    messagebox.showerror("Error", "Seleccione dónde se deposita el saldo prepago.", parent=win)
                    return
                caja = self.caja if metodo == "Caja" else None
                banco = self.banco if metodo == "Banco" else None
                from Alumno import Alumno
                alumno = Alumno(nombre, grado, saldo_prepago, metodo.lower(), caja, banco)
                self.clientes.append(alumno)
            elif tipo == "Profesor":
                from Profesor import Profesor
                profesor = Profesor(nombre, grado)
                self.clientes.append(profesor)
            else:
                messagebox.showerror("Error", "Seleccione el tipo de cliente.", parent=win)
                return
            Persistencia.guardar(self.clientes, "clientes.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Registrar", command=guardar, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)

    def recargar_prepago_cliente(self):
        """
        Permite recargar la cuenta prepaga de un alumno desde la GUI, con búsqueda moderna y validación.
        """
        alumnos = [c for c in self.clientes if hasattr(c, 'saldo_prepago')]
        if not alumnos:
            messagebox.showinfo("Recargar Cuenta Prepaga", "No hay alumnos con cuenta prepaga registrados.")
            return

        win = tk.Toplevel(self.root)
        win.title("Recargar Cuenta Prepaga")
        win.geometry("520x420")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="💳 Recargar Cuenta Prepaga", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(18, 10))

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        tk.Label(frame, text="Buscar alumno:", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w")
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(frame, textvariable=var_buscar, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(fill=tk.X, pady=(0, 8))
        listbox = tk.Listbox(frame, font=("Arial", 12), height=5, bg="#f5f5f5", relief="flat", selectbackground="#d0e6fa")
        listbox.pack(fill=tk.X, pady=(0, 8))

        def actualizar_lista(*args):
            filtro = var_buscar.get().lower()
            listbox.delete(0, tk.END)
            for a in alumnos:
                if filtro in a.nombre.lower():
                    listbox.insert(tk.END, a.nombre)
        var_buscar.trace('w', actualizar_lista)
        actualizar_lista()

        tk.Label(frame, text="Monto a recargar *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w")
        entry_monto = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_monto.pack(fill=tk.X, pady=(0, 8))

        tk.Label(frame, text="¿Dónde se deposita la recarga? *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w")
        var_metodo = tk.StringVar()
        metodo_frame = tk.Frame(frame, bg="#f5f5f5")
        metodo_frame.pack(anchor="w", pady=(0, 8))
        tk.Radiobutton(metodo_frame, text="Caja", variable=var_metodo, value="Caja", bg="#f5f5f5").pack(side="left")
        tk.Radiobutton(metodo_frame, text="Banco", variable=var_metodo, value="Banco", bg="#f5f5f5").pack(side="left")

        def guardar():
            sel = listbox.curselection()
            if not sel:
                messagebox.showerror("Error", "Seleccione un alumno.", parent=win)
                return
            nombre_sel = listbox.get(sel[0])
            alumno = next((a for a in alumnos if a.nombre == nombre_sel), None)
            if not alumno:
                messagebox.showerror("Error", "Alumno no encontrado.", parent=win)
                return
            try:
                monto = float(entry_monto.get())
                if monto <= 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Monto inválido.", parent=win)
                return
            metodo = var_metodo.get()
            if metodo == "Caja":
                if self.caja.dinero < monto:
                    messagebox.showerror("Error", "No hay suficiente dinero en CAJA.", parent=win)
                    return
                self.caja.dinero -= monto
                alumno.saldo_prepago += monto
            elif metodo == "Banco":
                if self.banco.saldo < monto:
                    messagebox.showerror("Error", "No hay suficiente dinero en BANCO.", parent=win)
                    return
                self.banco.saldo -= monto
                alumno.saldo_prepago += monto
            else:
                messagebox.showerror("Error", "Seleccione el origen de la recarga.", parent=win)
                return
            Persistencia.guardar(self.clientes, "clientes.pkl")
            Persistencia.guardar(self.caja, "caja.pkl")
            Persistencia.guardar(self.banco, "banco.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Recargar", command=guardar, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)

    def pagar_deuda_cliente(self):
        """
        Permite pagar la deuda de un cliente desde la GUI, con búsqueda moderna y validación.
        """
        clientes_con_deuda = [c for c in self.clientes if getattr(c, "deuda", 0) > 0]
        if not clientes_con_deuda:
            messagebox.showinfo("Pagar Deuda", "No hay clientes con deuda.")
            return

        win = tk.Toplevel(self.root)
        win.title("Pagar Deuda de Cliente")
        win.geometry("520x420")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="💸 Pagar Deuda de Cliente", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(18, 10))

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        tk.Label(frame, text="Buscar cliente:", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w")
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(frame, textvariable=var_buscar, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(fill=tk.X, pady=(0, 8))
        listbox = tk.Listbox(frame, font=("Arial", 12), height=5, bg="#f5f5f5", relief="flat", selectbackground="#d0e6fa")
        listbox.pack(fill=tk.X, pady=(0, 8))

        def actualizar_lista(*args):
            filtro = var_buscar.get().lower()
            listbox.delete(0, tk.END)
            for c in clientes_con_deuda:
                if filtro in c.nombre.lower():
                    listbox.insert(tk.END, c.nombre)
        var_buscar.trace('w', actualizar_lista)
        actualizar_lista()

        label_deuda = tk.Label(frame, text="Deuda actual: -", font=("Arial", 12), bg="#f5f5f5", fg="#c0392b")
        label_deuda.pack(anchor="w", pady=(0, 4))

        def mostrar_deuda(event=None):
            sel = listbox.curselection()
            if not sel:
                label_deuda.config(text="Deuda actual: -")
                return
            nombre_sel = listbox.get(sel[0])
            cliente = next((c for c in clientes_con_deuda if c.nombre == nombre_sel), None)
            if cliente:
                label_deuda.config(text=f"Deuda actual: S/{getattr(cliente, 'deuda', 0):.2f}")
        listbox.bind('<<ListboxSelect>>', mostrar_deuda)

        tk.Label(frame, text="Monto a pagar *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w")
        entry_monto = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_monto.pack(fill=tk.X, pady=(0, 8))

        tk.Label(frame, text="¿Dónde se recibe el pago? *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w")
        var_metodo = tk.StringVar()
        metodo_frame = tk.Frame(frame, bg="#f5f5f5")
        metodo_frame.pack(anchor="w", pady=(0, 8))
        tk.Radiobutton(metodo_frame, text="Caja", variable=var_metodo, value="Caja", bg="#f5f5f5").pack(side="left")
        tk.Radiobutton(metodo_frame, text="Banco", variable=var_metodo, value="Banco", bg="#f5f5f5").pack(side="left")

        def guardar():
            sel = listbox.curselection()
            if not sel:
                messagebox.showerror("Error", "Seleccione un cliente.", parent=win)
                return
            nombre_sel = listbox.get(sel[0])
            cliente = next((c for c in clientes_con_deuda if c.nombre == nombre_sel), None)
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado.", parent=win)
                return
            try:
                monto = float(entry_monto.get())
                if monto <= 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Monto inválido.", parent=win)
                return
            if monto > cliente.deuda:
                messagebox.showerror("Error", f"El monto no puede ser mayor a la deuda actual (S/{cliente.deuda:.2f}).", parent=win)
                return
            metodo = var_metodo.get()
            if metodo == "Caja":
                self.caja.dinero += monto
                cliente.deuda -= monto
                messagebox.showinfo("Éxito", f"Pago recibido en CAJA. Deuda restante: S/{cliente.deuda:.2f}", parent=win)
            elif metodo == "Banco":
                self.banco.saldo += monto
                cliente.deuda -= monto
                messagebox.showinfo("Éxito", f"Pago recibido en BANCO. Deuda restante: S/{cliente.deuda:.2f}", parent=win)
            else:
                messagebox.showerror("Error", "Seleccione el origen del pago.", parent=win)
                return
            Persistencia.guardar(self.clientes, "clientes.pkl")
            Persistencia.guardar(self.caja, "caja.pkl")
            Persistencia.guardar(self.banco, "banco.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Pagar", command=guardar, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        
    def modificar_caja(self):
        """
        Permite modificar el dinero en caja mediante un formulario moderno y validado.
        """
        win = tk.Toplevel(self.root)
        win.title("Modificar dinero en caja")
        win.geometry("340x200")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="🟩 Modificar dinero en CAJA", font=("Arial", 15, "bold"), fg="#145a32", bg="#f5f5f5").pack(pady=(18, 8))
        tk.Label(win, text=f"Dinero actual: S/{self.caja.dinero:.2f}", font=("Arial", 12), bg="#f5f5f5").pack(pady=(0, 8))
        tk.Label(win, text="Nuevo monto:", font=("Arial", 11), bg="#f5f5f5").pack()
        entry_monto = tk.Entry(win, font=("Arial", 12), justify="center")
        entry_monto.pack(pady=(0, 10))
        entry_monto.focus_set()

        def guardar():
            try:
                nuevo_monto = float(entry_monto.get())
                if nuevo_monto < 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Ingrese un monto válido (mayor o igual a 0).", parent=win)
                return
            self.caja.dinero = nuevo_monto
            Persistencia.guardar(self.caja, "caja.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Guardar", command=guardar, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)

    def ver_banco(self):
        """
        Muestra el saldo actual en banco con una ventana más estética.
        """
        saldo = self.banco.saldo if hasattr(self.banco, "saldo") else 0.0
        win = tk.Toplevel(self.root)
        win.title("Dinero en Banco")
        win.geometry("320x160")
        win.configure(bg="#f5f5f5")
        tk.Label(win, text="🟦 Dinero en Banco", font=("Arial", 16, "bold"), fg="#154360", bg="#f5f5f5").pack(pady=(22, 10))
        tk.Label(win, text=f"S/ {saldo:.2f}", font=("Arial", 28, "bold"), fg="#2980b9", bg="#f5f5f5").pack(pady=(0, 18))
        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack()

    def modificar_banco(self):
        """
        Permite modificar el saldo en banco mediante un formulario moderno y validado.
        """
        win = tk.Toplevel(self.root)
        win.title("Modificar dinero en banco")
        win.geometry("340x200")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="🟦 Modificar dinero en BANCO", font=("Arial", 15, "bold"), fg="#154360", bg="#f5f5f5").pack(pady=(18, 8))
        tk.Label(win, text=f"Dinero actual: S/{self.banco.saldo:.2f}", font=("Arial", 12), bg="#f5f5f5").pack(pady=(0, 8))
        tk.Label(win, text="Nuevo monto:", font=("Arial", 11), bg="#f5f5f5").pack()
        entry_monto = tk.Entry(win, font=("Arial", 12), justify="center")
        entry_monto.pack(pady=(0, 10))
        entry_monto.focus_set()

        def guardar():
            try:
                nuevo_monto = float(entry_monto.get())
                if nuevo_monto < 0:
                    raise ValueError
            except Exception:
                messagebox.showerror("Error", "Ingrese un monto válido (mayor o igual a 0).", parent=win)
                return
            self.banco.saldo = nuevo_monto
            Persistencia.guardar(self.banco, "banco.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Guardar", command=guardar, bg="#2980b9", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        
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


    def ver_proveedores_detallado(self):
        """
        Muestra la lista de proveedores con detalles (nombre, contacto, teléfono) en una tabla moderna y con búsqueda.
        """
        win = tk.Toplevel(self.root)
        win.title("Proveedores Registrados")
        win.geometry("600x420")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="🚚 Proveedores Registrados", font=("Arial", 15, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=8)
        buscador_frame = tk.Frame(win, bg="#f5f5f5")
        buscador_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(buscador_frame, text="🔍 Buscar:", font=("Arial", 12), bg="#f5f5f5").pack(side="left", padx=(0, 5))
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(buscador_frame, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(side="left", fill=tk.X, expand=True)
        entry_buscar.focus_set()

        columns = ("nombre", "contacto", "telefono")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=14)
        tree.heading("nombre", text="Nombre")
        tree.heading("contacto", text="Contacto")
        tree.heading("telefono", text="Teléfono")
        tree.column("nombre", width=200)
        tree.column("contacto", width=200)
        tree.column("telefono", width=120)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#2980b9", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#f5f5f5", fieldbackground="#f5f5f5")
        style.map("Treeview", background=[("selected", "#d0e6fa")])

        scrollbar = tk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill=tk.BOTH, expand=True, padx=(0, 0), pady=5)
        scrollbar.pack(side="right", fill=tk.Y)

        proveedores = self.proveedores if hasattr(self, "proveedores") else []

        def mostrar_proveedores():
            tree.delete(*tree.get_children())
            filtro = var_buscar.get().lower()
            encontrados = False
            for p in proveedores:
                nombre = getattr(p, "nombre", "")
                contacto = getattr(p, "contacto", "")
                telefono = getattr(p, "telefono", "")
                if (filtro in nombre.lower() or
                    filtro in str(contacto).lower() or
                    filtro in str(telefono).lower()):
                    tree.insert('', 'end', values=(nombre, contacto, telefono))
                    encontrados = True
            if not encontrados:
                tree.insert('', 'end', values=("No hay proveedores que coincidan", "", ""))

        var_buscar.trace('w', lambda *a: mostrar_proveedores())
        mostrar_proveedores()

        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat").pack(pady=10)

    def agregar_proveedor(self):
        """
        Muestra un formulario moderno para agregar un proveedor con validación.
        """
        win = tk.Toplevel(self.root)
        win.title("Agregar Proveedor")
        win.geometry("370x320")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="🚚 Agregar Proveedor", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(18, 10))

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        tk.Label(frame, text="Nombre *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_nombre = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_nombre.pack(fill=tk.X, pady=(0, 8))

        tk.Label(frame, text="Contacto", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_contacto = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_contacto.pack(fill=tk.X, pady=(0, 8))

        tk.Label(frame, text="Teléfono", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_telefono = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_telefono.pack(fill=tk.X, pady=(0, 8))

        def guardar():
            nombre = entry_nombre.get().strip()
            contacto = entry_contacto.get().strip()
            telefono = entry_telefono.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio.", parent=win)
                return
            # Validación opcional de teléfono
            if telefono and not telefono.isdigit():
                messagebox.showerror("Error", "El teléfono debe contener solo números.", parent=win)
                return
            # Crear proveedor (ajusta según tu clase Proveedor)
            from Proveedor import Proveedor
            nuevo = Proveedor(nombre, contacto, telefono)
            self.proveedores.append(nuevo)
            Persistencia.guardar(self.proveedores, "proveedores.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Guardar", command=guardar, bg="#2980b9", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        
    def ver_clientes(self):
        """
        Muestra la lista de clientes en una ventana con búsqueda y detalles, con mejor estética.
        """
        if not self.clientes:
            messagebox.showinfo("Clientes", "No hay clientes registrados.")
            return
        win = tk.Toplevel(self.root)
        win.title("Lista de Clientes")
        win.geometry("750x480")
        win.configure(bg="#f5f5f5")
        tk.Label(win, text="👤 Lista de Clientes", font=("Arial", 15, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=8)
        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True)
        # Campo de búsqueda
        buscador_frame = tk.Frame(frame, bg="#f5f5f5")
        buscador_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(buscador_frame, text="🔍 Buscar:", font=("Arial", 12), bg="#f5f5f5").pack(side="left", padx=(0, 5))
        var_buscar = tk.StringVar()
        entry_buscar = tk.Entry(buscador_frame, textvariable=var_buscar, font=("Arial", 11), bg="#ecf0f1", relief="flat")
        entry_buscar.pack(side="left", fill=tk.X, expand=True)
        entry_buscar.focus_set()
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
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#27ae60", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#f5f5f5", fieldbackground="#f5f5f5")
        style.map("Treeview", background=[("selected", "#d0e6fa")])
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
            if not tree.get_children():
                tree.insert('', 'end', values=("No hay clientes que coincidan", "", "", "", ""))
        var_buscar.trace('w', lambda *a: cargar_clientes())
        cargar_clientes()
        # Panel de detalle
        frame_det = tk.Frame(win, bg="#f5f5f5")
        frame_det.pack(fill=tk.X, padx=10, pady=5)
        label_det = tk.Label(frame_det, text="Seleccione un cliente para ver detalles", justify="left", anchor="w", bg="#f5f5f5")
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
        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat").pack(pady=10)
        
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
            
    # --- PRODUCTOS ---

    def editar_producto(self):
        """
        Edita un producto existente seleccionándolo de una lista.
        """
        productos = self.inventario.listar_productos()
        self.editar_elemento(productos, "producto", "nombre", self.editar_producto_individual)

    def eliminar_producto(self):
        """
        Elimina un producto existente seleccionándolo de una lista.
        """
        productos = self.inventario.listar_productos()
        self.eliminar_elemento(productos, "producto", "nombre", lambda: Persistencia.guardar(self.inventario, "inventario.pkl"))

    # --- CLIENTES ---

    def editar_cliente(self):
        """
        Edita un cliente existente seleccionándolo de una lista.
        """
        self.editar_elemento(self.clientes, "cliente", "nombre", self.editar_cliente_individual)

    def eliminar_cliente(self):
        """
        Elimina un cliente existente seleccionándolo de una lista.
        """
        self.eliminar_elemento(self.clientes, "cliente", "nombre", lambda: Persistencia.guardar(self.clientes, "clientes.pkl"))

    # --- PROVEEDORES ---

    def editar_proveedor(self):
        """
        Edita un proveedor existente seleccionándolo de una lista.
        """
        self.editar_elemento(self.proveedores, "proveedor", "nombre", self.editar_proveedor_individual)

    def eliminar_proveedor(self):
        """
        Elimina un proveedor existente seleccionándolo de una lista.
        """
        self.eliminar_elemento(self.proveedores, "proveedor", "nombre", lambda: Persistencia.guardar(self.proveedores, "proveedores.pkl"))

    def eliminar_elemento(self, lista, tipo, atributo="nombre", callback_post=None):
        """
        Elimina un elemento de una lista (producto, cliente o proveedor) tras confirmación del usuario.
        """
        if not lista:
            messagebox.showinfo(f"Eliminar {tipo.title()}", f"No hay {tipo}s registrados.")
            return

        def eliminar(elem, win_busqueda):
            win_busqueda.destroy()
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar '{getattr(elem, atributo, str(elem))}'?")
            if confirm:
                if tipo == "producto":
                    # Elimina por nombre, no por objeto
                    self.inventario.eliminar_producto(elem.nombre)
                elif tipo == "cliente":
                    self.clientes.remove(elem)
                elif tipo == "proveedor":
                    self.proveedores.remove(elem)
                messagebox.showinfo("Éxito", f"{tipo.title()} eliminado correctamente.")
                if callback_post:
                    callback_post()

        self.seleccionar_elemento_con_busqueda(tipo, lista, atributo, eliminar)
            
    def editar_elemento(self, lista, tipo, atributo="nombre", editar_callback=None):
        """
        Edita un elemento de una lista (productos, clientes, proveedores) usando el buscador genérico.
        editar_callback: función que recibe (elemento, win_busqueda) y abre el formulario de edición.
        """
        if not lista:
            messagebox.showinfo(f"Editar {tipo.title()}", f"No hay {tipo}s registrados.")
            return
        def editar(elem, win_busqueda):
            win_busqueda.destroy()
            if editar_callback:
                editar_callback(elem)
        self.seleccionar_elemento_con_busqueda(tipo, lista, atributo, editar)
        
    def editar_producto_individual(self, producto):
        """
        Abre un formulario moderno para editar un producto.
        """
        win = tk.Toplevel(self.root)
        win.title(f"Editar Producto: {producto.nombre}")
        win.geometry("420x420")
        win.resizable(False, False)
        win.configure(bg="#f5f5f5")

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame, text="Editar Producto", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(0, 15))

        campos = [
            ("Nombre", "nombre"),
            ("Precio de venta", "precio_venta"),
            ("Stock", "stock"),
            ("Categoría", "categoria"),
            ("Stock mínimo", "stock_minimo"),
            ("Disponible", "disponible")
        ]
        entradas = {}

        for label, key in campos:
            fr = tk.Frame(frame, bg="#f5f5f5")
            fr.pack(fill=tk.X, pady=5)
            tk.Label(fr, text=label + ":", font=("Arial", 11), width=15, anchor="w", bg="#f5f5f5").pack(side="left")
            if key == "disponible":
                entradas[key] = tk.BooleanVar(value=getattr(producto, 'disponible', True))
                ttk.Checkbutton(fr, variable=entradas[key], text="Sí").pack(side="left")
            else:
                ent = ttk.Entry(fr, font=("Arial", 11))
                ent.pack(side="left", fill=tk.X, expand=True)
                entradas[key] = ent

        # Rellenar campos con los datos actuales
        entradas["nombre"].insert(0, producto.nombre)
        entradas["precio_venta"].insert(0, f"{getattr(producto, 'precio', 0):.2f}")
        entradas["stock"].insert(0, str(getattr(producto, 'stock', 0)))
        entradas["categoria"].insert(0, getattr(producto, 'categoria', ''))
        entradas["stock_minimo"].insert(0, str(getattr(producto, 'stock_minimo', 1)))

        def guardar():
            nombre_anterior = producto.nombre  # Guarda el nombre original
            nombre = entradas["nombre"].get().strip()
            precio_venta = entradas["precio_venta"].get().strip()
            stock = entradas["stock"].get().strip()
            categoria = entradas["categoria"].get().strip()
            stock_minimo = entradas["stock_minimo"].get().strip()
            disponible = entradas["disponible"].get()

            # Validaciones
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.", parent=win)
                return
            # --- Validación de duplicados por nombre ---
            if any(p.nombre.lower() == nombre.lower() for p in self.inventario.listar_productos()):
                messagebox.showerror("Error", f"Ya existe un producto con el nombre '{nombre}'.", parent=win)
                return
            try:
                precio_venta = float(precio_venta)
                stock = int(stock)
                stock_minimo = int(stock_minimo)
            except Exception:
                messagebox.showerror("Error", "Precio y stock deben ser números válidos.", parent=win)
                return
            if precio_venta < 0 or stock < 0 or stock_minimo < 0:
                messagebox.showerror("Error", "Ningún valor puede ser negativo.", parent=win)
                return

            # Actualizar producto
            producto.nombre = nombre
            producto.precio = precio_venta
            producto.stock = stock
            producto.categoria = categoria
            producto.stock_minimo = stock_minimo
            producto.disponible = disponible

            # --- ACTUALIZA LA CLAVE EN EL INVENTARIO SI CAMBIA EL NOMBRE ---
            if hasattr(self.inventario, "_productos"):
                if nombre_anterior.lower() != nombre.lower():
                    prod = self.inventario._productos.pop(nombre_anterior.lower(), None)
                    if prod:
                        self.inventario._productos[nombre.lower()] = prod

            Persistencia.guardar(self.inventario, "inventario.pkl")
            win.destroy()

        btn_frame = tk.Frame(frame, bg="#f5f5f5")
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Guardar cambios", command=guardar, style="Accent.TButton").pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side="left", padx=10)
    
    def editar_proveedor_individual(self, proveedor):
        """
        Abre un formulario moderno para editar un proveedor.
        """
        win = tk.Toplevel(self.root)
        win.title(f"Editar Proveedor: {proveedor.nombre}")
        win.geometry("370x320")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="🚚 Editar Proveedor", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(18, 10))

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        tk.Label(frame, text="Nombre *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_nombre = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_nombre.pack(fill=tk.X, pady=(0, 8))
        entry_nombre.insert(0, proveedor.nombre)

        tk.Label(frame, text="Contacto", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_contacto = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_contacto.pack(fill=tk.X, pady=(0, 8))
        entry_contacto.insert(0, getattr(proveedor, "contacto", ""))

        tk.Label(frame, text="Teléfono", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_telefono = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_telefono.pack(fill=tk.X, pady=(0, 8))
        entry_telefono.insert(0, getattr(proveedor, "telefono", ""))

        def guardar():
            nombre = entry_nombre.get().strip()
            contacto = entry_contacto.get().strip()
            telefono = entry_telefono.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio.", parent=win)
                return
            if telefono and not telefono.isdigit():
                messagebox.showerror("Error", "El teléfono debe contener solo números.", parent=win)
                return
            proveedor.nombre = nombre
            proveedor.contacto = contacto
            proveedor.telefono = telefono
            Persistencia.guardar(self.proveedores, "proveedores.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Guardar", command=guardar, bg="#2980b9", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
    
    def editar_cliente_individual(self, cliente):
        """
        Abre un formulario moderno para editar un cliente (alumno o profesor).
        """
        win = tk.Toplevel(self.root)
        win.title(f"Editar Cliente: {cliente.nombre}")
        win.geometry("420x420")
        win.configure(bg="#f5f5f5")

        tk.Label(win, text="👤 Editar Cliente", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f5f5f5").pack(pady=(18, 10))

        frame = tk.Frame(win, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        tipo = cliente.__class__.__name__
        tk.Label(frame, text=f"Tipo: {tipo}", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(anchor="w", pady=(0, 8))

        tk.Label(frame, text="Nombre *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_nombre = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_nombre.pack(fill=tk.X, pady=(0, 8))
        entry_nombre.insert(0, cliente.nombre)

        tk.Label(frame, text="Grado/Lugar *", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
        entry_grado = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
        entry_grado.pack(fill=tk.X, pady=(0, 8))
        entry_grado.insert(0, getattr(cliente, "grado", getattr(cliente, "lugar", "")))

        # Si es alumno, permite editar saldo prepago y deuda
        if hasattr(cliente, "saldo_prepago"):
            tk.Label(frame, text="Saldo prepago", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
            entry_prepago = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
            entry_prepago.pack(fill=tk.X, pady=(0, 8))
            entry_prepago.insert(0, f"{getattr(cliente, 'saldo_prepago', 0):.2f}")

        if hasattr(cliente, "deuda"):
            tk.Label(frame, text="Deuda", font=("Arial", 12), bg="#f5f5f5").pack(anchor="w", pady=(0, 2))
            entry_deuda = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", relief="flat")
            entry_deuda.pack(fill=tk.X, pady=(0, 8))
            entry_deuda.insert(0, f"{getattr(cliente, 'deuda', 0):.2f}")

        def guardar():
            nombre = entry_nombre.get().strip()
            grado = entry_grado.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.", parent=win)
                return
            if not grado:
                messagebox.showerror("Error", "El grado/lugar no puede estar vacío.", parent=win)
                return
            cliente.nombre = nombre
            if hasattr(cliente, "grado"):
                cliente.grado = grado
            elif hasattr(cliente, "lugar"):
                cliente.lugar = grado
            if hasattr(cliente, "saldo_prepago"):
                try:
                    saldo = float(entry_prepago.get())
                    if saldo < 0:
                        raise ValueError
                    cliente.saldo_prepago = saldo
                except Exception:
                    messagebox.showerror("Error", "Saldo prepago inválido.", parent=win)
                    return
            if hasattr(cliente, "deuda"):
                try:
                    deuda = float(entry_deuda.get())
                    if deuda < 0:
                        raise ValueError
                    cliente.deuda = deuda
                except Exception:
                    messagebox.showerror("Error", "Deuda inválida.", parent=win)
                    return
            Persistencia.guardar(self.clientes, "clientes.pkl")
            win.destroy()

        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Guardar", command=guardar, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancelar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", width=12).pack(side="left", padx=8)
        
    # ELIMINAR
    def eliminar_cliente_por_nombre(self, nombre):
        self.clientes = [c for c in self.clientes if getattr(c, "nombre", "") != nombre]

    def eliminar_proveedor_por_nombre(self, nombre):
        self.proveedores = [p for p in self.proveedores if getattr(p, "nombre", "") != nombre]

    def posicionar_ventana_arriba(self, win, ancho, alto):
        """
        Posiciona la ventana win centrada horizontalmente y pegada arriba de la pantalla.
        """
        win.update_idletasks()
        pantalla_ancho = win.winfo_screenwidth()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = 0  # bien arriba
        win.geometry(f"{ancho}x{alto}+{x}+{y}")