class Producto:
    def __init__(self, id, nombre, precio, stock, stock_minimo, categoria):
        self.__id = id
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock
        self.__stock_minimo = stock_minimo
        self.__categoria = categoria

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

    # Categoría
    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria_nuevo):
        self.__categoria = categoria_nuevo
