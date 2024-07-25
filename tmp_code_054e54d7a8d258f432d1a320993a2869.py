def move_piece(board, start_pos, end_pos):
    """
    Move a piece from start_pos to end_pos on the board.
    
    Args:
        board (dict): The game board.
        start_pos (tuple): The starting position of the piece.
        end_pos (tuple): The ending position of the piece.
    
    Returns:
        dict: The updated game board.
        str: Error message if the move is invalid.
    """
    if not is_valid_position(start_pos) or not is_valid_position(end_pos):
        return "Invalid position"
    
    if board.get(start_pos) is None:
        return "No piece at start position"
    
    piece = board[start_pos]
    board[end_pos] = piece
    board[start_pos] = None
    return board

def is_valid_position(pos):
    """
    Check if the given position is valid on the board.
    
    Args:
        pos (tuple): The position to check.
    
    Returns:
        bool: True if the position is valid, False otherwise.
    """
    return isinstance(pos, tuple) and len(pos) == 2 and all(isinstance(coord, int) for coord in pos)