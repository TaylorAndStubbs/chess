import pieces
from move import Move

class Board:
    """
    The Board class manages the state and behavior of the chessboard.
    """

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        """
        Initialize the board with chess pieces and king movement flags.
        """
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboard):
        """
        Create a deep copy of the given chessboard.
        """
        chesspieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x][y]
                if piece != 0:
                    chesspieces[x][y] = piece.clone()
        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls):
        """
        Initialize a new chessboard with pieces in their starting positions.
        """
        chess_pieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        cls._initialize_pawns(chess_pieces)
        cls._initialize_rooks(chess_pieces)
        cls._initialize_knights(chess_pieces)
        cls._initialize_bishops(chess_pieces)
        cls._initialize_royalty(chess_pieces)
        return cls(chess_pieces, False, False)

    @staticmethod
    def _initialize_pawns(chess_pieces):
        for x in range(Board.WIDTH):
            chess_pieces[x][Board.HEIGHT-2] = pieces.Pawn(x, Board.HEIGHT-2, pieces.Piece.WHITE)
            chess_pieces[x][1] = pieces.Pawn(x, 1, pieces.Piece.BLACK)

    @staticmethod
    def _initialize_rooks(chess_pieces):
        chess_pieces[0][Board.HEIGHT-1] = pieces.Rook(0, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-1] = pieces.Rook(Board.WIDTH-1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[0][0] = pieces.Rook(0, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][0] = pieces.Rook(Board.WIDTH-1, 0, pieces.Piece.BLACK)

    @staticmethod
    def _initialize_knights(chess_pieces):
        chess_pieces[1][Board.HEIGHT-1] = pieces.Knight(1, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-2][Board.HEIGHT-1] = pieces.Knight(Board.WIDTH-2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[1][0] = pieces.Knight(1, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-2][0] = pieces.Knight(Board.WIDTH-2, 0, pieces.Piece.BLACK)

    @staticmethod
    def _initialize_bishops(chess_pieces):
        chess_pieces[2][Board.HEIGHT-1] = pieces.Bishop(2, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-3][Board.HEIGHT-1] = pieces.Bishop(Board.WIDTH-3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[2][0] = pieces.Bishop(2, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-3][0] = pieces.Bishop(Board.WIDTH-3, 0, pieces.Piece.BLACK)

    @staticmethod
    def _initialize_royalty(chess_pieces):
        chess_pieces[4][Board.HEIGHT-1] = pieces.King(4, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[3][Board.HEIGHT-1] = pieces.Queen(3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[4][0] = pieces.King(4, 0, pieces.Piece.BLACK)
        chess_pieces[3][0] = pieces.Queen(3, 0, pieces.Piece.BLACK)

    def get_possible_moves(self, color):
        """
        Return a list of possible moves for the given color.
        """
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.color == color:
                    moves += piece.get_possible_moves(self)
        return moves

    def perform_move(self, move):
        """
        Execute a given move on the board.
        """
        piece = self.chesspieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)
        self._handle_special_moves(piece, move)

    def _handle_special_moves(self, piece, move):
        """
        Handle special moves like pawn promotion and castling.
        """
        if piece.piece_type == pieces.Pawn.PIECE_TYPE:
            self._promote_pawn_if_necessary(piece)
        if piece.piece_type == pieces.King.PIECE_TYPE:
            self._update_king_movement_flags(piece)
            self._handle_castling(piece, move)

    def _promote_pawn_if_necessary(self, piece):
        if piece.y == 0 or piece.y == Board.HEIGHT-1:
            self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

    def _update_king_movement_flags(self, piece):
        if piece.color == pieces.Piece.WHITE:
            self.white_king_moved = True
        else:
            self.black_king_moved = True

    def _handle_castling(self, piece, move):
        if move.xto - move.xfrom == 2:  # King-side castling
            rook = self.chesspieces[piece.x+1][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)
        elif move.xto - move.xfrom == -2:  # Queen-side castling
            rook = self.chesspieces[piece.x-2][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)

    def move_piece(self, piece, xto, yto):
        """
        Move a piece to a new position.
        """
        self.chesspieces[piece.x][piece.y] = 0
        piece.x = xto
        piece.y = yto
        self.chesspieces[xto][yto] = piece

    def is_check(self, color):
        """
        Return True if the given color is in check, otherwise False.
        """
        other_color = pieces.Piece.WHITE if color == pieces.Piece.BLACK else pieces.Piece.BLACK
        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)
            if not any(piece != 0 and piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE
                       for row in copy.chesspieces for piece in row):
                return True
        return False

    def get_piece(self, x, y):
        """
        Return the piece at the given position or 0 if out of bounds.
        """
        return self.chesspieces[x][y] if self.in_bounds(x, y) else 0

    def in_bounds(self, x, y):
        """
        Check if the given coordinates are within the board's bounds.
        """
        return 0 <= x < Board.WIDTH and 0 <= y < Board.HEIGHT

    def to_string(self):
        """
        Return a string representation of the board.
        """
        board_str = "    A  B  C  D  E  F  G  H\n"
        board_str += "    -----------------------\n"
        for y in range(Board.HEIGHT):
            board_str += f"{8 - y} | "
            for x in range(Board.WIDTH):
                piece = self.chesspieces[x][y]
                board_str += piece.to_string() if piece != 0 else ".. "
            board_str += "\n"
        return board_str + "\n"
