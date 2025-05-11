from abc import ABC, abstractmethod

class Cliente(ABC):
    def __init__(self, id, nombre):
        self._id = id
        self._nombre = nombre
        self._deuda = 0

    # Id
    @property
    def id(self):
        return self._id

    # Nombre
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    # Deuda
    @property
    def deuda(self):
        return self._deuda

    @deuda.setter
    def deuda(self, valor):
        self._deuda = valor