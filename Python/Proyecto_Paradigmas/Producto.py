class Producto:
    _id_counter = 1  # Variable de clase para autoincremento

    def __init__(self, nombre, precio, stock, stock_minimo, categoria=None):
        self.__id = Producto._id_counter
        Producto._id_counter += 1  # Incrementar el contador
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock
        self.__stock_minimo = stock_minimo
        self.__categoria = categoria

    # Id
    @property
    def id(self):
        return self.__id

    # Nombre
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre_nuevo):
        self.__nombre = nombre_nuevo

    # Precio
    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, precio_nuevo):
        if precio_nuevo < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio_nuevo

    # Stock
    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, stock_nuevo):
        if stock_nuevo < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.__stock = stock_nuevo

    # Stock mínimo
    @property
    def stock_minimo(self):
        return self.__stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, stock_minimo_nuevo):
        if stock_minimo_nuevo < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        if stock_minimo_nuevo > self.stock:
            raise ValueError("El stock mínimo no puede ser mayor que el stock actual.")
        self.__stock_minimo = stock_minimo_nuevo

    # Categoría
    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, nueva_categoria):
        self.__categoria = nueva_categoria

    # Métodos
    def actualizar_stock(self, cantidad):
        self.stock += cantidad

    def reducir_stock(self, cantidad):
        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= cantidad

    def verificar_disponibilidad(self, cantidad):
        return self.stock >= cantidad

    def reiniciar_stock(self):
        self.stock = self.stock_minimo

    def valor_total_stock(self):
        return self.precio * self.stock

    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    def __str__(self):
        return f"{self.nombre} (ID: {self.id}) - Precio: {self.precio:.2f} - Stock: {self.stock} - Categoría: {self.categoria or 'Sin categoría'}"