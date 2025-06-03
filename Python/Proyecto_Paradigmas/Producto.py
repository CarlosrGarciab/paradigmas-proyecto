class Producto:
    """
    Representa un producto de la cantina.
    Gestiona nombre, precio, stock y categoría.
    """
    _id_counter = 1  # Variable de clase para autoincremento de IDs

    def __init__(self, nombre, precio, stock, categoria = None, stock_minimo = 1):
        """
        Inicializa un producto con nombre, precio, stock, stock mínimo y categoría.
        """
        self._id = Producto._id_counter
        Producto._id_counter += 1
        self._nombre = nombre
        self._precio = precio
        self._stock = stock
        self._categoria = categoria
        self._categoria = categoria
        self._stock_minimo = stock_minimo

    # Getters y Setters
    @property
    def id(self):
        """ID único del producto."""
        return self._id

    @property
    def nombre(self):
        """Nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, nombre_nuevo):
        """Permite cambiar el nombre del producto."""
        self._nombre = nombre_nuevo

    @property
    def precio(self):
        """Precio de venta del producto."""
        return self._precio

    @precio.setter
    def precio(self, precio_nuevo):
        """Permite cambiar el precio del producto."""
        if precio_nuevo < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = precio_nuevo

    @property
    def stock(self):
        """Stock actual del producto."""
        return self._stock

    @stock.setter
    def stock(self, stock_nuevo):
        """Permite cambiar el stock del producto."""
        if stock_nuevo < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = stock_nuevo

    @property
    def categoria(self):
        """Categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, nueva_categoria):
        """Permite cambiar la categoría del producto."""
        self._categoria = nueva_categoria
        
    @property
    def stock_minimo(self):
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor):
        self._stock_minimo = valor

    # Metodos
    def actualizar_stock(self, cantidad):
        """
        Suma la cantidad indicada al stock del producto.
        """
        self._stock += cantidad

    def reducir_stock(self, cantidad):
        """
        Resta la cantidad indicada al stock del producto.
        Lanza un error si no hay suficiente stock.
        """
        if cantidad > self._stock:
            raise ValueError("No hay suficiente stock disponible.")
        self._stock -= cantidad

    def __str__(self):
        """
        Representación en texto del producto.
        """
        return f"{self._nombre} (ID: {self._id}) - Precio: {self._precio:.2f} - Stock: {self._stock} - Categoría: {self._categoria or 'Sin categoría'}"