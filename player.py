from board import HexBoard
from player import Player
import random


class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    

class IAPlayerBridges(Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.vector_move_bridges = [(-1, 2), (-1, -1), (-2, 1),
                                    (1, -2), (1, 1), (2, -1)]

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
            mid = board.size // 2
            return (mid, mid)

        if not board.player_positions[self.player_id]:
            r = random.choice(board.get_possible_moves())

            if self.player_id ==1 and r[1] <=1:
                self.is_minimo = False
            elif self.player_id ==2 and r[0] <=1:
                self.is_minimo = False

            if self.player_id == 1 and r[1] < board.size-2:
                if r[1] > board.size - r[1]:
                    self.is_minimo = False
            elif self.player_id == 2 and r[0] < board.size -2:
                if r[0] > board.size - r[0]:
                    self.is_minimo = False

            return r
        
        move = self.heurisitic_bridges(board, board.last_move)
        print(move)

        return move


    




    def heurisitic_bridges(self, board: HexBoard, last_move_adv: tuple) -> tuple:
        """Heurística basada en patrones de puentes y contrarrestar jugadas del adversario."""
        possible_moves = board.get_possible_moves()
        player_moves = board.player_positions[self.player_id]
        print(last_move_adv)
        for v_second, v_first, v_out in self.bridge_patterns:
            result = self.coord_heuristic(last_move_adv, player_moves, v_second, v_first, v_out, board.size)
            if result and result in possible_moves:
                return result


        if board.min_stones_to_connect(self.player_id,board.directions + board.vector_move_bridges) == 0:


            cell = board.get_one_empty_cell_in_connection_path(self.player_id)

            return cell
            
            
        return self.best_move_dijkstra(self.player_id,board.directions + board.vector_move_bridges, board)



    def coord_heuristic(self, move: tuple, player_moves: set, v_second: tuple, v_first: tuple, v_out: tuple, size: int) -> tuple:
        
        
        f = (move[0] - v_first[0], move[1] - v_first[1])
        s = (f[0] + v_second[0], f[1] + v_second[1])
        o = (f[0] + v_out[0], f[1] + v_out[1])

        if (0 <= o[0] < size and 0 <= o[1] < size
                and f in player_moves and (s in player_moves or 
                (self.player_id == 1 and (s[1] == -1 or s[1] == size)) or
                (self.player_id == 2 and (s[0] == -1 or s[0] == size)))):
            return o
        return None


    

    def best_move_dijkstra(self, player_id, directions,board:HexBoard) -> tuple:
        R, C = board.size, board.size

        # 1. Obtener las posiciones actuales del jugador
        current_positions = board.player_positions[player_id]

        # 2. Candidatas a probar: todas las posiciones vacías adyacentes (o por puente) a mis fichas
        candidates = set()
        for x, y in current_positions:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (board.is_on_board((nx,ny))):
                    continue

                if board.board[nx][ny] == 0:
                    if (dx, dy) in self.vector_move_bridges:
                        # Verificar si es un puente válido
                        for vec_bridge, inter1, inter2 in self.bridge_patterns:
                            if vec_bridge == (dx, dy):
                                inter1_pos = (x + inter1[0], y + inter1[1])
                                inter2_pos = (x + inter2[0], y + inter2[1])
                                if (board.is_valid_move(inter1_pos[0],inter1_pos[1]) and 
                                    board.is_valid_move(inter2_pos[0],inter2_pos[1])):

                                    candidates.add((nx, ny))
                                break
                    else:
                        candidates.add((nx, ny))

        # 4. Probar cada jugada candidata
        best_move = None
        min_cost = float("inf")


        if self.player_id == 2:
            if self.is_minimo:
                end_nodes = [(0, i) for i in range(board.size)]
            else:
                end_nodes =[(board.size-1, i) for i in range(board.size)]

        else:
            if self.is_minimo:
                end_nodes = [(i, 0) for i in range(board.size)]
            else :
                end_nodes = [(i, board.size-1) for i in range(board.size)]


        for cx, cy in candidates:
            # Simular jugada
            board.board[cx][cy] = player_id

            start_nodes = current_positions | {(cx, cy)} 
            
            # Calcular costo mínimo desde borde de entrada hasta borde de salida
            cost = board.min_cost_between_sets(start_nodes,
                                               end_nodes,
                                               self.player_id,
                                               board.directions + board.vector_move_bridges,
                                               board.player_positions[3-self.player_id])

            # Deshacer jugada
            board.board[cx][cy] = 0

            if cost != -1 and cost < min_cost:
                min_cost = cost
                best_move = (cx, cy)

        
        if self.player_id == 1 :
            if best_move[1] == 0:
                self.is_minimo = False
            elif best_move[1] == 1 and board.is_valid_move(best_move[0],0) and board.is_valid_move(best_move[0]+1,0):
                self.is_minimo = False
            
            elif best_move[1] == board.size -1:
                self.is_minimo = True
            elif best_move[1] == board.size -2 and board.is_valid_move(best_move[0],board.size-1) and board.is_valid_move(best_move[0]-1,board.size-1):
                self.is_minimo = True
        
        elif self.player_id == 2 :
            if best_move[0] == 0:
                self.is_minimo = False
            elif best_move[0] == 1 and board.is_valid_move(0,best_move[1]) and board.is_valid_move(0,best_move[1]+1):
                self.is_minimo = False

            elif best_move[0] == board.size-1:
                self.is_minimo = True
            elif best_move[0] == board.size-2 and board.is_valid_move(board.size-1,best_move[1]) and board.is_valid_move(board.size-1,best_move[1]-1):
                self.is_minimo = True
              
        return best_move



