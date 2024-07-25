class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def move_piece(self, start_pos, end_pos):
        """Move a piece from start_pos to end_pos on the board."""
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None

    def __str__(self):
        """Return a string representation of the board."""
        return '\n'.join([' '.join([str(piece) if piece else '.' for piece in row]) for row in self.board])