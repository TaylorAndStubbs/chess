class Board:
    def __init__(self):
        self.board = self._create_empty_board()
        self._setup_board()

    def _create_empty_board(self):
        return [[None for _ in range(8)] for _ in range(8)]

    def _setup_board(self):
        # Setup pieces on the board
        pass

    def move_piece(self, start_pos, end_pos):
        piece = self._get_piece_at(start_pos)
        self._set_piece_at(end_pos, piece)
        self._set_piece_at(start_pos, None)

    def _get_piece_at(self, position):
        return self.board[position[0]][position[1]]

    def _set_piece_at(self, position, piece):
        self.board[position[0]][position[1]] = piece

    def display(self):
        for row in self.board:
            print(" ".join([str(piece) if piece else '.' for piece in row]))