import numpy as np

class HexBoard:
    def __init__(self, size: int):

        self.size = size  # Tamaño N del tablero (NxN)
        #self.board = [[0] * size for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
        self.board=  np.zeros((size,size), dtype = int)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador


        self.parent = {}
        self.size_uf = {}
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]

        for r in range(size):
            for c in range(size):
                self.parent[(r,c)] = (r,c)
                self.size_uf[(r,c)] = 1
    
    def find (self,cell):
        """Busca el representante de un conjunto (con compresion de caminos)"""

        if self.parent[cell] != cell:
            self.parent[cell] = self.find(self.parent[cell])
        
        return self.parent[cell]
    
    def union(self,cell1,cell2):
        """Une dos celdas en el mismo conjunto (union por tamanno)"""

        root1= self.find(cell1)
        root2= self.find(cell2)

        if root1!=root2:
            if self.size_uf[root1] < self.size_uf[root2]:
                root1,root2 = root2, root1
            
            self.parent[root2] = root1
            self.size_uf[root1]+= self.size_uf[root2]

    def clone(self) -> 'HexBoard':
        """Devuelve una copia del tablero actual"""
        new_board = HexBoard(self.size)
        #new_board.board = [row[:] for row in self.board] 
        new_board.board= self.board.copy()
        new_board.player_positions = {1: self.player_positions[1].copy(), 2: self.player_positions[2].copy()}  
        return new_board
    

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """Coloca una ficha si la casilla está vacía."""
        if row > self.size or row < 0 or col > self.size or col <0:

            return False
    
        if self.board[row][col] !=0:

            return False
    
        self.board[row][col] = player_id
        self.player_positions[player_id].add((row,col))

        
        for dr, dc in self.directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player_id:
                self.union((row, col), (nr, nc))

        return True


    def get_possible_moves(self) -> list:
        """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
        return [(row,col) 
                for row in range(self.size) 
                    for col in range(self.size) 
                        if self.board[row][col]==0
                ]

    
    def check_connection(self, player_id: int) -> bool:
        """Verifica si el jugador ha conectado sus dos lados"""
        
        if player_id==1:
            start_edge = [(r,0) for r in range(self.size) if self.board[r][0]==1]
            target_column = self.size-1
            is_goal = lambda r, c: c== target_column

        else :
            start_edge = [(0,c) for c in range(self.size) if self.board[0][c]==2]
            target_row = self.size -1
            is_goal = lambda r, c: r == target_row
        
        stack = start_edge[:]
        visited= set(start_edge)

        while stack:
            r,c = stack.pop()

            if is_goal(r,c):
                return True
            
            for dr,dc in self.directions:
                nr,nc = r+dr, c+dc
                if 0<= nr < self.size and 0<=nc < self.size and (nr,nc) not in visited:
                    if self.board[nr][nc] == player_id and self.find((r,c))== self.find((nr,nc)):
                        stack.append((nr,nc))
                        visited.add((nr,nc))

        return False
        
