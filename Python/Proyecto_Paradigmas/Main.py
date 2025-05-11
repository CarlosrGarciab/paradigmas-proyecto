from Alumno import Alumno
from Profesor import Profesor
from Caja import Caja
from CuentaBanco import CuentaBanco
from PagoEfectivo import PagoEfectivo
from PagoDeuda import PagoDeuda
from PagoPrepago import PagoPrepago
from PagoTransferencia import PagoTransferencia

def main():
    # Crear la caja y cuenta bancaria de la cantina
    caja = Caja()
    banco = CuentaBanco()

    # Crear clientes
    alumno = Alumno(1, "Carlos", "9no", 100000)
    profesor = Profesor(2, "Laura", "Nivel medio")

    # Mostrar estado inicial
    print(f"\n=== Estado inicial ===")
    print(f"Caja: {caja.dinero}")
    print(f"Banco: {banco.saldo}")
    print(f"Prepago de {alumno.nombre}: {alumno._saldo_cuenta_prepaga}")
    print(f"Deuda de {alumno.nombre}: {alumno.deuda}")
    print(f"Deuda de {profesor.nombre}: {profesor.deuda}")

    # Venta 1: Alumno paga con cuenta prepago (3000)
    print("\nVenta 1: Alumno paga con prepago (3000)")
    pago1 = PagoPrepago(alumno, 3000)
    pago1.procesar_pago()

    # Venta 2: Alumno paga con efectivo (entrega 10000 por compra de 7000)
    print("\nVenta 2: Alumno paga con efectivo (7000)")
    pago2 = PagoEfectivo(caja, 7000)
    pago2.procesar_pago()

    # Venta 3: Alumno paga a deuda (2000)
    print("\nVenta 3: Alumno paga a deuda (2000)")
    pago3 = PagoDeuda(alumno, 2000)
    pago3.procesar_pago()

    # Venta 4: Profesor paga con efectivo (entrega 5000 por compra de 4000)
    print("\nVenta 4: Profesor paga con efectivo (4000)")
    pago4 = PagoEfectivo(caja, 4000)
    pago4.procesar_pago()

    # Venta 5: Profesor paga con transferencia (6000)
    print("\nVenta 5: Profesor paga con transferencia (6000)")
    pago5 = PagoTransferencia(banco, 6000)
    pago5.procesar_pago()

    # Venta 6: Profesor paga a deuda (1000)
    print("\nVenta 6: Profesor paga a deuda (1000)")
    pago6 = PagoDeuda(profesor, 1000)
    pago6.procesar_pago()

    # Mostrar estado final
    print(f"\n=== Estado final ===")
    print(f"Caja: {caja.dinero}")
    print(f"Banco: {banco.saldo}")
    print(f"Prepago de {alumno.nombre}: {alumno._saldo_cuenta_prepaga}")
    print(f"Deuda de {alumno.nombre}: {alumno.deuda}")
    print(f"Deuda de {profesor.nombre}: {profesor.deuda}")

if __name__ == "__main__":
    main()