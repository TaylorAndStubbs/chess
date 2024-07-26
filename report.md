# Chess Repository Report

## Files and Their Functionalities

### 1. `board.py`
- **Classes**:
  - `Board`: Represents the chessboard.
    - **Attributes**:
      - `WIDTH`, `HEIGHT`: Dimensions of the board.
      - `chesspieces`: 2D list representing the pieces on the board.
      - `white_king_moved`, `black_king_moved`: Flags indicating if the kings have moved.
    - **Methods**:
      - `__init__`: Initializes the board with pieces and king movement flags.
      - `clone`: Creates a deep copy of the board.
      - `new`: Creates a new board with initial piece positions.
      - `get_possible_moves`: Returns all possible moves for a given color.
      - `perform_move`: Executes a move on the board.
      - `move_piece`: Moves a piece to a new position.
      - `is_check`: Checks if a given color is in check.
      - `get_piece`: Returns the piece at a given position.
      - `in_bounds`: Checks if a position is within the board bounds.
      - `to_string`: Returns a string representation of the board.

### 2. `ai.py`
- **Classes**:
  - `Heuristics`: Contains methods for evaluating board positions.
    - **Attributes**:
      - `PAWN_TABLE`, `KNIGHT_TABLE`, `BISHOP_TABLE`, `ROOK_TABLE`, `QUEEN_TABLE`: Position evaluation tables for different pieces.
    - **Methods**:
      - `evaluate`: Evaluates the board position.
      - `get_piece_position_score`: Returns the score for the position of a given piece type.
      - `get_material_score`: Returns the material score of the board.
  - `AI`: Contains methods for AI move generation.
    - **Attributes**:
      - `INFINITE`: A large value used for evaluation.
    - **Methods**:
      - `get_ai_move`: Returns the best move for the AI.
      - `is_invalid_move`: Checks if a move is invalid.
      - `minimax`: Minimax algorithm for move evaluation.
      - `alphabeta`: Alpha-beta pruning algorithm for move evaluation.

### 3. `pieces.py`
- **Classes**:
  - `Piece`: Base class for all chess pieces.
    - **Attributes**:
      - `WHITE`, `BLACK`: Constants for piece colors.
      - `x`, `y`: Position of the piece.
      - `color`, `piece_type`, `value`: Attributes of the piece.
    - **Methods**:
      - `get_possible_diagonal_moves`, `get_possible_horizontal_moves`: Returns possible diagonal and horizontal moves.
      - `get_move`: Returns a move object for a given position.
      - `remove_null_from_list`: Removes null values from a list of moves.
      - `to_string`: Returns a string representation of the piece.
  - `Rook`, `Knight`, `Bishop`, `Queen`, `King`, `Pawn`: Subclasses of `Piece` representing specific chess pieces.
    - **Methods**:
      - `get_possible_moves`: Returns possible moves for the piece.
      - `clone`: Creates a copy of the piece.

### 4. `move.py`
- **Classes**:
  - `Move`: Represents a move in the game.
    - **Attributes**:
      - `xfrom`, `yfrom`, `xto`, `yto`: Coordinates of the move.
    - **Methods**:
      - `equals`: Checks if two moves are equal.
      - `to_string`: Returns a string representation of the move.

### 5. `main.py`
- **Functions**:
  - `get_user_move`: Gets a move from the user.
  - `get_valid_user_move`: Gets a valid move from the user.
  - `letter_to_xpos`: Converts a letter to a board position.
- **Main Logic**:
  - Initializes a new board.
  - Runs a loop to get user and AI moves, updating the board and checking for game end conditions.

## How to Run the Project

1. **Install Dependencies**:
   - Ensure you have Python and `numpy` installed.
   - You can install `numpy` using pip:
     ```bash
     pip install numpy
     ```

2. **Run the Main Script**:
   - Execute the `main.py` script to start the game:
     ```bash
     python main.py
     ```
