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
        super().__init__(nombre, grado)