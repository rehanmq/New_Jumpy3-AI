#!/usr/bin/env python3
"""
jumpy3_utils.py

This module contains common functions for the Jumpy3 project:
– Board I/O and representation (boards are lists of 16 characters)
– Move generation for White moves (and by flipping, for Black moves)
– The static evaluation function (and an improved version)
– Terminal tests (WhiteWin and BlackWin)
– Minimax and AlphaBeta search functions
"""

import copy

# ----------------------------
# Board I/O
# ----------------------------

def read_board(filename):
    """Read a board position from file. Expect a file with 16 characters."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Assume file content is exactly 16 characters (possibly with spaces/newlines removed)
    board = list(content.replace(" ", "").replace("\n", ""))
    if len(board) != 16:
        raise ValueError("Board must contain exactly 16 positions.")
    return board

def write_board(board, filename):
    """Write the board position to the given file as a string of 16 letters."""
    with open(filename, 'w') as f:
        f.write(''.join(board))

# ----------------------------
# Utility: Flip the board
# ----------------------------

def flip(board):
    """
    Flip the board by reversing the order and swapping White and Black pieces.
    Mapping: W <-> B, w <-> b; x remains x.
    """
    mapping = {'W': 'B', 'w': 'b', 'B': 'W', 'b': 'w', 'x': 'x'}
    flipped = [mapping[piece] for piece in board[::-1]]
    return flipped

# ----------------------------
# Move generation for White
# ----------------------------

def generate_white_moves(board):
    """
    Generate all possible board positions after one white move.
    For each white piece (W or w), apply the following rules:
      - If piece is at index 15: remove it (simulate moving off the board).
      - Else if the next square (i+1) is empty ('x'): move piece to i+1.
      - Else (jump): find the first empty square j to the right.
            * If no empty square exists, remove the piece.
            * Else, move piece from i to j.
                - If the jump length is exactly 2 (i.e. j == i+2), check:
                    if the jumped square (i+1) contains a black piece (b or B),
                    then “capture” it by moving that piece to the rightmost empty square.
                - If jump length is greater than 2, no capture is made.
    Each move is applied to a copy of the board.
    """
    moves = []
    for i, piece in enumerate(board):
        if piece not in ['W', 'w']:
            continue
        new_board = copy.deepcopy(board)
        if i == 15:
            # Move out of board.
            new_board[i] = 'x'
            moves.append(new_board)
        elif new_board[i+1] == 'x':
            # Simple one-step move.
            new_board[i+1] = piece
            new_board[i] = 'x'
            moves.append(new_board)
        else:
            # Jump move.
            # Find first empty square to the right of i
            j = None
            for idx in range(i+1, 16):
                if new_board[idx] == 'x':
                    j = idx
                    break
            if j is None:
                # No empty square: piece jumps out.
                new_board[i] = 'x'
                moves.append(new_board)
            else:
                # Copy board and perform jump.
                jump_board = copy.deepcopy(board)
                jump_board[j] = piece
                jump_board[i] = 'x'
                # Check if jump is over a single piece.
                if j - i == 2:
                    # Determine if jumped piece is white.
                    jumped_piece = board[i+1]
                    if jumped_piece in ['W', 'w']:
                        # Jump over own piece: no capture.
                        moves.append(jump_board)
                    else:
                        # Jump over a black piece: capture it.
                        # Find rightmost empty square.
                        k = None
                        for idx in range(15, -1, -1):
                            if jump_board[idx] == 'x':
                                k = idx
                                break
                        if k is not None:
                            jump_board[k] = jumped_piece
                        # Remove the jumped piece.
                        jump_board[i+1] = 'x'
                        moves.append(jump_board)
                else:
                    # Jump over several squares: no capture.
                    moves.append(jump_board)
    return moves

def generate_black_moves(board):
    """
    Generate moves for Black by flipping the board, generating white moves,
    and then flipping the results back.
    """
    flipped = flip(board)
    white_moves_on_flipped = generate_white_moves(flipped)
    black_moves = [flip(b) for b in white_moves_on_flipped]
    return black_moves

# ----------------------------
# Terminal conditions and static evaluation
# ----------------------------

def white_win(board):
    """White wins if the board does not contain White king 'W'."""
    return 'W' not in board

def black_win(board):
    """Black wins if the board does not contain Black king 'B'."""
    return 'B' not in board

def static_evaluation(board):
    """
    Standard static evaluation:
       If White wins, return 100;
       If Black wins, return -100;
       Otherwise, let i be the index of White king (W) and j the index of Black king (B),
       and return (i + j - 15).
    """
    if white_win(board):
        return 100
    if black_win(board):
        return -100
    try:
        i = board.index('W')
    except ValueError:
        # Should not occur if game is not terminal.
        i = 16
    try:
        j = board.index('B')
    except ValueError:
        j = -1
    return i + j - 15

def improved_static_evaluation(board):
    """
    Improved static evaluation function.
    In addition to the basic evaluation (king positions), this function also takes into
    account the mobility (the number of legal moves available) for White and Black.
    The evaluation is defined as:
         evaluation = (i + j - 15) + 0.1 * (num_white_moves - num_black_moves)
    Terminal positions are evaluated the same as before.
    """
    if white_win(board):
        return 100
    if black_win(board):
        return -100
    try:
        i = board.index('W')
    except ValueError:
        i = 16
    try:
        j = board.index('B')
    except ValueError:
        j = -1
    basic_eval = i + j - 15
    num_white_moves = len(generate_white_moves(board))
    num_black_moves = len(generate_black_moves(board))
    mobility_bonus = 0.1 * (num_white_moves - num_black_moves)
    return basic_eval + mobility_bonus

# ----------------------------
# Minimax and AlphaBeta search routines
# ----------------------------

def minimax(board, depth, is_white_turn, eval_fn, positions_evaluated):
    """
    Minimax search.
    
    Parameters:
      board: current board position.
      depth: remaining depth to search.
      is_white_turn: True if it is White’s move (maximizing), False for Black (minimizing).
      eval_fn: function to evaluate a board (static_evaluation or improved_static_evaluation).
      positions_evaluated: a list with one element (acting as a mutable counter).
      
    Returns:
      (best_eval, best_move)
    """
    # Terminal node: if game is over or depth==0, evaluate.
    if depth == 0 or white_win(board) or black_win(board):
        positions_evaluated[0] += 1
        return eval_fn(board), board

    if is_white_turn:
        best_eval = -float('inf')
        best_move = None
        moves = generate_white_moves(board)
        for move in moves:
            eval_value, _ = minimax(move, depth - 1, False, eval_fn, positions_evaluated)
            if eval_value > best_eval:
                best_eval = eval_value
                best_move = move
        return best_eval, best_move
    else:
        best_eval = float('inf')
        best_move = None
        moves = generate_black_moves(board)
        for move in moves:
            eval_value, _ = minimax(move, depth - 1, True, eval_fn, positions_evaluated)
            if eval_value < best_eval:
                best_eval = eval_value
                best_move = move
        return best_eval, best_move

def alphabeta(board, depth, alpha, beta, is_white_turn, eval_fn, positions_evaluated):
    """
    Alpha-Beta pruning search.
    
    Parameters:
      board: current board position.
      depth: remaining depth.
      alpha: current alpha value.
      beta: current beta value.
      is_white_turn: True if maximizing (White), False if minimizing (Black).
      eval_fn: static evaluation function.
      positions_evaluated: a list with one element for counting evaluations.
      
    Returns:
      (best_eval, best_move)
    """
    if depth == 0 or white_win(board) or black_win(board):
        positions_evaluated[0] += 1
        return eval_fn(board), board

    if is_white_turn:
        best_eval = -float('inf')
        best_move = None
        moves = generate_white_moves(board)
        for move in moves:
            eval_value, _ = alphabeta(move, depth - 1, alpha, beta, False, eval_fn, positions_evaluated)
            if eval_value > best_eval:
                best_eval = eval_value
                best_move = move
            alpha = max(alpha, best_eval)
            if beta <= alpha:
                break  # Beta cutoff
        return best_eval, best_move
    else:
        best_eval = float('inf')
        best_move = None
        moves = generate_black_moves(board)
        for move in moves:
            eval_value, _ = alphabeta(move, depth - 1, alpha, beta, True, eval_fn, positions_evaluated)
            if eval_value < best_eval:
                best_eval = eval_value
                best_move = move
            beta = min(beta, best_eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return best_eval, best_move
