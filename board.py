import pieces
from move import Move

class Board:
    """Class representing a chessboard."""

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        """Initialize the board with chess pieces and king movement flags."""
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboard):
        """Create a clone of the given chessboard."""
        chesspieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x][y]
                if piece != 0:
                    chesspieces[x][y] = piece.clone()
        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls):
        """Create a new chessboard with the initial setup."""
        chess_pieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        cls._create_pawns(chess_pieces)
        cls._create_rooks(chess_pieces)
        cls._create_knights(chess_pieces)
        cls._create_bishops(chess_pieces)
        cls._create_royalty(chess_pieces)
        return cls(chess_pieces, False, False)

    @staticmethod
    def _create_pawns(chess_pieces):
        for x in range(Board.WIDTH):
            chess_pieces[x][Board.HEIGHT-2] = pieces.Pawn(x, Board.HEIGHT-2, pieces.Piece.WHITE)
            chess_pieces[x][1] = pieces.Pawn(x, 1, pieces.Piece.BLACK)

    @staticmethod
    def _create_rooks(chess_pieces):
        chess_pieces[0][Board.HEIGHT-1] = pieces.Rook(0, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-1] = pieces.Rook(Board.WIDTH-1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[0][0] = pieces.Rook(0, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][0] = pieces.Rook(Board.WIDTH-1, 0, pieces.Piece.BLACK)

    @staticmethod
    def _create_knights(chess_pieces):
        chess_pieces[1][Board.HEIGHT-1] = pieces.Knight(1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-2][Board.HEIGHT-1] = pieces.Knight(Board.WIDTH-2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[1][0] = pieces.Knight(1, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-2][0] = pieces.Knight(Board.WIDTH-2, 0, pieces.Piece.BLACK)

    @staticmethod
    def _create_bishops(chess_pieces):
        chess_pieces[2][Board.HEIGHT-1] = pieces.Bishop(2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-3][Board.HEIGHT-1] = pieces.Bishop(Board.WIDTH-3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[2][0] = pieces.Bishop(2, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-3][0] = pieces.Bishop(Board.WIDTH-3, 0, pieces.Piece.BLACK)

    @staticmethod
    def _create_royalty(chess_pieces):
        chess_pieces[4][Board.HEIGHT-1] = pieces.King(4, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[3][Board.HEIGHT-1] = pieces.Queen(3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[4][0] = pieces.King(4, 0, pieces.Piece.BLACK)
        chess_pieces[3][0] = pieces.Queen(3, 0, pieces.Piece.BLACK)

    def get_possible_moves(self, color):
        """Get all possible moves for the given color."""
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.color == color:
                    moves += piece.get_possible_moves(self)
        return moves

    def perform_move(self, move):
        """Perform the given move on the board."""
        piece = self.chesspieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)
        self._handle_special_moves(piece, move)

    def _handle_special_moves(self, piece, move):
        """Handle special moves like pawn promotion and castling."""
        if piece.piece_type == pieces.Pawn.PIECE_TYPE:
            self._promote_pawn(piece)
        elif piece.piece_type == pieces.King.PIECE_TYPE:
            self._handle_castling(piece, move)

    def _promote_pawn(self, piece):
        if piece.y == 0 or piece.y == Board.HEIGHT-1:
            self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

    def _handle_castling(self, piece, move):
        if piece.color == pieces.Piece.WHITE:
            self.white_king_moved = True
        else:
            self.black_king_moved = True
        if move.xto - move.xfrom == 2:
            rook = self.chesspieces[piece.x+1][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)
        elif move.xto - move.xfrom == -2:
            rook = self.chesspieces[piece.x-2][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)

    def move_piece(self, piece, xto, yto):
        """Move a piece to the given coordinates."""
        self.chesspieces[piece.x][piece.y] = 0
        piece.x = xto
        piece.y = yto
        self.chesspieces[xto][yto] = piece

    def is_check(self, color):
        """Check if the given color is in check."""
        other_color = pieces.Piece.WHITE if color == pieces.Piece.BLACK else pieces.Piece.BLACK
        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)
            if not self._king_exists(copy, color):
                return True
        return False

    def _king_exists(self, board, color):
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = board.chesspieces[x][y]
                if piece != 0 and piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE:
                    return True
        return False

    def get_piece(self, x, y):
        """Get the piece at the given coordinates or 0 if out of bounds."""
        return self.chesspieces[x][y] if self.in_bounds(x, y) else 0

    def in_bounds(self, x, y):
        """Check if the given coordinates are within the board bounds."""
        return 0 <= x < Board.WIDTH and 0 <= y < Board.HEIGHT

    def to_string(self):
        """Convert the board state to a string representation."""
        string = "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for y in range(Board.HEIGHT):
            string += str(8 - y) + " | "
            for x in range(Board.WIDTH):
                piece = self.chesspieces[x][y]
                string += piece.to_string() if piece != 0 else ".. "
            string += "\n"
        return string + "\n"
