from abc import ABC, abstractmethod

class Pago(ABC):
    def __init__(self, id, fecha, monto, tipo):
        self.__id = id
        self.__fecha = fecha
        self.__monto = monto
        self.__tipo = tipo

    # |--- Getters y Setters ---|
    # Id
    @property
    def id(self):
        return self.__id

    # Fecha
    @property
    def fecha(self):
        return self.__fecha

    # Monto
    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, monto_nuevo):
        self.__monto = monto_nuevo

    # Tipo
    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo_nuevo):
        self.__tipo = tipo_nuevo

    # Método
    @abstractmethod
    def procesar_pago(self):
        pass