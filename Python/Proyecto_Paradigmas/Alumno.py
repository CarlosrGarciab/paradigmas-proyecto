import Cliente

class Alumno(Cliente):
    def __init__(self, id_cliente, nombre, grado, saldo_cuenta_prepaga):
        super().__init__(nombre, id_cliente)
        self._grado = grado
        self._saldo_cuenta_prepaga = saldo_cuenta_prepaga

# |--- Getters y Setters ---|
# Grado
@property
def grado(self):
    return self._grado

@grado.setter
def grado(self, valor):
    self._grado = valor
    
# Saldo de la cuenta prepaga
@property
def saldo_cuenta_prepaga(self):
    return self._saldo_cuenta_prepaga

@saldo_cuenta_prepaga.setter
def saldo_cuenta_prepaga(self, valor):
    self._saldo_cuenta_prepaga = valor
    
# Método recargar la cuenta prepaga
def recargar_cuenta_prepaga(self, valor):
    self._saldo_cuenta_prepaga += valor
    
# Método mostrar datos
def __str__(self):
    return (
        f"Nombre: {self.nombre}\n"
        f"ID: {self.id_cliente}\n"
        f"Grado: {self.grado}\n"
        f"Sección: {self.seccion}\n"
        f"Saldo Cuenta Prepaga: S/ {self.saldo_cuenta_prepaga:.2f}"
    )