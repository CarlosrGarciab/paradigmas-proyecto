from Cliente import Cliente

class Profesor(Cliente):
    def __init__(self, nombre, grado):
        super().__init__(nombre)
        self._grado = grado
        # La deuda ya está en Cliente, no hace falta redefinirla

    @property
    def grado(self):
        return self._grado

    @grado.setter
    def grado(self, lista_grado):
        self._grado = lista_grado

    def __str__(self):
        return (
            f"Nombre: {self.nombre}\n"
            f"Grado donde enseña: {self.grado}\n"
            f"Deuda: {self.deuda:.2f}"
        )