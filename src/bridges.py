
from board import HexBoard,Graph
from player import Player
import math

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
    
    

    def play(self, board: HexBoard) -> tuple:
        
        if board.last_move is None:
            mid = math.ceil(board.size/2)
            return (mid,mid)

        move = self.heurisitic_bridges(board,board.last_move)
        #print(move)
        return move
        


    def coord_heuristic(self, move: tuple, player_moves: set, v_second: tuple, v_first: tuple, v_out: tuple,size :int) -> tuple:
        f = (move[0] - v_first[0], move[1] - v_first[1])
        s = (f[0] + v_second[0], f[1] + v_second[1])
        o = (f[0] + v_out[0], f[1] + v_out[1])

        # print(f)
        # print(s)
        # print(o)

        if (0 <= o[0] < size and 0 <= o[1] < size
            and f in player_moves and s in player_moves):
            #print(89898989)
            return o
        #print(78787878787)
        return None
    
    def make_move(self,board:HexBoard,path) -> tuple:
        
        
        for i in range(len(path)):
            nr,nc = path[i]
            
            if self.player_id==2 and nr == 0:
                continue
            elif self.player_id ==1 and nc ==0:
                continue
            
            if self.player_id == 1 and nc ==1:
                if board.is_on_board((nr,0)) and board.board[nr][0] ==2:
                    continue
                if board.is_on_board((nr+1,0)) and board.board[nr+1][0] ==2:
                    continue

                return (nr,0)
            
            elif self.player_id == 2 and nr == 1:
                if board.is_on_board((0,nc)) and board.board[0][nc] ==2:
                    continue
                if board.is_on_board((0,nc+1)) and board.board[0][nc+1] ==2:
                    continue

                return (0,nc)
            

            if self.player_id == 1 and nc == board.size-1:
                continue
            elif self.player_id == 2 and nr == board.size -1:
                continue
            
            if self.player_id == 1 and nc == board.size-2:
                if board.is_on_board((nr,board.size-1)) and board.board[nr][board.size-1] ==2:
                    continue
                if board.is_on_board((nr-1,board.size-1)) and board.board[nr-1][board.size-1] ==2:
                    continue

                return (nr,board.size-1)
            
            elif self.player_id == 2 and nr == board.size-2:
                if board.is_on_board((board.size-1,nc)) and board.board[board.size-1][nc] ==2:
                    continue
                if board.is_on_board((board.size-1,nc-1)) and board.board[ board.size-1][nc-1] ==2:
                    continue

                return (board.size-1,nc)

            nr1,nc1 = path[i-1]

            f,v = nr1-nr,nc1-nc

            

            for pattern in self.bridge_patterns:
                bridge_vec, neighbor1, neighbor2 = pattern
                if (f, v) == bridge_vec:
                    break
            
            if board.board[nr+neighbor1[0]][nc+neighbor1[1]] == 2 or board.board[nr+neighbor2[0]][nc+neighbor2[1]] ==2 :
                continue
            
            else:
                return (nr+neighbor1[0], nc+ neighbor1[1])
            

                        

            

            



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
            graph = Graph(board.parent,board.bridge_parent)

            bfs = graph.bfs(self.player_id)

            
            return self.make_move(board,bfs)
            # print("El path es :" ,path)
            # return self.make_move(board,path)
        
        return None
        # en caso de que no tengamos el camino completo entonces debemos jugar a buscar el mejor camino

        
        


        
            
        