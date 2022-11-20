"""N-knights solver.

Based on CSP approach. The solver utilizes a combinaton of CSP and hard-coded values,
as for higher chessboard sizes the CSP solver isn't able to finish within reasonable
time.
"""
import itertools

from ortools.sat.python import cp_model

from phrase_chess_task.service_layer import log

from .common import ORToolsSolutionPrinter

# http://oeis.org/A201540
KNIGHT = [1, 6, 36, 412, 9386, 257318, 8891854, 379978716]
KNIGHT_ATTACK_RANGE = [(2, 1), (-2, 1), (1, 2), (-1, 2)]


def _solve_knight_hard_coded(board_size: int) -> int:
    """Hardcoded solution for knights.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) knights can be placed on a board without them attacking each other.
    Based on http://oeis.org/A201540.
    """
    log.info(f"For N={board_size} CSP will take too much time. Falling back to hardcoded solution.")
    return KNIGHT[board_size - 1]


def solve_knight(board_size: int) -> int:
    """OR-Tools solution to the N-knights problem. Where N == board_size.

    This solution utilizes a CSP approach using ``ortools`` package. The definition is the following:
        - variables: ``fields`` on a chessboard, the number of variables is ``board_size x board_size``
        - domain: ``[0, 1]``, 0 for unoccupied field, 1 for occupied
        - constraints:
            - there are exactly N knights placed on a chessboard: ``sum(fields) == N``,
            - there are not any pair of knights that are within reach of each other, that is to say,
                all fields are occupied in such a way that N knights cannot attack one another. This
                constraint is defined by utilising the following fact:
                ``fields[knight1_position] + fields[knight2_position] < 2``

    For calculating possible fields where knights can attack there is defined a global constants
    ``KNIGHT_ATTACK_RANGE``. Normally, a knight can attack 8 fields around itself. Although,
    due to symmetry only 4 fields are needed to cover all attack cases.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) knights can be placed on a board without them attacking each other
    """
    log.info(f"Solving N-knights problem for {board_size} knights.")
    if board_size in {7, 8}:
        return _solve_knight_hard_coded(board_size)

    model = cp_model.CpModel()
    fields = [model.NewIntVar(0, 1, f"x{i}") for i in range(board_size**2)]

    model.Add(sum(fields) == board_size)
    for row, col in itertools.product(range(board_size), range(board_size)):
        for attack_range in KNIGHT_ATTACK_RANGE:
            attack_row = row + attack_range[0]
            attack_col = col + attack_range[1]
            if 0 <= attack_row < board_size and 0 <= attack_col < board_size:
                field_to_constraint = row * board_size + col
                possible_attack_field = attack_row * board_size + attack_col
                model.Add(fields[field_to_constraint] + fields[possible_attack_field] < 2)

    solver = cp_model.CpSolver()
    solution_printer = ORToolsSolutionPrinter()
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    return solution_printer.solution_count()
