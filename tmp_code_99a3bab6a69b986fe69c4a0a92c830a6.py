import pieces
from move import Move

class Board:
    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chess_pieces, white_king_moved=False, black_king_moved=False):
        """
        Initialize the board with the given chess pieces and flags indicating whether the kings have moved.
        """
        self.chess_pieces = chess_pieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboard):
        """
        Create a clone of the given chessboard.
        """
        chess_pieces = [[0 for _ in range(cls.WIDTH)] for _ in range(cls.HEIGHT)]
        for x in range(cls.WIDTH):
            for y in range(cls.HEIGHT):
                piece = chessboard.chess_pieces[x][y]
                if piece != 0:
                    chess_pieces[x][y] = piece.clone()
        return cls(chess_pieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls):
        """
        Create a new chessboard with the initial setup of pieces.
        """
        chess_pieces = [[0 for _ in range(cls.WIDTH)] for _ in range(cls.HEIGHT)]
        cls._setup_pieces(chess_pieces)
        return cls(chess_pieces)

    @staticmethod
    def _setup_pieces(chess_pieces):
        """
        Set up the initial positions of the chess pieces on the board.
        """
        # Create pawns
        for x in range(Board.WIDTH):
            chess_pieces[x][Board.HEIGHT-2] = pieces.Pawn(x, Board.HEIGHT-2, pieces.Piece.WHITE)
            chess_pieces[x][1] = pieces.Pawn(x, 1, pieces.Piece.BLACK)

        # Create rooks
        chess_pieces[0][Board.HEIGHT-1] = pieces.Rook(0, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-1] = pieces.Rook(Board.WIDTH-1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[0][0] = pieces.Rook(0, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][0] = pieces.Rook(Board.WIDTH-1, 0, pieces.Piece.BLACK)

        # Create knights
        chess_pieces[1][Board.HEIGHT-1] = pieces.Knight(1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-2][Board.HEIGHT-1] = pieces.Knight(Board.WIDTH-2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[1][0] = pieces.Knight(1, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-2][0] = pieces.Knight(Board.WIDTH-2, 0, pieces.Piece.BLACK)

        # Create bishops
        chess_pieces[2][Board.HEIGHT-1] = pieces.Bishop(2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-3][Board.HEIGHT-1] = pieces.Bishop(Board.WIDTH-3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[2][0] = pieces.Bishop(2, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-3][0] = pieces.Bishop(Board.WIDTH-3, 0, pieces.Piece.BLACK)

        # Create kings and queens
        chess_pieces[4][Board.HEIGHT-1] = pieces.King(4, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[3][Board.HEIGHT-1] = pieces.Queen(3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[4][0] = pieces.King(4, 0, pieces.Piece.BLACK)
        chess_pieces[3][0] = pieces.Queen(3, 0, pieces.Piece.BLACK)

    def get_possible_moves(self, color):
        """
        Return a list of possible moves for the given color.
        """
        moves = []
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                piece = self.chess_pieces[x][y]
                if piece != 0 and piece.color == color:
                    moves.extend(piece.get_possible_moves(self))
        return moves

    def perform_move(self, move):
        """
        Perform the given move on the board.
        """
        piece = self.chess_pieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)
        self._handle_special_moves(piece, move)

    def _handle_special_moves(self, piece, move):
        """
        Handle special moves like pawn promotion and castling.
        """
        if piece.piece_type == pieces.Pawn.PIECE_TYPE:
            self._handle_pawn_promotion(piece)
        elif piece.piece_type == pieces.King.PIECE_TYPE:
            self._handle_castling(piece, move)

    def _handle_pawn_promotion(self, piece):
        """
        Promote a pawn to a queen if it reaches the end of the board.
        """
        if piece.y == 0 or piece.y == self.HEIGHT-1:
            self.chess_pieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

    def _handle_castling(self, piece, move):
        """
        Handle castling moves for the king.
        """
        if piece.color == pieces.Piece.WHITE:
            self.white_king_moved = True
        else:
            self.black_king_moved = True

        if move.xto - move.xfrom == 2:  # King-side castling
            rook = self.chess_pieces[piece.x+1][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)
        elif move.xto - move.xfrom == -2:  # Queen-side castling
            rook = self.chess_pieces[piece.x-2][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)

    def move_piece(self, piece, xto, yto):
        """
        Move a piece to the specified position.
        """
        self.chess_pieces[piece.x][piece.y] = 0
        piece.x = xto
        piece.y = yto
        self.chess_pieces[xto][yto] = piece

    def is_check(self, color):
        """
        Check if the given color is in check.
        """
        opponent_color = pieces.Piece.BLACK if color == pieces.Piece.WHITE else pieces.Piece.WHITE
        for move in self.get_possible_moves(opponent_color):
            copy = self.clone(self)
            copy.perform_move(move)
            if not any(piece for row in copy.chess_pieces for piece in row if piece and piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE):
                return True
        return False

    def get_piece(self, x, y):
        """
        Return the piece at the given position or 0 if there is no piece or the position is out of bounds.
        """
        return self.chess_pieces[x][y] if self.in_bounds(x, y) else 0

    def in_bounds(self, x, y):
        """
        Check if the given position is within the bounds of the board.
        """
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT

    def to_string(self):
        """
        Return a string representation of the board.
        """
        board_str = "    A  B  C  D  E  F  G  H\n"
        board_str += "    -----------------------\n"
        for y in range(self.HEIGHT):
            board_str += f"{8 - y} | "
            for x in range(self.WIDTH):
                piece = self.chess_pieces[x][y]
                board_str += piece.to_string() if piece != 0 else ".. "
            board_str += "\n"
        return board_str + "\n"