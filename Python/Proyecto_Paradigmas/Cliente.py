from abc import ABC, abstractmethod

class Cliente(ABC):
    def _init_(self, nombre):
        self.__nombre = nombre
        self.__deuda = 0
        self.__saldo = 0

# |--- Getters y Setters ---|
# Nombre
@property
def nombre(self):
    return self.__nombre

@nombre.setter
def nombre(self, nuevo_nombre):
    self.__nombre = nuevo_nombre

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

# posibles metodos: realizar compra, pagar deuda, tiene_deuda, mostrar_datos(abs)