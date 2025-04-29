class Producto:
    def __init__(self, id, nombre, precio, stock, stock_minimo):
        self.__id = id
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock
        self.__stock_minimo = stock_minimo

    # |--- Getters y Setters ---|
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
        self.__precio = precio_nuevo

    # Stock
    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, stock_nuevo):
        self.__stock = stock_nuevo

    # Stock mínimo
    @property
    def stock_minimo(self):
        return self.__stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, stock_minimo_nuevo):
        self.__stock_minimo = stock_minimo_nuevo
        
    # Métodos
    def actualizar_stock(self, cantidad):
        self.stock += cantidad
        
    def modificar_precio(self, nuevo_precio):
        self.precio = nuevo_precio
        
    def stock_bajo(self):
        return self.stock <= self.stock_minimo
        
    def __str__(self):
        return f"{self.nombre} (ID: {self.id}) - Precio: {self.precio:.2f} - Stock: {self.stock}"
