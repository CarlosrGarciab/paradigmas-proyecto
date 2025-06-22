# type: ignore

from pyDatalog import pyDatalog

pyDatalog.create_terms('Producto, Cliente, Alumno, Proveedor, bajo_stock, disponible_venta, cliente_con_deuda, alumno_puede_prepago, venta_valida, compra_valida, pago_efectivo_valido, pago_transferencia_valido, recarga_prepago_valida, pago_deuda_valido, Stock, StockMinimo, Disponible, Nombre, Deuda, SaldoPrepago, Monto, Total, Cantidad, CajaDinero, BancoSaldo, ProveedorNombre, Precio, ProductoNombre, CantidadVendida')

# --- Hechos de ejemplo ---
+Producto('Galleta', 2, 5, True)
+Producto('Jugo', 10, 5, True)
+Producto('Sandwich', 4, 4, False)
+Cliente('Ana', 0)
+Cliente('Luis', 15.5)
+Alumno('Sofía', 8.0)
+Proveedor('Proveedor1')
+Proveedor('Proveedor2')

# --- Reglas de negocio ---

# 1. Producto en bajo stock
bajo_stock(Nombre) <= (Producto(Nombre, Stock, StockMinimo, Disponible) & (Stock <= StockMinimo))

# 2. Producto disponible para la venta
disponible_venta(Nombre) <= (Producto(Nombre, Stock, StockMinimo, Disponible) & (Disponible == True) & (Stock > 0))

# 3. Cliente con deuda
cliente_con_deuda(Nombre) <= (Cliente(Nombre, Deuda) & (Deuda > 0))

# 4. Alumno puede pagar con prepago si saldo prepago >= monto
alumno_puede_prepago(Nombre, Monto) <= (Alumno(Nombre, SaldoPrepago) & (SaldoPrepago >= Monto))

# 5. Venta válida (simplificada: cantidad vendida <= stock actual)
venta_valida(ProductoNombre, CantidadVendida) <= (Producto(ProductoNombre, Stock, StockMinimo, Disponible) & (CantidadVendida <= Stock))

# 6. Compra válida si el proveedor existe y cantidad y precio son positivos
compra_valida(ProveedorNombre, Cantidad, Precio) <= (Proveedor(ProveedorNombre)) & (Cantidad > 0) & (Precio > 0)

# 7. Pago en efectivo válido si monto entregado >= total
pago_efectivo_valido(Monto, Total) <= (Monto >= Total)

# 8. Pago por transferencia válido si el banco puede recibir el monto
pago_transferencia_valido(Monto, BancoSaldo) <= (BancoSaldo >= Monto)

# 9. Recarga prepago válida si monto > 0 y hay suficiente dinero en caja o banco
recarga_prepago_valida(Monto, CajaDinero, BancoSaldo) <= (Monto > 0) & (CajaDinero >= Monto)
recarga_prepago_valida(Monto, CajaDinero, BancoSaldo) <= (Monto > 0) & (BancoSaldo >= Monto)

# 10. Pago de deuda válido si monto > 0 y monto <= deuda
pago_deuda_valido(Monto, Deuda) <= (Monto > 0) & (Monto <= Deuda)

# --- Consultas de ejemplo ---
print("Productos en bajo stock:", bajo_stock(Nombre))
print("Productos disponibles para la venta:", disponible_venta(Nombre))
print("Clientes con deuda:", cliente_con_deuda(Nombre))
print("¿Sofía puede pagar S/5 con prepago?", alumno_puede_prepago('Sofía', 5))
print("¿Pago en efectivo de S/20 es válido para total S/18?", pago_efectivo_valido(20, 18))
print("¿Pago por transferencia de S/10 es válido si banco=15?", pago_transferencia_valido(10, 15))
print("¿Recarga prepago de S/10 es válida si caja=8 y banco=15?", recarga_prepago_valida(10, 8, 15))
print("¿Pago de deuda de S/5 es válido si deuda=8?", pago_deuda_valido(5, 8))
print("¿Compra válida a Proveedor1 de 5 unidades a S/3 cada una?", compra_valida('Proveedor1', 5, 3))
print("¿Venta válida de 2 Galletas?", venta_valida('Galleta', 2))
print("¿Venta válida de 5 Sandwich?", venta_valida('Sandwich', 5))