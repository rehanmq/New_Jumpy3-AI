#!/usr/bin/env python3
"""
alphabeta.py

This program plays a move for White using the alpha-beta pruning algorithm.
Usage:
    python alphabeta.py inputfile.txt outputfile.txt depth
Example:
    python alphabeta.py board1.txt board2.txt 2
"""
import sys
from jumpy3_utils import (
    read_board,
    write_board,
    alphabeta,
    static_evaluation,
    white_win,
    black_win
)

def main():
    if len(sys.argv) != 4:
        print("Usage: python alphabeta.py inputfile.txt outputfile.txt depth")
        sys.exit(1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    depth = int(sys.argv[3])

    board = read_board(inputfile)
    positions_evaluated = [0]

    eval_value, best_move = alphabeta(
        board, depth, -float('inf'), float('inf'), True, static_evaluation, positions_evaluated
    )

    print("Output board position:", ''.join(best_move))
    print("Positions evaluated by static estimation:", positions_evaluated[0])
    print("ALPHA-BETA estimate:", eval_value)

    # Manual check
    manual_eval = static_evaluation(best_move)
    print("Manual static eval of best move:", manual_eval)

    # Winner check
    if white_win(best_move):
        print(f" Winner: White detected at depth {depth}")
    elif black_win(best_move):
        print(f" Winner: Black detected at depth {depth}")
    else:
        print("⚪ No winner yet.")

    write_board(best_move, outputfile)

if __name__ == "__main__":
    main()
