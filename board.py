import numpy as np
from collections import deque
import heapq
import copy

class HexBoard:
    def __init__(self, size: int):

        self.size = size  # Tamaño N del tablero (NxN)
        self.board=  np.zeros((size,size), dtype = int)
        self.player_positions = {1: set(), 2: set()} 

        self.last_move = None

        self.pc = PathCompresion(size)

        self.state_stack = []

        self.state_stack = [(self.pc, (-1, -1))]  

        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]

        self.vector_move_bridges = [(-1, 2), (-1, -1), (-2, 1),(1, -2), (1, 1), (2, -1)]

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

        for row in range(size):
            for col in range(size):
                self.pc.parent[(row,col)] = (row,col)
                self.pc.size[(row,col)] = 1

                self.pc.bridge_parent[(row, col)] = (row, col)
                self.pc.bridge_size[(row, col)] = 1


        self.virtual_nodes = {
            1:("LEFT","RIGHT"),
            2:("TOP","BOTTOM")
        }

        for node in ["LEFT","RIGHT","TOP","BOTTOM"]:
            self.pc.parent[node] = node
            self.pc.size[node] =1

            self.pc.bridge_parent[node] = node
            self.pc.bridge_size[node] = 1
        
    

    def clone(self,row,col,player_id):

        new_pc = self.pc.clone()

        self.place_piece(row,col,player_id,new_pc)

        self.state_stack.append((new_pc,(row,col)))

        self.pc = new_pc
    

    def is_on_board(self,cell:tuple) -> bool:
        "Comprobar si una celda esta en mi tablero"
        r,c = cell
        return 0<= r < self.size and 0<= c < self.size
    
    def is_valid_move(self,move0,move1) -> bool:
        
        return self.is_on_board((move0,move1)) and self.board[move0][move1] == 0
    


    def place_piece(self, row: int, col: int, player_id: int, place_piece : 'PathCompresion' = None) -> bool:
        """Coloca una ficha si la casilla está vacía."""
        if place_piece is None:
            place_piece = self.pc
        
        if not self.is_on_board((row,col)):

            return False
    
        if self.board[row][col] !=0:

            return False
        
        self.last_move = (row,col)
        self.board[row][col] = player_id
        self.player_positions[player_id].add((row,col))

        
        for dr, dc in self.directions:
            nr, nc = row + dr, col + dc
            if self.is_on_board((nr,nc)) and self.board[nr][nc] == player_id:
                place_piece.union((row, col), (nr, nc))
                place_piece.union((row, col),  (nr, nc), True)
                #print(787878)
        
        
        # Conectar con mis nodos virtuales si estan en los bordes

        if player_id ==1:
            if col ==0:
               place_piece.union((row,col),"LEFT")
               place_piece.union((row,col),"LEFT", True)
            if col == self.size -1:
                place_piece.union((row,col),"RIGHT")
                place_piece.union((row,col),"RIGHT", True)
        
        else :
            if row ==0:
                place_piece.union((row,col),"TOP")
                place_piece.union((row,col),"TOP", True)
            if row == self.size -1:
                place_piece.union((row,col),"BOTTOM")
                place_piece.union((row,col),"BOTTOM", True)

        

        for bridge_vec, neighbor1, neighbor2 in self.bridge_patterns:
            nr,nc = row + bridge_vec[0] , col + bridge_vec[1]
            n11,n12 = row + neighbor1[0], col + neighbor1[1]
            n21, n22 = row + neighbor2[0], col + neighbor2[1]

            if (self.is_on_board((nr,nc)) and self.board[nr][nc] == player_id and 
                self.is_on_board((n11,n12)) and self.board[n11][n12] == 0 and
                self.is_on_board((n21,n22)) and self.board[n21][n22] == 0):

                place_piece.union((row,col) , (nr,nc) , True)
        
        if player_id ==1:
            if col == 1:
                place_piece.union((row,col),"LEFT", True)
            if col == self.size -2:
                place_piece.union((row,col),"RIGHT", True)
        
        else :
            if row ==1:
                place_piece.union((row,col),"TOP", True)
            if row == self.size -2:
                place_piece.union((row,col),"BOTTOM", True)

        return True


    def get_possible_moves(self) -> list:
        """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
        return [(row,col) 
                for row in range(self.size) 
                    for col in range(self.size) 
                        if self.board[row][col]==0
                ]

        # for row in range(self.size):
        #     for col in range(self.size):
        #         if self.board[row][col] == 0:
        #             yield (row,col)
    
    def check_connection(self, player_id: int) -> bool:
        """Verifica si el jugador ha conectado sus dos lados"""
        

        v1,v2 = self.virtual_nodes[player_id]

        return self.pc.find(v1) == self.pc.find(v2)
    
    
    

    def check_bridges_pattern(self,player_id:int) -> bool:
        
        """Verifica si existe un camino de puentes entre los lados del jugador"""
        v1,v2 = self.virtual_nodes[player_id]

        return self.pc.find(v1,True) == self.pc.find(v2,True)

    
    def min_cost_between_sets(self, start_nodes, end_nodes, player_id, directions):
        """
        Encuentra el costo mínimo de conectar un nodo de start_nodes a uno de end_nodes
        usando movimientos válidos (incluyendo puentes).
        """
        R, C = self.size, self.size
        dist = {}
        heap = []

        for x, y in start_nodes:
            if self.board[x][y] == player_id:
                cost = 0
            elif self.board[x][y] == 0:
                cost = 1
            else:
                continue  # no empieces desde una celda enemiga
            dist[(x, y)] = cost
            heapq.heappush(heap, (cost, (x, y)))

        end_nodes_set = set(end_nodes)

        while heap:
            cost, (x, y) = heapq.heappop(heap)

            if (x, y) in end_nodes_set:
                return cost  # ya llegaste a algún nodo final

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < R and 0 <= ny < C):
                    continue

                # Validación de puente
                if (dx, dy) in self.vector_move_bridges:
                    for vec_bridge, inter1, inter2 in self.bridge_patterns:
                        if vec_bridge == (dx, dy):
                            inter1_pos = (x + inter1[0], y + inter1[1])
                            inter2_pos = (x + inter2[0], y + inter2[1])

                            if (self.is_on_board(inter1_pos) and self.is_on_board(inter2_pos) and
                                self.board[inter1_pos[0]][inter1_pos[1]] == 0 and
                                self.board[inter2_pos[0]][inter2_pos[1]] == 0):
                                break  # puente válido
                            else:
                                nx, ny = -1, -1
                            break

                if 0 <= nx < R and 0 <= ny < C:
                    if self.board[nx][ny] == player_id:
                        new_cost = cost
                    elif self.board[nx][ny] == 0:
                        new_cost = cost + 1
                    else:
                        continue  # celda del oponente

                    if (nx, ny) not in dist or new_cost < dist[(nx, ny)]:
                        dist[(nx, ny)] = new_cost
                        heapq.heappush(heap, (new_cost, (nx, ny)))

        return -1  # no se pudo conectar
    





    def min_stones_to_connect(self, player_id, directions):
            
            if player_id == 2:
                start_edge = [(0, i) for i in range(self.size)]
                target_edge = [(self.size-1, i) for i in range(self.size)]
            else:
            
                start_edge = [(i, 0) for i in range(self.size)]
                target_edge = [(i, self.size-1) for i in range(self.size)]


            R, C = self.size, self.size
            dist = {}
            heap = []

            for cell in start_edge:
                x, y = cell
                if self.board[x][y] == player_id:
                    cost = 0
                elif self.board[x][y] == 0:
                    cost = 1
                else:
                    continue
                dist[cell] = cost
                heapq.heappush(heap, (cost, cell))

            while heap:
                cost, (x, y) = heapq.heappop(heap)

                if (x, y) in target_edge:
                    return cost

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < R and 0 <= ny < C):
                        continue

                    # Si es un movimiento de puente, validar casillas intermedias
                    if (dx, dy) in self.vector_move_bridges:
                        for vec_bridge, inter1, inter2 in self.bridge_patterns:
                            if vec_bridge == (dx, dy):
                                inter1_pos = (x + inter1[0], y + inter1[1])
                                inter2_pos = (x + inter2[0], y + inter2[1])

                                if (self.is_on_board(inter1_pos) and self.is_on_board(inter2_pos) and
                                    self.board[inter1_pos[0]][inter1_pos[1]] == 0 and
                                    self.board[inter2_pos[0]][inter2_pos[1]] == 0):
                                    break  # puente válido
                                else:
                                    nx, ny = -1, -1  # forzar que no se procese
                                break  # no seguir buscando patrones

                    if 0 <= nx < R and 0 <= ny < C:
                        if self.board[nx][ny] == player_id:
                            new_cost = cost
                        elif self.board[nx][ny] == 0:
                            new_cost = cost + 1
                        else:
                            continue

                        if (nx, ny) not in dist or new_cost < dist[(nx, ny)]:
                            dist[(nx, ny)] = new_cost
                            heapq.heappush(heap, (new_cost, (nx, ny)))

            return -1

    
    def get_one_empty_cell_in_connection_path(self, player_id):
        R, C = self.size, self.size

        if player_id == 1:
            start_edge = [(i, 0) for i in range(R)]
            target_edge = [(i, C - 1) for i in range(R)]
        else:
            start_edge = [(0, i) for i in range(C)]
            target_edge = [(R - 1, i) for i in range(C)]

        dist = {}
        came_from = {}
        heap = []

        for cell in start_edge:
            x, y = cell
            if self.board[x][y] == player_id:
                cost = 0
            elif self.board[x][y] == 0:
                cost = 1
            else:
                continue
            dist[cell] = cost
            heapq.heappush(heap, (cost, cell))

        while heap:
            cost, current = heapq.heappop(heap)
            x, y = current

            if current in target_edge:
                # Reconstruir camino
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(current)
                path.reverse()
                for cell in path:
                    if self.board[cell[0]][cell[1]] == 0:
                        return cell  # Primera celda vacía del camino
                return None

            for dx, dy in self.directions:  # solo direcciones simples, sin puentes
                nx, ny = x + dx, y + dy
                if not self.is_on_board((nx, ny)):
                    continue

                if self.board[nx][ny] == player_id:
                    new_cost = cost
                elif self.board[nx][ny] == 0:
                    new_cost = cost + 1
                else:
                    continue

                if (nx, ny) not in dist or new_cost < dist[(nx, ny)]:
                    dist[(nx, ny)] = new_cost
                    came_from[(nx, ny)] = (x, y)
                    heapq.heappush(heap, (new_cost, (nx, ny)))

        return None


    def hex_distance(self,a,b):

        return max(
            abs(a[0]-b[0]),
            abs(a[1]-b[1]),
            abs((a[0] + a[0])- (b[0]+b[1]))
        )
    

    def improved_heuristic(self,pos,goal_nodes,opponent_positions):

        h1 = min(self.hex_distance(pos,goal) for goal in goal_nodes)

        proximity_penalty = sum(1 for op in opponent_positions if self.hex_distance(pos,op) <=1)

        return h1 + 3*proximity_penalty

        
    def min_cost_between_sets_a_star(self, start_set, end_set, player_id, directions, opponent_positions):
        visited = set()
        heap = []

        for start in start_set:
            h = self.improved_heuristic(start, end_set, opponent_positions)
            heapq.heappush(heap, (h, 0, start))  # (f = g + h, g, position)

        while heap:
            f, g, current = heapq.heappop(heap)

            if current in end_set:
                return g  # Ya llegamos al objetivo

            if current in visited:
                continue
            visited.add(current)

            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)

                if not self.is_on_board(neighbor):
                    continue

                value = self.board[nx][ny]

                # Permitimos movernos por nuestras propias fichas o espacios vacíos
                if value == player_id or value == 0:
                    cost = 1 if value == 0 else 0  # preferimos pasar por nuestras propias fichas
                    h = self.improved_heuristic(neighbor, end_set, opponent_positions)
                    heapq.heappush(heap, (g + cost + h, g + cost, neighbor))

        return -1  # No hay camino posible

    # def evaluate(self,player) -> float:
    #     """Funcion de evaluacion del tablero"""

    #     # si se conecta el tablero
    #     if self.check_connection(player):
    #         return 10000  # Player 1 wins
    #     if self.check_connection(3-player):
    #         return -10000  # Player 2 wins

    #     # el camino mas corto de puentes entre ambos jugadores

        

        
        
    #     dist_p1 = self.min_stones_to_connect(1,self.directions)
    #     dist_p2 = self.min_stones_to_connect(2,self.directions)

    #     bridges_p1 = self.min_stones_to_connect(1,self.directions+self.vector_move_bridges)
    #     bridges_p2 = self.min_stones_to_connect(2,self.directions+self.vector_move_bridges)

        
    #     bridges = bridges_p2 if player ==2 else bridges_p1
    #     bridges_opt = bridges_p1 if player == 2 else bridges_p2

    #     if bridges > 0:
    #         return 8000
    #     elif bridges_opt >0:
    #         return -8000
        
    #     distance_term = (1.0 / (dist_p1+1)) - (1.0 / (dist_p2+1))

    #     return distance_term

        




    def print_board(self):
        space = ""
        print(space , end="     ")
        for i in range(self.size):
            print(f"\033[34m{i}  \033[0m", end=" ")
        print("\n")
        for i in range(self.size):
            print(space , end=" ")
            print(f"\033[31m{i}  \033[0m",end=" ")
            for j in range(self.size):
                if self.board[i][j] == 0:
                    print("⬜ ",end=" ")
                if self.board[i][j] == 1:
                    print("🟥 ",end=" ")
                if self.board[i][j] == 2:
                    print("🟦 ",end=" ")
                if j == self.size -1:
                    print(f"\033[31m {i} \033[0m",end=" ")
            space += "  "
            print("\n")
        print(space,end="    ")
        for i in range(self.size):
            print(f"\033[34m{i}  \033[0m", end=" ")

    def undo(self):

        if len(self.state_stack) > 1:
            last_pc, move = self.state_stack.pop()

            self.board[move[0]][move[1]] = 0
            
            self.pc = last_pc
        else:

            self.pc = self.state_stack[0][0]
        

class PathCompresion:

    def __init__(self,n):
        self.parent = {}
        self.bridge_parent = {}
        self.size= {}
        self.bridge_size= {}
        self.history = []


    def find(self,cell,bridge = False):
        
        parent_structure = self.bridge_parent if bridge else self.parent

        if parent_structure[cell] != cell:
            parent_structure[cell] = self.find(parent_structure[cell],bridge)
        
        return parent_structure[cell]
    

    def union(self,cell1,cell2, bridge = False):
        """Une dos celdas en el mismo conjunto (union por tamanno)"""

        root1= self.find(cell1,bridge)
        root2= self.find(cell2,bridge)

        parent_structure = self.bridge_parent if bridge else self.parent
        size_structure = self.bridge_size if bridge else self.size
        
        if root1!=root2:
            if size_structure[root1] < size_structure[root2]:
                root1,root2 = root2, root1
            
            self.history.append((
                bridge,                         # si era de tipo bridge
                root2,                          # hijo
                parent_structure[root2],        # su padre original
                root1,                          # nuevo padre
                size_structure[root1]           # tamaño original del nuevo padre
            ))

            parent_structure[root2] = root1
            size_structure[root1]+= size_structure[root2]

        else:
            self.history.append(None)

    def undo(self):
        "Deshace la ultima union"

        change = self.history.pop()

        if change is None:
            return 

        bridge, root2, old_parent , root1, old_size = change

        parent_structure = self.bridge_parent if bridge else self.parent
        size_structure = self.bridge_size if bridge else self.size
        
        parent_structure[root2] = old_parent
        size_structure[root1] = old_size
    
    def search_all_hommies(self, cell,bridge= False):
        root = self.find(cell,bridge)
        parent_structure = self.bridge_parent if bridge else self.parent
        return [c for c in parent_structure if self.find(c,bridge) == root and isinstance(c, tuple)]

    def clone(self):

        new_pc = copy.deepcopy(self)
        return new_pc
