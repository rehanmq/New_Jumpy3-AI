#!/usr/bin/env python3
"""
minimaxblack.py

This program plays a move for Black using the minimax algorithm.
It computes Black’s move by flipping the board, generating white moves, and flipping back.
Usage:
    python minimaxblack.py inputfile.txt outputfile.txt depth
Example:
    python minimaxblack.py board1.txt board2.txt 2
"""
import sys
from jumpy3_utils import read_board, write_board, minimax, flip, static_evaluation

def main():
    if len(sys.argv) != 4:
        print("Usage: python minimaxblack.py inputfile.txt outputfile.txt depth")
        sys.exit(1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    depth = int(sys.argv[3])
    
    board = read_board(inputfile)
    # Flip board so that black becomes white.
    flipped_board = flip(board)
    positions_evaluated = [0]
    # Use minimax as if white were playing on the flipped board.
    eval_value, best_move_flipped = minimax(flipped_board, depth, True, static_evaluation, positions_evaluated)
    # Flip back the resulting move.
    best_move = flip(best_move_flipped)
    
    print("Output board position:", ''.join(best_move))
    print("Positions evaluated by static estimation:", positions_evaluated[0])
    print("MINIMAX estimate (for Black move):", eval_value)
    
    write_board(best_move, outputfile)

if __name__ == "__main__":
    main()
