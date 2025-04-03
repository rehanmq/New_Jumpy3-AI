#!/usr/bin/env python3
"""
minimaximproved.py

This program plays a move for White using the minimax algorithm with an improved static evaluation.
The improved evaluation function adds a mobility bonus (the difference in number of legal moves).
Usage:
    python minimaximproved.py inputfile.txt outputfile.txt depth
Example:
    python minimaximproved.py board1.txt board2.txt 2

Explanation of improvement:
    In addition to the basic evaluation (which considers the positions of the kings),
    the improved static function rewards positions with greater mobility.
    By considering the number of legal moves available for White and Black,
    the evaluation better captures board control and potential for future moves.
"""
import sys
from jumpy3_utils import read_board, write_board, minimax, improved_static_evaluation

def main():
    if len(sys.argv) != 4:
        print("Usage: python minimaximproved.py inputfile.txt outputfile.txt depth")
        sys.exit(1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    depth = int(sys.argv[3])
    
    board = read_board(inputfile)
    positions_evaluated = [0]
    eval_value, best_move = minimax(board, depth, True, improved_static_evaluation, positions_evaluated)
    
    print("Output board position:", ''.join(best_move))
    print("Positions evaluated by static estimation:", positions_evaluated[0])
    print("MINIMAX (improved) estimate:", eval_value)
    
    write_board(best_move, outputfile)

if __name__ == "__main__":
    main()
