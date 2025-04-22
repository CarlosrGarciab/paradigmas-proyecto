import random

# Baraja con valores simplificados (el As vale 11 o 1)
palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
valores = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Crear una baraja
def crear_baraja():
    return [(valor, palo) for valor in valores for palo in palos]

# Repartir una carta
def repartir_carta(baraja):
    return baraja.pop()

# Calcular el valor de una mano
def calcular_valor(mano):
    valor_total = 0
    ases = 0
    for carta in mano:
        valor = valores[carta[0]]
        valor_total += valor
        if carta[0] == 'A':
            ases += 1
    # Ajustar ases si se pasa de 21
    while valor_total > 21 and ases:
        valor_total -= 10
        ases -= 1
    return valor_total

# Mostrar mano
def mostrar_mano(jugador, mano, ocultar_primera = False):
    print(f"{jugador} tiene:")
    for i, carta in enumerate(mano):
        if ocultar_primera and i == 0:
            print("  [Carta oculta]")
        else:
            print(f"  {carta[0]} de {carta[1]}")
    if not ocultar_primera:
        print(f"  Total: {calcular_valor(mano)}")
    print()

# Juego principal
def jugar_blackjack():
    baraja = crear_baraja()
    random.shuffle(baraja)

    jugador = [repartir_carta(baraja), repartir_carta(baraja)]
    crupier = [repartir_carta(baraja), repartir_carta(baraja)]

    mostrar_mano("Jugador", jugador)
    mostrar_mano("Crupier", crupier, ocultar_primera = True)

    # Turno del jugador
    while calcular_valor(jugador) < 21:
        accion = input("¿Querés otra carta? (s/n): ").lower()
        if accion == 's':
            jugador.append(repartir_carta(baraja))
            mostrar_mano("Jugador", jugador)
        else:
            break

    valor_jugador = calcular_valor(jugador)
    if valor_jugador > 21:
        print("¡Te pasaste! Pierdes.")
        return

    # Turno del crupier
    mostrar_mano("Crupier", crupier)
    while calcular_valor(crupier) < 17:
        print("El crupier pide otra carta...")
        crupier.append(repartir_carta(baraja))
        mostrar_mano("Crupier", crupier)

    valor_crupier = calcular_valor(crupier)

    # Resultado final
    print("Resultado final:")
    print(f"Tú: {valor_jugador} | Crupier: {valor_crupier}")
    if valor_crupier > 21 or valor_jugador > valor_crupier:
        print("¡Ganaste!")
    elif valor_jugador < valor_crupier:
        print("Perdiste.")
    else:
        print("Empate.")

# Función para volver a jugar
def jugar_otra_vez():
    while True:
        jugar_blackjack()
        otra_vez = input("¿Querés jugar otra vez? (s/n): ").lower()
        if otra_vez != 's':
            print("Cerrando Juego...")
            break

# Ejecutar el juego
jugar_otra_vez()