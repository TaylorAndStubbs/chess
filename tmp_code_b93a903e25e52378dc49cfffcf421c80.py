class Board:
    def __init__(self):
        """Initialize the chess board with pieces."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        """Setup the initial positions of the chess pieces on the board."""
        # Setup pieces on the board
        pass

    def move_piece(self, start_pos, end_pos):
        """Move a piece from start_pos to end_pos on the board."""
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None