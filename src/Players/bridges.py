
from board import HexBoard
from player import Player
from collections import deque
import random


class IAPlayerBridges(Player):

    def __init__(self,player_id):
        super().__init__(player_id)
        self.vector_move_bridges = [(-1,2), (-1,-1), (-2,1),
                                    (1,-2), (1,1), (2,-1)]
        
        self.opponent_last_move = None
    
    def set_opponent_last_move(self,move: tuple):
        self.opponent_last_move = move

    def play(self, board: HexBoard) -> tuple:
        
        if self.oponent_last_move:

            blocking_move = self.check_bridges_pattern(board)
    

    def check_bridges_pattern(self,board:HexBoard):
        x,y = self.opponent_last_move

        opponent_id = 3- self.player_id

        bridges_pattern =[

            ((x-1,y+1),[(x,y),(x-1,y+2)]),
            
        ]

        for (block_pos, required_positions) in bridges_pattern:

            if (0<= block_pos[0] < board.size and 0<= block_pos[1] < board.size) and 
                (board.board[block_pos[0]][block_pos[1]] == 0):

                all_opponent = True

                for pos in required_positions:
                    if not (0<= pos[0] <board.size and 0<= pos[1]< board.size and board.board[pos[0]][pos[1]]==opponent_id):
                        all_opponent = False
                        break
                
                if all_opponent:
                    return block_pos
                
        return None

    

            
    def coord_heuristic(self,move: tuple, jugadas, v_second:tuple, v_first:tuple,v_salida:tuple) -> tuple:

        f = move - v_first
        s = f + v_second
        o = f + v_salida

        condition1= f in jugadas
        condition2 = s in jugadas

        if condition1 and condition2:
            return o
        
        return False
        

    def heurisitic_bridges(self, board: HexBoard, last_move_adv: tuple) -> tuple:
        """Mi heuristica es inspecccionar solamente de mis nodos
        los puentes que pueda construir y si el jugador contrario me jugo en un paso entre puente
        jugarle a contrarrestar la jugada hecha"""

        possible_moves = board.get_possible_moves()
        jugadas= board.player_positions(self.player_id)

        # buscar si la utlima jugada del adversario mi intersecta un puente
        
        if self.coord_heuristic(last_move_adv,jugadas,(-1,2),(0,1),(-1,1)):
            return self.coord_heuristic(last_move_adv,jugadas,(-1,2),(0,1),(-1,1))
        
        if self.coord_heuristic(last_move_adv,jugadas,(-1,-1),(0,-1),(-1,0)):
            return self.coord_heuristic(last_move_adv,jugadas,(-1,-1),(0,-1),(-1,0))
        
        if self.coord_heuristic(last_move_adv,jugadas,(-2,1),(-1,0),(-1,1)):
            return self.coord_heuristic(last_move_adv,jugadas,(-2,1),(-1,0),(-1,1))
        if self.coord_heuristic(last_move_adv,jugadas,(1,-2),(0,-1),(1,-1)):
            return self.coord_heuristic(last_move_adv,jugadas,(1,-2),(0,-1),(1,-1))
        if self.coord_heuristic(last_move_adv,jugadas,(1,1),(0,1),(1,0)):
            return self.coord_heuristic(last_move_adv,jugadas,(1,1),(0,1),(1,0))
        if self.coord_heuristic(last_move_adv,jugadas,(2,-1),(1,-1),(1,0)):
            return self.coord_heuristic(last_move_adv,jugadas,(2,-1),(1,-1),(1,0))
        
        


        if self.coord_heuristic(last_move_adv,jugadas,(-1,2),(-1,1),(0,1)):
            return self.coord_heuristic(last_move_adv,jugadas,(-1,2),(-1,1),(0,1))
        
        if self.coord_heuristic(last_move_adv,jugadas,(-1,-1),(-1,0),(0,-1)):
            return self.coord_heuristic(last_move_adv,jugadas,(-1,-1),(-1,0),(0,-1))
        
        if self.coord_heuristic(last_move_adv,jugadas,(-2,1),(-1,1),(-1,0)):
            return self.coord_heuristic(last_move_adv,jugadas,(-2,1),(-1,1),(-1,0))
        if self.coord_heuristic(last_move_adv,jugadas,(1,-2),(1,-1),(0,-1)):
            return self.coord_heuristic(last_move_adv,jugadas,(1,-2),(1,-1),(0,-1))
        if self.coord_heuristic(last_move_adv,jugadas,(1,1),(1,0),(0,1)):
            return self.coord_heuristic(last_move_adv,jugadas,(1,1),(1,0),(0,1))
        if self.coord_heuristic(last_move_adv,jugadas,(2,-1),(1,0),(1,-1)):
            return self.coord_heuristic(last_move_adv,jugadas,(2,-1),(1,0),(1,-1))
        


        # comprobar si ya tenemos el camino de puentes usando el path compresion

        # en caso de que no tengamos el camino completo entonces debemos jugar a buscar el mejor camino

        # en caso de de si tengamos el camino completo procedemos a unir los puentes que no estan unidos




        
            
        