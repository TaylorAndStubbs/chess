import pieces
from move import Move

class Board:

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboard):
        chesspieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x][y]
                if piece != 0:
                    chesspieces[x][y] = piece.clone()
        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls):
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
        positions = [(0, Board.HEIGHT-1), (Board.WIDTH-1, Board.HEIGHT-1), (0, 0), (Board.WIDTH-1, 0)]
        colors = [pieces.Piece.WHITE, pieces.Piece.WHITE, pieces.Piece.BLACK, pieces.Piece.BLACK]
        for (x, y), color in zip(positions, colors):
            chess_pieces[x][y] = pieces.Rook(x, y, color)

    @staticmethod
    def _create_knights(chess_pieces):
        positions = [(1, Board.HEIGHT-1), (Board.WIDTH-2, Board.HEIGHT-1), (1, 0), (Board.WIDTH-2, 0)]
        colors = [pieces.Piece.WHITE, pieces.Piece.WHITE, pieces.Piece.BLACK, pieces.Piece.BLACK]
        for (x, y), color in zip(positions, colors):
            chess_pieces[x][y] = pieces.Knight(x, y, color)

    @staticmethod
    def _create_bishops(chess_pieces):
        positions = [(2, Board.HEIGHT-1), (Board.WIDTH-3, Board.HEIGHT-1), (2, 0), (Board.WIDTH-3, 0)]
        colors = [pieces.Piece.WHITE, pieces.Piece.WHITE, pieces.Piece.BLACK, pieces.Piece.BLACK]
        for (x, y), color in zip(positions, colors):
            chess_pieces[x][y] = pieces.Bishop(x, y, color)

    @staticmethod
    def _create_royalty(chess_pieces):
        positions = [(4, Board.HEIGHT-1), (3, Board.HEIGHT-1), (4, 0), (3, 0)]
        pieces_types = [pieces.King, pieces.Queen, pieces.King, pieces.Queen]
        colors = [pieces.Piece.WHITE, pieces.Piece.WHITE, pieces.Piece.BLACK, pieces.Piece.BLACK]
        for (x, y), piece_type, color in zip(positions, pieces_types, colors):
            chess_pieces[x][y] = piece_type(x, y, color)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.color == color:
                    moves += piece.get_possible_moves(self)
        return moves

    def perform_move(self, move):
        piece = self.chesspieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)
        self._handle_special_moves(piece, move)

    def _handle_special_moves(self, piece, move):
        if piece.piece_type == pieces.Pawn.PIECE_TYPE:
            self._handle_pawn_promotion(piece)
        elif piece.piece_type == pieces.King.PIECE_TYPE:
            self._handle_king_move(piece, move)

    def _handle_pawn_promotion(self, piece):
        if piece.y == 0 or piece.y == Board.HEIGHT-1:
            self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

    def _handle_king_move(self, piece, move):
        if piece.color == pieces.Piece.WHITE:
            self.white_king_moved = True
        else:
            self.black_king_moved = True
        self._handle_castling(piece, move)

    def _handle_castling(self, piece, move):
        if move.xto - move.xfrom == 2:  # King-side castling
            rook = self.chesspieces[piece.x+1][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)
        elif move.xto - move.xfrom == -2:  # Queen-side castling
            rook = self.chesspieces[piece.x-2][piece.y]
            self.move_piece(rook, piece.x+1, piece.y)

    def move_piece(self, piece, xto, yto):
        self.chesspieces[piece.x][piece.y] = 0
        piece.x = xto
        piece.y = yto
        self.chesspieces[xto][yto] = piece

    def is_check(self, color):
        other_color = pieces.Piece.BLACK if color == pieces.Piece.WHITE else pieces.Piece.WHITE
        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)
            if not any(piece != 0 and piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE
                       for row in copy.chesspieces for piece in row):
                return True
        return False

    def get_piece(self, x, y):
        return self.chesspieces[x][y] if self.in_bounds(x, y) else 0

    def in_bounds(self, x, y):
        return 0 <= x < Board.WIDTH and 0 <= y < Board.HEIGHT

    def to_string(self):
        board_str = "    A  B  C  D  E  F  G  H\n"
        board_str += "    -----------------------\n"
        for y in range(Board.HEIGHT):
            board_str += f"{8 - y} | "
            for x in range(Board.WIDTH):
                piece = self.chesspieces[x][y]
                board_str += piece.to_string() if piece != 0 else ".. "
            board_str += "\n"
        return board_str + "\n"
