class Producto:
    """
    Representa un producto de la cantina.
    Gestiona nombre, precio, stock y categoría.
    """
    def __init__(self, nombre, precio, stock, categoria=None, stock_minimo=1, disponible=True):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.stock_minimo = stock_minimo
        self.disponible = disponible

    # Getters y Setters
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre_nuevo):
        if not nombre_nuevo or not isinstance(nombre_nuevo, str):
            raise ValueError("El nombre debe ser un texto no vacío.")
        self._nombre = nombre_nuevo

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, precio_nuevo):
        if precio_nuevo < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = precio_nuevo

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock_nuevo):
        if stock_nuevo < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = stock_nuevo

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, nueva_categoria):
        self._categoria = nueva_categoria

    @property
    def stock_minimo(self):
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor):
        if valor < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        self._stock_minimo = valor

    @property
    def disponible(self):
        return getattr(self, '_disponible', True)

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    # Métodos de negocio centralizados
    def agregar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a agregar debe ser positiva.")
        self._stock += cantidad

    def vender(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser positiva.")
        if cantidad > self._stock:
            raise ValueError("Stock insuficiente.")
        self._stock -= cantidad

    def actualizar_datos(self, nombre=None, precio=None, categoria=None, stock_minimo=None, disponible=None):
        if nombre is not None:
            self.nombre = nombre
        if precio is not None:
            self.precio = precio
        if categoria is not None:
            self.categoria = categoria
        if stock_minimo is not None:
            self.stock_minimo = stock_minimo
        if disponible is not None:
            self.disponible = disponible

    def __str__(self):
        return f"{self.nombre} - Precio: {self.precio:.2f} - Stock: {self.stock} - Categoría: {self.categoria or 'Sin categoría'} - {'Disponible' if self.disponible else 'No disponible para venta'}"