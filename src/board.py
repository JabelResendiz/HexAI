import numpy as np
from collections import deque

class HexBoard:
    def __init__(self, size: int):

        self.size = size  # Tamaño N del tablero (NxN)
        self.board=  np.zeros((size,size), dtype = int)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador

        self.last_move = None
        self.parent = {}
        self.size_uf = {}

        self.bridge_parent = {}
        self.bridge_size_uf ={}

        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]

        self.vector_move_bridges = [(-1, 2), (-1, -1), (-2, 1),
                                    (1, -2), (1, 1), (2, -1)]

        for row in range(size):
            for col in range(size):
                self.parent[(row,col)] = (row,col)
                self.size_uf[(row,col)] = 1

                self.bridge_parent[(row, col)] = (row, col)
                self.bridge_size_uf[(row, col)] = 1


        self.virtual_nodes = {
            1:("LEFT","RIGHT"),
            2:("TOP","BOTTOM")
        }

        for node in ["LEFT","RIGHT","TOP","BOTTOM"]:
            self.parent[node] = node
            self.size_uf[node] =1

            self.bridge_parent[node] = node
            self.bridge_size_uf[node] = 1
        
    def find (self,cell,bridge = False):
        """Busca el representante de un conjunto (con compresion de caminos)"""

        parent_structure = self.bridge_parent if bridge else self.parent

        if parent_structure[cell] != cell:
            parent_structure[cell] = self.find(parent_structure[cell],bridge)
        
        return parent_structure[cell]
    
    def union(self,cell1,cell2):
        """Une dos celdas en el mismo conjunto (union por tamanno)"""

        root1= self.find(cell1)
        root2= self.find(cell2)

        if root1!=root2:
            if self.size_uf[root1] < self.size_uf[root2]:
                root1,root2 = root2, root1
            
            self.parent[root2] = root1
            self.size_uf[root1]+= self.size_uf[root2]
    

    def bridge_union(self,cell1,cell2):

        root1= self.find(cell1,bridge = True)
        root2 = self.find(cell2,bridge=True)

        if root1 != root2:
            if self.bridge_size_uf[root1] < self.bridge_size_uf[root2]:
                root1, root2 = root2, root1

            self.bridge_parent[root2] = root1
            self.bridge_size_uf[root1] += self.bridge_size_uf[root2]



    def clone(self) -> 'HexBoard':
        """Devuelve una copia del tablero actual"""
        new_board = HexBoard(self.size)
        new_board.board= self.board.copy()
        new_board.player_positions = {1: self.player_positions[1].copy(), 2: self.player_positions[2].copy()}  
        new_board.parent = self.parent.copy()
        new_board.size_uf = self.size_uf.copy()
        return new_board
    

    def is_on_board(self,cell:tuple) -> bool:
        r,c = cell
        return 0<= r < self.size and 0<= c < self.size

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """Coloca una ficha si la casilla está vacía."""
        if not self.is_on_board((row,col)):

            return False
    
        if self.board[row][col] !=0:

            return False
        
        self.last_move = (row,col)
        self.board[row][col] = player_id
        self.player_positions[player_id].add((row,col))

        
        for dr, dc in self.directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player_id:
                self.union((row, col), (nr, nc))
                self.bridge_union((row,col),(nr,nc))
                
        # Conectar con mis nodos virtuales si estan en los bordes

        if player_id ==1:
            if col ==0:
                self.union((row,col),"LEFT")
                self.bridge_union((row,col),"LEFT")
            if col == self.size -1:
                self.union((row,col),"RIGHT")
                self.bridge_union((row,col),"RIGHT")
        
        else :
            if row ==0:
                self.union((row,col),"TOP")
                self.bridge_union((row,col),"TOP")
            if row == self.size -1:
                self.union((row,col),"BOTTOM")
                self.bridge_union((row,col),"BOTTOM")


        for dr, dc in self.vector_move_bridges:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player_id:
                self.bridge_union((row, col), (nr, nc))
        
        if player_id ==1:
            if col == 1:
                self.bridge_union((row,col),"LEFT")
            if col == self.size -2:
                self.bridge_union((row,col),"RIGHT")
        
        else :
            if row ==1:
                self.bridge_union((row,col),"TOP")
            if row == self.size -2:
                self.bridge_union((row,col),"BOTTOM")

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

        return self.find(v1) == self.find(v2)
    

        # if player_id == 1:
        #     start_edge = [(r,0) for r in range(self.size) if self.board[r][0]==1]
        #     target_edge = [(r,self.size-1) for r in range(self.size) if self.board[r][self.size-1]==1]
        
        # else :
        #     start_edge = [(0,r) for r in range(self.size) if self.board[0][r]==2]
        #     target_edge = [(self.size-1,r) for r in range(self.size) if self.board[self.size-1][r]==2]


        # start_root = {self.find(start) for start in start_edge}
        # target_root = {self.find(target) for target in target_edge}

        # return not start_root.isdisjoint(target_root)
    

    def check_bridges_pattern(self,player_id:int) -> bool:

        v1,v2 = self.virtual_nodes[player_id]

        return self.find(v1,True) == self.find(v2,True)
    
    
    def bfs(self,player_id:int) -> list:

        
        if player_id ==1 :
            v = self.find("LEFT")
            w = self.find("RIGHT")
            start_edge = {node for node in self.parent if self.parent[node] == v and node != "LEFT"}
            target_edge = {node for node in self.parent if self.parent[node] == w and node != "RIGHT"}
            start_edge2 = {(r,1) for r in range(self.size) if self.board[r][1] == 1}
            target_edge2 = {(r,self.size-2) for r in range(self.size) if self.board[r][self.size-2]==1}
            
        else:
            v = self.find("TOP")
            w = self.find("BOTTOM")
            start_edge ={node for node in self.parent if self.parent[node] == v and node != "TOP"}
            target_edge = {node for node in self.parent if self.parent[node] == w and node != "BOTTOM"}
            start_edge2 ={(1,c) for c in range(self.size) if self.board[1][c] ==2}
            target_edge2 = {(self.size-2,c) for c in range (self.size) if self.board[self.size-2][c]==2}

        def shortest_path(*paths):
            non_empty_paths = [path for path in paths if path]
            return min(non_empty_paths, key= len)
        
        d1 = self.run_bfs(player_id,start_edge,target_edge)
        d2= self.run_bfs(player_id,start_edge,target_edge2)
        d3 = self.run_bfs(player_id,start_edge2,target_edge)
        d4 = self.run_bfs(player_id,start_edge2,target_edge2)
        

        return shortest_path(d1,d2,d3,d4)

    # def search_all_hommies(self,cell):
        
    #     root = self.find(cell)

    #     result = []

    #     for c in range(len(self.parent)):
    #         if self.find(c) == root:
    #             result.append(c)
        
    #     return result

    def search_all_hommies(self, cell):
        root = self.find(cell)
        return [c for c in self.parent if self.find(c) == root and isinstance(c, tuple)]

    

    def run_bfs(self,player_id,start_edge,target_edge):

        visited= set()
        visited_parent = set ()
        queue = deque()
        parent_map = {}

        # start_edge podrian ser desde el punto de vista los representantes de grupos en si 
        # asi que primero debemos 
        for start in start_edge:
            if self.find(start) not in visited_parent:
                result = self.search_all_hommies(start)
                #print(result)
                for e in result:
                    queue.append(e)
                    visited.add(e)
                    parent_map[e] = None
                
                visited_parent.add(self.find(start))


        while queue:

            current = queue.popleft()
            
            if current in target_edge:
                
                path = []

                while current is not None:
                    path.append(current)
                    current = parent_map[current]

                path.reverse()

                return path
            
            all_directions = self.directions + self.vector_move_bridges
            
            for dr,dc in all_directions:
                nc,nr = current[0]+dr, current[1]+dc
                if self.is_on_board((nc,nr)):
                    if self.board[nc][nr] == player_id and (nc,nr) not in visited:
                        if self.find((nc,nr)) not in visited_parent:
                            result = self.search_all_hommies((nc,nr))
                            for e in result:
                                queue.append(e)
                                visited.add(e)
                                parent_map[e] = current
                            
                            visited_parent.add(self.find((nc,nr)))
                        # visited.add((nc,nr))
                        # queue.append((nc,nr))
                        # parent_map[(nc,nr)] = current
                        
            
        return []
        

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





class Graph:

    def __init__(self,parent,board,bridges_parent):
        self.parent = parent
        self.board = board
        self.bridges_parent = bridges_parent
        self.graph= self.build_graph()


    def build_graph(self):

        graph = {}

        for node in self.parent:
            group = self.parent[node]
            if group not in graph:
                graph[group] = set()
        
        
        

        return graph
    
    def bfs(self,player_id:int) ->list:


        visited = set()

        queue = deque()
        parent_map ={}

        if player_id == 1:
            v = self.parent["LEFT"]
            w = self.parent["RIGHT"]
        else:
            v = self.parent["TOP"]
            w = self.parent["BOTTOM"]

        queue.append(v)
        parent_map[v] = None

        while queue:
            
            current = queue.popleft()

            if current == w:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent_map[current]

                path.reverse()

                return path

            for edge in self.graph[current]:
                if edge not in visited:
                    queue.append(edge)
                    parent_map[edge] = current

        return []
    

    def process_path(self,player_id):

        g = self.bfs(player_id)

        print(g)

        
