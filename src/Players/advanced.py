
from board import HexBoard
from player import Player
import random

class IAPlayerAdvanced(Player):
    def __init__(self,player_id:int):
        super().__init__(player_id)
    
    def play(self,board: HexBoard)-> tuple:

        possible_moves = board.get_possible_moves()

        return random.choice(possible_moves) if possible_moves else None
            
            
    def heuristic(self,board: HexBoard)-> int:

        "Heuristica que compara el tamano del grupo mas grande de cada jugador"

        max_size_player1 =0
        max_size_player2 =0

        for cell in board.player_positions[1]:
            root = board.find(cell)
            current_size = board.size_uf[root]
            max_size_player1 = max(current_size,max_size_player1)
        
        for cell in board.player_positions[2]:
            root = board.find(cell)
            current_size = board.size_uf[root]
            max_size_player2 = max(max_size_player2,current_size)
        
        return max_size_player1 - max_size_player2
    

    def heuristic_with_bonus(self, board: HexBoard) -> int:
        max_size_p1, max_size_p2 = 0, 0

    # Calcula el grupo más grande para cada jugador
        for player in [1, 2]:
            max_size = 0
            for cell in board.player_positions[player]:
                root = board.find(cell)
                max_size = max(board.size_uf[root], max_size)
        
            if player == 1:
                max_size_p1 = max_size
            else:
                max_size_p2 = max_size

    # Bonificación por conexión a bordes
        bonus_p1 = 100 if board.check_connection(1) else 0
        bonus_p2 = 100 if board.check_connection(2) else 0

        return (max_size_p1 + bonus_p1) - (max_size_p2 + bonus_p2)
        
