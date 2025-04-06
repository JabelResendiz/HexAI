
class HexBoard:
    def __init__(self,value,left:'HexBoard' = None,right:'HexBoard'=None):
        self.value = value
        self.left = left
        self.right = right
    
    def get_possible_moves(self):
        return [self.left,self.right]


def heuristic_with_bonus(board: HexBoard):
    return board.value

def minimax(board:HexBoard, 
                depth :int, 
                maximizing_player: bool ,
                alpha : float= -float('inf'), 
                beta: float = float('inf'))-> float :

        """Implementacion del algoritmo del minimax usando poda alpha-beta"""
        
        if depth ==0 or (board.get_possible_moves()[1] == None and board.get_possible_moves()[0] == None):
            return heuristic_with_bonus(board)
        
        if maximizing_player:
            value = -float('inf')

            for move in board.get_possible_moves():
                # new_board = board.clone()
                # new_board.place_piece(move[0],move[1],1)

                value = max(value, minimax(move,depth-1,False,alpha,beta))

                alpha = max(alpha,value)

                if alpha >= beta:
                    break
            
                print(value)
            return value

        else :
            value = float('inf')
            for move in board.get_possible_moves():
                # new_board = board.clone()
                # new_board.place_piece(move[0],move[1],2)

                value = min(value, minimax(move,depth-1,True,alpha,beta))

                beta= min(beta,value)

                if alpha>=beta:
                    break
            
                print(value)
            return value 
        
if __name__ == "__main__":
    h = HexBoard(0,
                 HexBoard(0,
                          HexBoard(0,
                                   HexBoard(4), HexBoard(8)),
                          HexBoard(0,
                                   HexBoard(9), HexBoard(3))
                         ),
                 HexBoard(0,
                          HexBoard(0,
                                   HexBoard(2), HexBoard(-2)),
                            HexBoard(0,
                                     HexBoard(9), HexBoard(-1))
                        )
                )
    
    j= minimax(h,9,True)
    print("----------------------")
    print(j)