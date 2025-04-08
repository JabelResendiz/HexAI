
import math
from board import HexBoard
from player import Player
import random

class MCTSNode:
    def __init__(self, board: HexBoard, player_id: int, parent=None, move=None):
        self.board = board  # Estado del tablero
        self.player_id = player_id  # Jugador que moverá en este estado
        self.parent = parent
        self.move = move  # Movimiento que llevó a este nodo
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = board.get_possible_moves()


class MCTSPlayer(Player):
    def __init__(self, player_id: int, simulations: int = 500):
        super().__init__(player_id)
        self.simulations = simulations

    def play(self, board: HexBoard) -> tuple:
        root = MCTSNode(board.clone(), self.player_id)

        for _ in range(self.simulations):
            node = root
            # 1. SELECCIÓN
            while node.untried_moves == [] and node.children:
                node = self._select_child(node)

            # 2. EXPANSIÓN
            if node.untried_moves:
                node = self._expand(node)

            # 3. SIMULACIÓN
            winner = self._simulate(node.board.clone(), node.player_id)

            # 4. RETROPROPAGACIÓN
            self._backpropagate(node, winner)

        
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move


    def _select_child(self, node: MCTSNode) -> MCTSNode:
        def ucb1(child):
            if child.visits == 0:
                return float('inf')
            exploit = child.wins / child.visits
            explore = math.sqrt(math.log(node.visits) / child.visits)
            return exploit + 1.41 * explore 

        return max(node.children, key=ucb1)

    def _expand(self, node: MCTSNode) -> MCTSNode:
        move = node.untried_moves.pop()
        new_board = node.board.clone()
        new_board.place_piece(move[0], move[1], node.player_id)
        next_player = 2 if node.player_id == 1 else 1
        child = MCTSNode(new_board, next_player, parent=node, move=move)
        node.children.append(child)
        return child

    def _simulate(self, board: HexBoard, current_player: int) -> int:
        player = current_player
        while not board.check_connection(1) and not board.check_connection(2):
            moves = board.get_possible_moves()
            move = random.choice(moves)
            board.place_piece(move[0], move[1], player)
            player = 2 if player == 1 else 1
        return 1 if board.check_connection(1) else 2

    def _backpropagate(self, node: MCTSNode, winner: int):
        while node:
            node.visits += 1
            if node.player_id == winner:
                node.wins += 1
            node = node.parent




board = HexBoard(11)
player1 = MCTSPlayer(1, simulations=1000)
player2 = MCTSPlayer(2, simulations=1000)

while True:
    board.print_board()
    move1 = player1.play(board)
    board.place_piece(move1[0], move1[1], 1)
    if board.check_connection(1):
        print("Jugador 1 gana")
        break

    board.print_board()
    move2 = player2.play(board)
    board.place_piece(move2[0], move2[1], 2)
    if board.check_connection(2):
        print("Jugador 2 gana")
        break