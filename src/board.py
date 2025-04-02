import numpy as np

class HexBoard:
    def __init__(self, size: int):

        self.size = size  # Tamaño N del tablero (NxN)
        #self.board = [[0] * size for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
        self.board=  np.zeros((size,size), dtype = int)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador

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
        pass
