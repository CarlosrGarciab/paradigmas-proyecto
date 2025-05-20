from Pago import Pago

class PagoPrepago(Pago):
    def __init__(self, cliente, monto):
        super().__init__(monto)
        self.cliente = cliente

    def procesar_pago(self, monto):
        if self.cliente.saldo_prepago >= monto:
            self.cliente.saldo_prepago -= monto
            print(f"Pago prepago procesado: S/{monto:.2f} descontado del saldo prepago de {self.cliente.nombre}.")
            return True
        else:
            print("Saldo prepago insuficiente.")
            return False