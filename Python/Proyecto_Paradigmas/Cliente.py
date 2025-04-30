from abc import ABC, abstractmethod

class Cliente(ABC):
    def _init_(self, id, nombre_completo, tipo):
        self.__id = id
        self.__nombre_completo = nombre_completo
        self.__tipo = tipo
        self.__deuda = 0
        self.__saldo = 0

# |--- Getters y Setters ---|
# Id
@property
def id(self):
    return self.__id

# Nombre
@property
def nombre_completo(self):
    return self.__nombre

@nombre_completo.setter
def nombre(self, nuevo_nombre):
    self.__nombre = nuevo_nombre

# Tipo    
@property
def tipo(self):
    return self.__tipo

@tipo.setter
def tipo(self, nuevo_tipo):
    self.__tipo = nuevo_tipo

# Deuda
@property
def deuda(self):
    return self.__deuda

@deuda.setter
def deuda(self, valor):
    self.__deuda = valor

# Saldo
@property
def saldo(self):
    return self.__saldo

@saldo.setter
def saldo(self, valor):
    self.__saldo = valor

# Métodos a implementar
def realizar_compra():
    pass