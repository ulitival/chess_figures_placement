# pylint: disable=wrong-import-position
"""
The package exposes the solve function that calculate the number of ways N chess piece
figures can be placed on a chess board of size N x N.
"""

import functools
from typing import Literal

from phrase_chess_task import logging

log = logging.getLogger("phrase_chess_task.service_layer.solver")

from phrase_chess_task.service_layer.solvers import chess_solvers as solvers


@functools.lru_cache
def solve(board_size: int, chess_piece_type: Literal["knight", "bishop", "rook", "queen"]) -> int:
    """
    Accepts a board size and type of a chess piece and returns the total number of ways they can
    be placed on a board without attacking each other.
    :param board_size: the size of a board and as well a number of chess piece figures
    :return: the total number of ways `chess_piece_type` can be placed without attacking each other
    """
    return solvers[chess_piece_type](board_size)
