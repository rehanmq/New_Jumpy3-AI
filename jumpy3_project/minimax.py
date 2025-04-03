#!/usr/bin/env python3
"""
minimax.py

This program plays a move for White using the minimax algorithm.
Usage:
    python minimax.py inputfile.txt outputfile.txt depth
Example:
    python minimax.py board1.txt board2.txt 2
"""

import sys
from jumpy3_utils import (
    read_board,
    write_board,
    minimax,
    static_evaluation,
    generate_white_moves
)

def main():
    if len(sys.argv) != 4:
        print("Usage: python minimax.py inputfile.txt outputfile.txt depth")
        sys.exit(1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    depth = int(sys.argv[3])
    
    board = read_board(inputfile)

    # Debug: All possible White moves and their evaluations
    print("\n Debug: Generated White Moves from input position:")
    moves = generate_white_moves(board)
    for idx, m in enumerate(moves):
        move_str = ''.join(m)
        eval_val = static_evaluation(m)
        print(f"Move {idx+1}: {move_str} | Eval: {eval_val}")
    print()

    # 🧠 Run MiniMax algorithm
    positions_evaluated = [0]
    eval_value, best_move = minimax(board, depth, True, static_evaluation, positions_evaluated)
    
    # 🧾 Output results
    print("Output board position:", ''.join(best_move))
    print("Positions evaluated by static estimation:", positions_evaluated[0])
    print("MINIMAX estimate:", eval_value)

    # ✅ Sanity check
    manual_eval = static_evaluation(best_move)
    print("Manual static eval of best move:", manual_eval)

    write_board(best_move, outputfile)

if __name__ == "__main__":
    main()
