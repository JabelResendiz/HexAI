from board import HexBoard
import random

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
class IAPlayer(Player):
    def __init__(self,player_id:int):
        super().__init__(player_id)
    
    # def play(self,board: HexBoard)-> tuple:
    #     """Seleccionar la mejor jugada usando una heuristica"""

    #     possible_moves = board.get_possible_moves()

    #     return random.choice(possible_moves) if possible_moves else None

    def play(self,board: HexBoard)-> tuple:

        possible_moves = board.get_possible_moves()

        max_move = -(board.size * board.size+1)

        move = None

        for row,column in possible_moves:
            clone = board.clone()
            clone.board[row][column] = self.player_id

            value = self.heuristic(clone)

            if max_move < value:
                move= (row,column)
                max_move=value
        
        return move
            
            
    
    def heuristic(self,board:HexBoard) -> float:
        """Funcion de evaluacion heuristica del tablero"""

        function =0 
        for row in range(board.size):
            for column in range(board.size):
                function = function + (
                            1 if (board.board[row][column] == self.player_id)
                            else 0 if board.board[row][column]==0 else -1)
        
        return function
    

    

    
        
