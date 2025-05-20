from Cliente import Cliente

class Profesor(Cliente):
    """
    Representa a un profesor cliente de la cantina.
    Incluye el grado donde enseña.
    """
    def __init__(self, nombre, grado):
        """
        Inicializa un profesor con nombre y grado donde enseña.
        """
        super().__init__(nombre)
        self._grado = grado

    @property
    def grado(self):
        """Grado donde enseña el profesor."""
        return self._grado

    @grado.setter
    def grado(self, lista_grado):
        """Permite cambiar el grado donde enseña el profesor."""
        self._grado = lista_grado

    def __str__(self):
        """
        Representación en texto del profesor (sin mostrar el ID).
        """
        return (
            f"Nombre: {self.nombre}\n"
            f"Grado donde enseña: {self.grado}\n"
            f"Deuda: {self.deuda:.2f}"
        )