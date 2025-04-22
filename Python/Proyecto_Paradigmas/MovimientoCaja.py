class MovimientoCaja:
    def __init__(self, id, fecha, tipo, descripcion, monto):
        self.__id = id
        self.__fecha = fecha
        self.__tipo = tipo
        self.__descripcion = descripcion
        self.__monto = monto

    # |--- Getters y Setters ---|
    # Id
    @property
    def id(self):
        return self.__id

    # Fecha
    @property
    def fecha(self):
        return self.__fecha

    # Tipo
    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo_nuevo):
        self.__tipo = tipo_nuevo

    # Descripción
    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion_nuevo):
        self.__descripcion = descripcion_nuevo

    # Monto
    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, monto_nuevo):
        self.__monto = monto_nuevo
