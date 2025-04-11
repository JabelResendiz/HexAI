
from board import HexBoard
from player import Player
import math
import random

class IAPlayerBridges(Player):

    def __init__(self,player_id):
        super().__init__(player_id)
        self.vector_move_bridges = [(-1,2), (-1,-1), (-2,1),
                                    (1,-2), (1,1), (2,-1)]
        
        
        self.bridge_patterns = [
            ((-1, 2), (0, 1), (-1, 1)),
            ((-1, -1), (0, -1), (-1, 0)),
            ((-2, 1), (-1, 0), (-1, 1)),
            ((1, -2), (0, -1), (1, -1)),
            ((1, 1), (0, 1), (1, 0)),
            ((2, -1), (1, -1), (1, 0)),
            ((-1, 2), (-1, 1), (0, 1)),
            ((-1, -1), (-1, 0), (0, -1)),
            ((-2, 1), (-1, 1), (-1, 0)),
            ((1, -2), (1, -1), (0, -1)),
            ((1, 1), (1, 0), (0, 1)),
            ((2, -1), (1, 0), (1, -1)),
        ]

        self.is_minimo = True
    
    

    def play(self, board: HexBoard) -> tuple:
        
        if board.last_move is None:
            mid = math.ceil(board.size/2)
            return (mid,mid)

        move = self.heurisitic_bridges(board,board.last_move)

        return move
        


    def coord_heuristic(self, move: tuple, player_moves: set, v_second: tuple, v_first: tuple, v_out: tuple,size :int) -> tuple:
        f = (move[0] - v_first[0], move[1] - v_first[1])
        s = (f[0] + v_second[0], f[1] + v_second[1])
        o = (f[0] + v_out[0], f[1] + v_out[1])


        if (0 <= o[0] < size and 0 <= o[1] < size
            and f in player_moves and (s in player_moves or (self.player_id == 1 and (s[1]==0 or s[1]== size))
                                                         or  (self.player_id == 2 and (s[0]==0 or s[0]==size)))):
            return o
        
        return None
    
    def make_move(self,board:HexBoard,path:list) -> tuple:
        
        for i in range(len(path)):

            nr,nc = path[i]

            #print((nr,nc))
            if (self.player_id == 1 and nc ==0) or (self.player_id ==2 and nr ==0):
                continue
            if (self.player_id == 1 and nc == board.size-1)  or (self.player_id == 2 and nr == board.size-1):
                continue

            if self.player_id == 1 and nc == 1:
                return (nr,0)

            if self.player_id == 2 and nr ==1:
                return (0,nc)
            
            if self.player_id == 1 and nc == board.size-2:
                return (nr,nc+1)

            if self.player_id == 2 and nr ==board.size-2:
                return (nr+1,nc)
            
            # 2dos vertices

            nr1,nc1 = path[i-1]

            hommies = board.search_all_hommies((nr,nc))

            #print(f"Los hommies de ({nr},{nc}) son: {hommies}")

            for u in hommies:
                dx = u[0] - nr1
                dy = u[1] - nc1
                
                #print(dx,dy)
                
                for bridge_vec, neighbor1, neighbor2 in self.bridge_patterns:
                    if (dx, dy) == bridge_vec:
                        n1 = (nr1 + neighbor1[0], nc1 + neighbor1[1])
                        n2 = (nr1 + neighbor2[0], nc1 + neighbor2[1])

                        #print(n1,n2)

                        if (board.is_on_board(n1) and board.board[n1[0]][n1[1]] == 0):
                            return n1  
                        if (board.is_on_board(n2) and board.board[n2[0]][n2[1]] == 0):
                            return n2
            

    def search_best_path(self,board:HexBoard) -> tuple:

        value_min = board.size +1
        value_max = - value_min
        my_bridges = board.player_positions[self.player_id]

        # si no esta vacio busco una jugada aleatoria para jugar 
        if not my_bridges:
            return random.choice(board.get_possible_moves())
        

        for (r,c) in my_bridges:
            for bridge_vec, neighbor1, neighbor2 in self.bridge_patterns:
                dx = (r+ bridge_vec[0], c + bridge_vec[1])
                n1 = (r + neighbor1[0], c+neighbor1[1])
                n2  = (r+neighbor2[0], c + neighbor2[1])

                if  (board.is_on_board(dx) and board.is_on_board(n1) and board.is_on_board(n2)
                    and board.board[dx[0]][dx[1]] == 0 and
                        board.board[n1[0]][n1[1]] == 0 and
                        board.board[n2[0]][n2[1]] == 0):
                     
                    if self.is_minimo:
                         
                        if self.player_id == 1 and dx[1] < value_min:
                            value_min = dx[1]
                            move = dx
                        
                        elif self.player_id == 2 and dx[0] <value_min:
                            value_min = dx[0]
                            move = dx
                    
                    else: # es de maximizar

                        if self.player_id  == 1 and dx[1] > value_max:
                            value_max = dx[1]
                            move = dx

                        elif self.player_id ==2 and dx[0] > value_max:
                            value_max = dx[0]
                            move = dx  

        if self.player_id == 1 and move[1] <=1:
            self.is_minimo = False
        elif self.player_id == 2 and move[0] <=1:
            self.is_minimo = False

        return move
        

        


    def heurisitic_bridges(self, board: HexBoard, last_move_adv: tuple) -> tuple:
        """Mi heuristica es inspecccionar solamente de mis nodos
        los puentes que pueda construir y si el jugador contrario me jugo en un paso entre puente
        jugarle a contrarrestar la jugada hecha"""

        possible_moves = board.get_possible_moves()

    
        player_moves = board.player_positions[self.player_id]

        

        for v_second, v_first, v_out in self.bridge_patterns:
            result = self.coord_heuristic(last_move_adv, player_moves, v_second, v_first, v_out, board.size)
            if result and result in possible_moves:
                return result

        #print(898989898)
        # comprobar si ya tenemos el camino de puentes usando el path compresion
        if board.check_bridges_pattern(self.player_id):
            
           # print(898989898)

            bfs = board.bfs(self.player_id)
            #print(bfs)
            
            return self.make_move(board,bfs)
        

        return self.search_best_path(board)
            # print("El path es :" ,path)
            # return self.make_move(board,path)
        
        # en caso de que no tengamos el camino completo entonces debemos jugar a buscar el mejor camino

        
        


        
            
        