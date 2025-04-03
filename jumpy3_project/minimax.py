#!/usr/bin/env python3
"""
minimax.py

This program plays a move for White using the minimax algorithm.
Usage:
    python minimax.py inputfile.txt outputfile.txt depth [--quiet]
Example:
    python minimax.py board1.txt board2.txt 2
    python minimax.py board1.txt board2.txt 4 --quiet
"""

import sys
from jumpy3_utils import (
    read_board,
    write_board,
    minimax,
    static_evaluation,
    generate_white_moves,
    white_win,
    black_win
)

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python minimax.py inputfile.txt outputfile.txt depth [--quiet]")
        sys.exit(1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    depth = int(sys.argv[3])
    quiet = len(sys.argv) == 5 and sys.argv[4] == "--quiet"

    board = read_board(inputfile)

    # Debug: List all possible White moves and their evaluations
    if not quiet:
        print("\n Debug: Generated White Moves from input position:")
        moves = generate_white_moves(board)
        for idx, m in enumerate(moves):
            move_str = ''.join(m)
            eval_val = static_evaluation(m)
            print(f"Move {idx+1}: {move_str} | Eval: {eval_val}")
        print()

    # Run MiniMax algorithm
    positions_evaluated = [0]
    eval_value, best_move = minimax(board, depth, True, static_evaluation, positions_evaluated)

    # 🗞 Output results
    if not quiet:
        print("Output board position:", ''.join(best_move))
        print("Positions evaluated by static estimation:", positions_evaluated[0])
        print("MINIMAX estimate:", eval_value)
        manual_eval = static_evaluation(best_move)
        print("Manual static eval of best move:", manual_eval)

    #  Winner check with depth display
    if white_win(best_move):
        print(f"\ud83c\udfc6 Winner: White detected at depth {depth}")
    elif black_win(best_move):
        print(f"\ud83c\udfc6 Winner: Black detected at depth {depth}")
    else:
        print(" No winner yet.")

    write_board(best_move, outputfile)

if __name__ == "__main__":
    main()
