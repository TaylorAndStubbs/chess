class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None