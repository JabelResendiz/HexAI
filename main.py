import os
import time
from board import HexBoard
from player import IAPlayerBridges



board = HexBoard(size=11)



# print(board.check_connection(2))


# player = IAPlayerBridges(2)

# print(player.play(board))


# board.print_board()







def clear_console():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color):
    """Imprime texto con color en la consola."""
    colors = {"red": "\033[91m", "blue": "\033[94m", "reset": "\033[0m"}
    return f"{colors[color]}{text}{colors['reset']}"

def get_human_move(board: HexBoard):
    """Solicita y valida un movimiento del jugador humano."""
    while True:
        move_input = input("\nIngrese su movimiento (fila columna): ")
        try:
            row, col = map(int, move_input.split())
            row -= 1
            col -= 1
            if board.is_valid_move(row, col):
                return row, col
            else:
                print(print_colored("❌ Movimiento no válido o casilla ocupada. Inténtelo de nuevo.", "red"))
        except ValueError:
            print(print_colored("❌ Entrada inválida. Formato correcto: fila columna (ejemplo: 2 3)", "red"))

# Inicialización del jugador IA
player_objects = {
    1: None,                      # Humano
    2: IAPlayerBridges(2)         # Inteligencia artificial
}

current_player = 1
player_moves = {1: [], 2: []}

try:
    while True:
        clear_console()
        board.print_board()

        if board.check_connection(1):
            print(print_colored("\n🏆 ¡El jugador 1 (🔴) ha ganado!", "red"))
            break
        if board.check_connection(2):
            print(print_colored("\n🏆 ¡El jugador 2 (🔵) ha ganado!", "blue"))
            break
        if not board.get_possible_moves():
            print(print_colored("\n🤝 Empate. No hay más movimientos disponibles.", "blue"))
            break

        print(f"\nTurno del jugador {current_player} ({'🔴' if current_player == 1 else '🔵'})")

        if player_objects[current_player] is None:
            # Turno del jugador humano
            row, col = get_human_move(board)
            board.place_piece(row, col, current_player)
            print(print_colored(f"\n✅ Jugada del jugador humano en ({row+1}, {col+1})", "blue"))
            player_moves[current_player].append((row+1, col+1))  # Guardar en formato 1-indexado
            time.sleep(1)
        else:
            # Turno de la IA
            print("🤖 Pensando...")
            time.sleep(0.5)
            row, col = player_objects[current_player].play(board)
            board.place_piece(row, col, current_player)
            print(print_colored(f"\n🤖 La IA jugó en ({row+1}, {col+1})", "red"))
            player_moves[current_player].append((row+1, col+1))  # Guardar en formato 1-indexado
            time.sleep(1)

        current_player = 3 - current_player  # Cambiar de jugador

except KeyboardInterrupt:
    print(print_colored("\n\n⛔ Juego interrumpido por el usuario (Ctrl + C)", "red"))

finally:
    # Mostrar árbol padre si quieres depuración (opcional)
    # print(board.pc.parent)  # Comenta si no usas Union-Find o PC

    with open("jugadas_hex.txt", "w", encoding="utf-8") as file:
        for player_id in [1, 2]:
            color = '🔴' if player_id == 1 else '🔵'
            file.write(f"Jugador {player_id} ({color}):\n")
            for move in player_moves[player_id]:
                file.write(f"  -> {move}\n")
            file.write("\n")

    print(print_colored("📝 Jugadas guardadas en 'jugadas_hex.txt'", "blue"))
