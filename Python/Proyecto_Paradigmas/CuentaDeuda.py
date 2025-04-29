class CuentaDeuda:
   def __init__(self, deuda):
      self.__deuda = deuda

   # Getter
   @property
   def deuda(self):
      return self.__deuda

   # Métodos
   def sumar_deuda(self, valor):
      self.__deuda += valor

   def pagar(self, valor):
      self.__saldo -= valor

   def tiene_deuda(self):
      return self.__saldo > 0

   def __str__(self):
      return f"Deuda actual: {self.__saldo:.2f}"
