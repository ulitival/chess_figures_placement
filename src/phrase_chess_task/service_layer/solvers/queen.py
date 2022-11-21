# pylint: disable=duplicate-code
"""N-queens solver.

Based on CSP approach.
"""
from ortools.sat.python import cp_model

from phrase_chess_task import logging

from .common import ORToolsSolutionPrinter

log = logging.getLogger(__name__)


def solve_queen(board_size: int) -> int:
    """
    OR-Tools solution to the N-queens problem. Where N == board_size.

    This solution utilizes CSP approach using `ortools` package. The code for the N-queens problem
    can be found on the official `ortools` website here: https://developers.google.com/optimization/cp/queens.
    The approach below copies the aforementioned code as-is.
    The definition of the problem is the following:
        - variables: queens that are represented as an array. Each position in this array corresponds to a column
            on a chessboard, i.e. ``queens = [0, 1, 2, 3]`` means there are 4 queens that should be placed in columns
            ``0``, ``1``, ``2`` and ``3``
        - domain: a chessboard's row, such that each value in an array of queens means that queen is placed on a row
            corresponding to that value, i.e. ``queens[0] = 0`` means there is a queen in column ``0`` and row ``0``
        - constraints:
            - there isn't two queens on the same row, i.e. all values of an array ``queens`` should be different
            - there isn't two queens on the same column, this constraint is implicit. Since no two queens can have
                the same index in an array no two queens can be in the same column
            - there isn't two queens on the same diagonal. There are two types of diagonals: positive and negative.
                Two queens are on the same positive diagonal if their row number plus their colummn number are equal.
                In other words, ``queens[j] + j`` has the same value for two different ``j``, where ``j`` is the column
                number, i.e. for ``queens = [3, 2, 1, 0]``, ``queens[0] + 0`` mustn't be equal ``queens[1] + 1``. The
                same holds for negative diagonals as well with a difference, that ``queens[j] - j`` mustn't be the same
                for two different ``j``.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) queens can be placed on a board without them attacking each other
    """
    log.info(f"Solving N-queens problem for {board_size} queens.")
    model = cp_model.CpModel()
    queens = [model.NewIntVar(0, board_size - 1, f"x{i}") for i in range(board_size)]

    model.AddAllDifferent(queens)
    model.AddAllDifferent(queens[i] + i for i in range(board_size))
    model.AddAllDifferent(queens[i] - i for i in range(board_size))

    solver = cp_model.CpSolver()
    solution_printer = ORToolsSolutionPrinter()
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    return solution_printer.solution_count()
