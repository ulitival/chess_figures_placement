"""N-rooks solver.

The solver utilizes the fact that the number of ways to place ``N`` rooks on a chessboard
of size ``N x N`` is given as a factorial of N.
"""
from math import factorial

from phrase_chess_task import logging

log = logging.getLogger(__name__)


def solve_rook(board_size: int) -> int:
    """Solves placement of N rooks on a NxN chess board.
    Where N == board_size.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) rooks can be placed on a board without them attacking each other
    """
    log.info(f"Solving N-rooks problem for {board_size} rooks.")
    return factorial(board_size)
