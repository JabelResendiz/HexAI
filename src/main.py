import os
import time
from board import HexBoard,Graph
from bridges import IAPlayerBridges

# from player import IAPlayer

board = HexBoard(size=11)

    # Prueba básica: colocar fichas para el jugador 1
# board.place_piece(0, 0, 1)
# board.place_piece(0, 1, 1)
# board.place_piece(0, 2, 1)
# board.place_piece(0, 3, 1)
# board.place_piece(0, 4, 1)

board.place_piece(1,3,1)
board.place_piece(2,2,1)
board.place_piece(3,0,1)

board.place_piece(0,5,1)
board.place_piece(3,3,1)
board.place_piece(1,5,1)
board.place_piece(4,4,1)
board.place_piece(3,6,1)
board.place_piece(1,6,1)
board.place_piece(1,7,1)

board.place_piece(2,8,1)
board.place_piece(1,10,1)
board.print_board()

print("¿Jugador 1 conectó izquierda a derecha?")
print(board.check_connection(1))  # Esperamos True si conectó

print("¿Jugador 1 conectó mediante puente?")
print(board.check_bridges_pattern(1))  # También puedes probar esto

g= Graph(board.parent,board,board.bridge_parent)

print(g.process_path(1))


#print(board.parent)

# v = board.find("LEFT")
# w = board.find("RIGHT")
# start_edge = {node for node in board.parent if board.parent[node] == v}
# target_edge = {node for node in board.parent if board.parent[node] == w}

# print(start_edge)
# print(target_edge)



# def clear_console():
#     """Limpia la pantalla de la consola."""
#     os.system('cls' if os.name == 'nt' else 'clear')

# def print_colored(text, color):
#     """Imprime texto con color en la consola."""
#     colors = {"red": "\033[91m", "blue": "\033[94m", "reset": "\033[0m"}
#     return f"{colors[color]}{text}{colors['reset']}"


# def get_human_move(board):
#     """Solicita y valida un movimiento del jugador humano."""
#     while True:
#         move_input = input("\nIngrese su movimiento (fila columna): ")
#         try:
#             row, col = map(int, move_input.split())
#             if (row, col) in board.get_possible_moves():
#                 return row, col
#             else:
#                 print(print_colored("❌ Movimiento no válido o casilla ocupada. Inténtelo de nuevo.", "red"))
#         except ValueError:
#             print(print_colored("❌ Entrada inválida. Formato correcto: fila columna (ejemplo: 2 3)", "red"))



# player_objects = { 1: IAPlayerBridges(1), 2:None}

# current_player =2

# while True:
#     clear_console()
#     board.print_board()

#     if board.check_connection(1):
#         print(print_colored("\n🏆 ¡El jugador 1 (🔴) ha ganado!", "red"))
#         break
#     if board.check_connection(2):
#         print(print_colored("\n🏆 ¡El jugador 2 (🔵) ha ganado!", "blue"))
#         break
#     if not board.get_possible_moves():
#         print(print_colored("\n🤝 Empate. No hay más movimientos disponibles.", "blue"))
#         break

#     print(f"\nTurno del jugador {current_player} ({'🔴' if current_player == 1 else '🔵'})")

#     if player_objects[current_player] is None:
#         # Turno del jugador humano
#         row, col = get_human_move(board)
#         board.place_piece(row, col, current_player)

#         # Mostrar el tablero después de la jugada humana
#         clear_console()
#         board.print_board()
#         print(print_colored(f"\n✅ Jugada del jugador humano en ({row}, {col})", "blue"))
#         time.sleep(1.5)  # Pausa para que el jugador vea la jugada antes de que la IA responda

#     else:
#         # Turno de la IA
#         print("🤖 Pensando...")
#         time.sleep(0.5)
#         row, col = player_objects[current_player].play(board)
#         board.place_piece(row, col, current_player)

#         # Mostrar el tablero después de la jugada de la IA
#         #
        
#         print(print_colored(f"\n🤖 La IA jugó en ({row}, {col})", "red"))
#         time.sleep(10.5)  # Pausa para que el humano vea la jugada
#         clear_console()
#         board.print_board()

#     # Cambiar de jugador
#     current_player = 3 - current_player

    

