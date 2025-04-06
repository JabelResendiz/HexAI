from board import HexBoard
from player import Player
import random

class IAPlayerRandom(Player):
    def __init__(self,player_id:int):
        super().__init__(player_id)
    
    def play(self,board: HexBoard)-> tuple:

        possible_moves = board.get_possible_moves()

        return random.choice(possible_moves) if possible_moves else None
            
            
    

