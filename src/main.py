import os
import time
from board import HexBoard
from player import IAPlayer

def clear_console():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color):
    """Imprime texto con color en la consola."""
    colors = {"red": "\033[91m", "blue": "\033[94m", "reset": "\033[0m"}
    return f"{colors[color]}{text}{colors['reset']}"

def print_board(board):
    """Imprime el tablero en un formato visual mejorado."""
    size = board.size
    print("\n   " + " ".join([str(i) for i in range(size)]))  # Números de columna
    for i, row in enumerate(board.board):
        print(" " * i, end="")  # Indentación para el formato hexagonal
        print(str(i) + " ", end="")  # Número de fila
        for cell in row:
            if cell == 1:
                print(print_colored("🔴", "red"), end=" ")
            elif cell == 2:
                print(print_colored("🔵", "blue"), end=" ")
            else:
                print("⬡", end=" ")  # Hexágono vacío
        print()

def get_human_move(board):
    """Solicita y valida un movimiento del jugador humano."""
    while True:
        move_input = input("\nIngrese su movimiento (fila columna): ")
        try:
            row, col = map(int, move_input.split())
            if (row, col) in board.get_possible_moves():
                return row, col
            else:
                print(print_colored("❌ Movimiento no válido o casilla ocupada. Inténtelo de nuevo.", "red"))
        except ValueError:
            print(print_colored("❌ Entrada inválida. Formato correcto: fila columna (ejemplo: 2 3)", "red"))

def main():
    clear_console()
    print(print_colored("🎮 Bienvenido a HEX 🎮", "blue"))

    try:
        size = int(input("\nIngrese el tamaño del tablero (ejemplo: 5): "))
    except ValueError:
        print(print_colored("⚠️ Tamaño inválido. Usando tamaño por defecto: 5", "red"))
        size = 5

    board = HexBoard(size)

    print("\nModos de juego:")
    print("1️⃣ - Humano vs Humano")
    print("2️⃣ - Humano vs IA")
    print("3️⃣ - IA vs IA")
    mode = input("\nSeleccione modo de juego (1, 2 o 3): ")

    player_objects = {1: None, 2: None}

    if mode == "2":
        human_player = int(input("\nElija su identificador (1 para 🔴, 2 para 🔵): "))
        ai_player = 2 if human_player == 1 else 1
        player_objects[ai_player] = IAPlayer(ai_player)
    elif mode == "3":
        player_objects = {1: IAPlayer(1), 2: IAPlayer(2)}

    current_player = 1

    while True:
        clear_console()
        print_board(board)

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
            row, col = get_human_move(board)
        else:
            time.sleep(.5)  # Para que la IA no juegue instantáneamente
            row, col = player_objects[current_player].play(board)
            print(f"🤖 La IA juega en la posición: ({row}, {col})")

        board.place_piece(row, col, current_player)
        current_player = 2 if current_player == 1 else 1

    print("\nFin del juego 🎉")

if __name__ == "__main__":
    main()
