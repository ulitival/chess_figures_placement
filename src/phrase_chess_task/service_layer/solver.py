"""
The module conists of solvers for the chess task.
Bishop's and rook's solver use a standardised formulas that were discovered by Vaclas Kotesovec et al.
The mathematicals formulas can be found in "Non-attacking chess pieces book 6ed" here:
    http://www.kotesovec.cz/books/kotesovec_non_attacking_chess_pieces_2013_6ed.pdf
The queen's and knight's solver are using CSP approach (CP-SAT) as there isn't a known mathematical formula that
return the number of ways they can be placed on a board.
"""
import itertools
from math import factorial, floor

from ortools.sat.python import cp_model

# http://oeis.org/A201540
_knight = [1, 6, 36, 412, 9386, 257318, 8891854, 379978716]
_knight_attack_range = [(2, 1), (-2, 1), (1, 2), (-1, 2)]


class _ORToolsSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Counts all solutions as a callback."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def solution_count(self):  # pylint: disable=missing-function-docstring
        return self.__solution_count

    def on_solution_callback(self):  # pylint: disable=missing-function-docstring
        self.__solution_count += 1


def solve_knight_hard_coded(board_size: int) -> int:
    """Hardcoded solution for knights.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) knights can be placed on a board without them attacking each other.
    Based on http://oeis.org/A201540.
    """
    return _knight[board_size - 1]


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
    ``_knight_attack_range``. Normally, a knight can attack 8 fields around itself. Although,
    due to symmetry only 4 fields are needed to cover all attack cases.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) knights can be placed on a board without them attacking each other
    """
    model = cp_model.CpModel()
    fields = [model.NewIntVar(0, 1, f"x{i}") for i in range(board_size**2)]

    model.Add(sum(fields) == board_size)
    for row, col in itertools.product(range(board_size), range(board_size)):
        for attack_range in _knight_attack_range:
            attack_row = row + attack_range[0]
            attack_col = col + attack_range[1]
            if 0 <= attack_row < board_size and 0 <= attack_col < board_size:
                field_to_constraint = row * board_size + col
                possible_attack_field = attack_row * board_size + attack_col
                model.Add(fields[field_to_constraint] + fields[possible_attack_field] < 2)

    solver = cp_model.CpSolver()
    solution_printer = _ORToolsSolutionPrinter()
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    return solution_printer.solution_count()


def solve_bishop(board_size: int) -> int:
    """Solves placement of N bishops on a NxN chess board.
    Where N == board_size.

    This solution utilises a formula that was discoverd by Vaclav Kotesovec, for more details
    please check the "Non-attacking chess pieces book 6ed" book, page 246. The link is in this module's
    description.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) bishops can be placed on a board without them attacking each other
    """
    if board_size == 1:
        return 1

    def solve_bishop_left(ind: int) -> float:
        """The function covers positive diagonals on a board.

        It corresponds to the inner left sum of the formula, see page 246 in the book.

        :param int ind: a row index
        :return float: the result for the inner left sum of the formula
        """
        sum_left = 0
        for m in range(1, board_size - ind + 1):  # pylint: disable=invalid-name
            sum_left += ((-1) ** m * m ** floor(board_size / 2) * (m + 1) ** floor((board_size + 1) / 2)) / (
                factorial(board_size - ind - m) * factorial(m)
            )
        return sum_left

    def solve_bishop_right(ind: int) -> float:
        """The function covers negative diagonals on a board.

        It corresponds to the inner right sum of the formula, see page 246 in the book.

        :param int ind: a row index
        :return float: the result for the inner right sum of the formula
        """
        sum_right = 0
        for m in range(1, ind + 1):  # pylint: disable=invalid-name
            sum_right += ((-1) ** m * m ** floor((board_size + 1) / 2) * (m + 1) ** floor(board_size / 2)) / (
                factorial(ind - m) * factorial(m)
            )
        return sum_right

    return int(
        ((-1) ** board_size) * sum(solve_bishop_left(ind) * solve_bishop_right(ind) for ind in range(1, board_size))
    )


def solve_rook(board_size: int) -> int:
    """Solves placement of N rooks on a NxN chess board.
    Where N == board_size.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) rooks can be placed on a board without them attacking each other
    """
    return factorial(board_size)


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
    model = cp_model.CpModel()
    queens = [model.NewIntVar(0, board_size - 1, f"x{i}") for i in range(board_size)]

    model.AddAllDifferent(queens)
    model.AddAllDifferent(queens[i] + i for i in range(board_size))
    model.AddAllDifferent(queens[i] - i for i in range(board_size))

    solver = cp_model.CpSolver()
    solution_printer = _ORToolsSolutionPrinter()
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    return solution_printer.solution_count()
