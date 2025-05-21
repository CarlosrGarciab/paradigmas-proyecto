class Producto:
    """
    Representa un producto de la cantina.
    Gestiona nombre, precio, stock, stock mínimo y categoría.
    """
    _id_counter = 1  # Variable de clase para autoincremento

    def __init__(self, nombre, precio, stock, stock_minimo, categoria=None):
        """
        Inicializa un producto con nombre, precio, stock, stock mínimo y categoría.
        """
        self._id = Producto._id_counter
        Producto._id_counter += 1  # Incrementar el contador
        self._nombre = nombre
        self._precio = precio
        self._stock = stock
        self._stock_minimo = stock_minimo
        self._categoria = categoria

    # Id
    @property
    def id(self):
        """ID único del producto (solo lectura)."""
        return self._id

    # Nombre
    @property
    def nombre(self):
        """Nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, nombre_nuevo):
        """Permite cambiar el nombre del producto."""
        self._nombre = nombre_nuevo

    # Precio
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

    # Stock
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

    # Stock mínimo
    @property
    def stock_minimo(self):
        """Stock mínimo recomendado para el producto."""
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, stock_minimo_nuevo):
        """Permite cambiar el stock mínimo del producto."""
        if stock_minimo_nuevo < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        if stock_minimo_nuevo > self.stock:
            raise ValueError("El stock mínimo no puede ser mayor que el stock actual.")
        self._stock_minimo = stock_minimo_nuevo

    # Categoría
    @property
    def categoria(self):
        """Categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, nueva_categoria):
        """Permite cambiar la categoría del producto."""
        self._categoria = nueva_categoria

    # Métodos
    def actualizar_stock(self, cantidad):
        """
        Suma la cantidad indicada al stock del producto.
        """
        self.stock += cantidad

    def reducir_stock(self, cantidad):
        """
        Resta la cantidad indicada al stock del producto.
        Lanza un error si no hay suficiente stock.
        """
        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= cantidad

    def verificar_disponibilidad(self, cantidad):
        """
        Verifica si hay suficiente stock para una cantidad dada.
        """
        return self.stock >= cantidad

    def reiniciar_stock(self):
        """
        Reinicia el stock al valor del stock mínimo.
        """
        self.stock = self.stock_minimo

    def valor_total_stock(self):
        """
        Calcula el valor total del stock disponible.
        """
        return self.precio * self.stock

    def stock_bajo(self):
        """
        Indica si el stock está por debajo o igual al mínimo.
        """
        return self.stock <= self.stock_minimo

    def __str__(self):
        """
        Representación en texto del producto.
        """
        return f"{self.nombre} (ID: {self.id}) - Precio: {self.precio:.2f} - Stock: {self.stock} - Categoría: {self.categoria or 'Sin categoría'}"