from Cliente import Cliente

class Profesor(Cliente):
    def __init__(self, nombre, id_cliente, grado):
        super().__init__(nombre, id_cliente)
        self._grado = grado

    # |--- Getters y Setters ---|
    # Curso
    @property
    def grado(self):
        return self._grado

    @grado.setter
    def grado(self, lista_grado):
        self._grado = lista_grado

    # Método mostrar datos
    def __str__(self):
        return (
            f"Nombre: {self.nombre}\n"
            f"ID: {self.id_cliente}\n"
            f"grado donde enseña: {self.grado}"
        )