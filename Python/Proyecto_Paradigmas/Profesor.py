from Cliente import Cliente

class Profesor(Cliente):
    def __init__(self, id_cliente, nombre, grado):
        super().__init__(id_cliente, nombre)
        self._grado = grado

    @property
    def grado(self):
        return self._grado

    @grado.setter
    def grado(self, lista_grado):
        self._grado = lista_grado

    def __str__(self):
        return (
            f"Nombre: {self.nombre}\n"
            f"ID: {self.id}\n"
            f"Grado donde enseña: {self.grado}"
        )