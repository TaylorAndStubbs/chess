import pieces
from move import Move

class Board:
    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        """
        Initialize the board with chess pieces and king movement status.
        """
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboard):
        """
        Clone the given chessboard.
        """
        chesspieces = [[piece.clone() if piece != 0 else 0 for piece in row] for row in chessboard.chesspieces]
        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls):
        """
        Create a new chessboard with initial positions of pieces.
        """
        chess_pieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        cls._create_pieces(chess_pieces)
        return cls(chess_pieces, False, False)

    @staticmethod
    def _create_pieces(chess_pieces):
        """
        Helper method to create pieces on the board.
        """
        # Create pawns
        for x in range(Board.WIDTH):
            chess_pieces[x][Board.HEIGHT-2] = pieces.Pawn(x, Board.HEIGHT-2, pieces.Piece.WHITE)
            chess_pieces[x][1] = pieces.Pawn(x, 1, pieces.Piece.BLACK)

        # Create rooks
        positions = [(0, Board.HEIGHT-1), (Board.WIDTH-1, Board.HEIGHT-1), (0, 0), (Board.WIDTH-1, 0)]
        colors = [pieces.Piece.WHITE, pieces.Piece.WHITE, pieces.Piece.BLACK, pieces.Piece.BLACK]
        for (x, y), color in zip(positions, colors):
            chess_pieces[x][y] = pieces.Rook(x, y, color)

        # Create knights
        positions = [(1, Board.HEIGHT-1), (Board.WIDTH-2, Board.HEIGHT-1), (1, 0), (Board.WIDTH-2, 0)]
        for (x, y), color in zip(positions, colors):
            chess_pieces[x][y] = pieces.Knight(x, y, color)

        # Create bishops
        positions = [(2, Board.HEIGHT-1), (Board.WIDTH-3, Board.HEIGHT-1), (2, 0), (Board.WIDTH-3, 0)]
        for (x, y), color in zip(positions, colors):
            chess_pieces[x][y] = pieces.Bishop(x, y, color)

        # Create kings and queens
        positions = [(4, Board.HEIGHT-1), (3, Board.HEIGHT-1), (4, 0), (3, 0)]
        types = [pieces.King, pieces.Queen, pieces.King, pieces.Queen]
        for (x, y), piece_type in zip(positions, types):
            color = pieces.Piece.WHITE if y == Board.HEIGHT-1 else pieces.Piece.BLACK
            chess_pieces[x][y] = piece_type(x, y, color)

    def get_possible_moves(self, color):
        """
        Get all possible moves for the given color.
        """
        return [move for row in self.chesspieces for piece in row if piece != 0 and piece.color == color for move in piece.get_possible_moves(self)]

    def perform_move(self, move):
        """
        Perform the given move on the board.
        """
        piece = self.chesspieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)

        # If a pawn reaches the end, upgrade it to a queen.
        if piece.piece_type == pieces.Pawn.PIECE_TYPE and (piece.y == 0 or piece.y == Board.HEIGHT-1):
            self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

        if piece.piece_type == pieces.King.PIECE_TYPE:
            self._handle_king_move(piece, move)

    def _handle_king_move(self, piece, move):
        """
        Handle special conditions when a king is moved.
        """
        if piece.color == pieces.Piece.WHITE:
            self.white_king_moved = True
        else:
            self.black_king_moved = True

        # Check for castling
        if abs(move.xto - move.xfrom) == 2:
            rook_x = piece.x + 1 if move.xto - move.xfrom == 2 else piece.x - 2
            rook = self.chesspieces[rook_x][piece.y]
            self.move_piece(rook, piece.x + 1, piece.y)

    def move_piece(self, piece, xto, yto):
        """
        Move a piece to the given coordinates.
        """
        self.chesspieces[piece.x][piece.y] = 0
        piece.x, piece.y = xto, yto
        self.chesspieces[xto][yto] = piece

    def is_check(self, color):
        """
        Check if the given color is in check.
        """
        other_color = pieces.Piece.BLACK if color == pieces.Piece.WHITE else pieces.Piece.WHITE
        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)
            if not any(piece != 0 and piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE for row in copy.chesspieces for piece in row):
                return True
        return False

    def get_piece(self, x, y):
        """
        Get the piece at the given coordinates or 0 if out of bounds.
        """
        return self.chesspieces[x][y] if self.in_bounds(x, y) else 0

    def in_bounds(self, x, y):
        """
        Check if the given coordinates are within the board bounds.
        """
        return 0 <= x < Board.WIDTH and 0 <= y < Board.HEIGHT

    def to_string(self):
        """
        Convert the board to a string representation.
        """
        board_str = "    A  B  C  D  E  F  G  H\n    -----------------------\n"
        for y in range(Board.HEIGHT):
            board_str += f"{8 - y} | " + " ".join(piece.to_string() if piece != 0 else ".." for piece in self.chesspieces[y]) + "\n"
        return board_str + "\n"