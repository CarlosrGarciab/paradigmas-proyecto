class CuentaPrepago:
  def __init__(self, saldo_inicial):
    self.__saldo = saldo_inicial

  # Getter
  @property
  def saldo(self):
    return self.__saldo

  # Métodos
  def cargar_credito(self, valor):
    self.__saldo += valor

  def descontar(self, valor):
    self.__saldo -= valor

  def tiene_credito(self):
    return self.__saldo > 0

  def __str__(self):
    return f"Saldo cuenta prepaga: {self.__saldo:.2f}"