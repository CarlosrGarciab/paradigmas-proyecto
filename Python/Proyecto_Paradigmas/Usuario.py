class Usuario:
    def __init__(self, id, nombre, tipo, saldo = 0.0, deuda = 0.0):
        self.__id = id
        self.__nombre = nombre
        self.__tipo = tipo
        self.__saldo = saldo
        self.__deuda = deuda

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

    # Tipo
    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo_nuevo):
        self.__tipo = tipo_nuevo

    # Saldo
    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo_nuevo):
        self.__saldo = saldo_nuevo

    # Deuda
    @property
    def deuda(self):
        return self.__deuda

    @deuda.setter
    def deuda(self, deuda_nuevo):
        self.__deuda = deuda_nuevo