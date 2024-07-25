def move_piece(board, start_pos, end_pos):
    if board[start_pos] is None:
        return "No piece at start position"
    piece = board[start_pos]
    board[end_pos] = piece
    board[start_pos] = None
    return board