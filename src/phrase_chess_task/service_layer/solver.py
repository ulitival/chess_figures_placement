"""
The module conists of solvers for the chess task.
Bishop's and rook's solver use a standardised formulas that were discovered by Vaclas Kotesovec et al.
The mathematicals formulas can be found in "Non-attacking chess pieces book 6ed" here:
    http://www.kotesovec.cz/books/kotesovec_non_attacking_chess_pieces_2013_6ed.pdf
The queen's and knight's solver in using CSP approach (CP-SAT) as there isn't a known mathematical formula for that.
"""
import itertools
from math import factorial, floor

from ortools.sat.python import cp_model

# http://oeis.org/A201540
_knight = [1, 6, 36, 412, 9386, 257318, 8891854, 379978716]
_knight_attack_range = [(2, 1), (-2, 1), (1, 2), (-1, 2)]


class _ORToolsSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Calculate all solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def solution_count(self):  # pylint: disable=missing-function-docstring
        return self.__solution_count

    def on_solution_callback(self):  # pylint: disable=missing-function-docstring
        self.__solution_count += 1


def solve_knight_hard(board_size: int) -> int:
    """Hardcoded solution for knights.

    :param int board_size: size of a chess board
    :return int: number of ways we can place N (==board_size) knights on a board without
    them attacking each other.
    """
    return _knight[board_size - 1]


def solve_knight(board_size: int) -> int:
    """
    OR-Tools solution to the N-knights problem. Where N == board_size.
    This solution utilizes CSP approach using `ortools` package. Here every variable represents a field
    on a chessboard. It can have two states 0-unoccupied and 1-occupied. The solver tries to find a solution
    that sum(all_fields) == N, i.e. there are exactly N knights placed. There are also constraints that restrict
    two fileds having knights if they can attack each other. Above is defined a global constant for a knight's
    possible moves `_knight_attack_range`. We then add a constraint that two fields within a reach of knights
    on them cannot both be occupied, i.e. `fields[knight1_position] + fields[knight2_position] < 2`. Note that due
    to symmetry we only need to consider half of knight's possible attack moves thus instead of defining 8 valid moves
    we only have 4.

    :param int board_size: size of a chess board
    :return int: number of ways we can place N (==board_size) knights on a board without them attacking each others
    """
    # Creates the solver.
    model = cp_model.CpModel()
    total_number_of_fields = board_size**2
    # Creates the variables.
    fields = [model.NewIntVar(0, 1, f"x{i}") for i in range(total_number_of_fields)]

    # Creates the constraints.
    # There should be number of occupied fields equals to number of knights
    model.Add(sum(fields) == board_size)

    # Restrict fields where two knights can attack each other
    for row, col in itertools.product(range(board_size), range(board_size)):
        for attack_range in _knight_attack_range:
            attack_row = row + attack_range[0]
            attack_col = col + attack_range[1]
            if 0 <= attack_row < board_size and 0 <= attack_col < board_size:
                field_to_constraint = row * board_size + col
                possible_attack_field = attack_row * board_size + attack_col
                model.Add(fields[field_to_constraint] + fields[possible_attack_field] < 2)

    # Solve the model.
    solver = cp_model.CpSolver()
    solution_printer = _ORToolsSolutionPrinter()
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    return solution_printer.solution_count()


def solve_bishop(board_size: int) -> int:
    """Solves placement of N bishops on a NxN chess board.
    Where N == board_size.
    This solution utilises a formula that was discoverd by Vaclas Kotesovec, for more details
    please check the "Non-attacking chess pieces book 6ed" book, page 248. The link is in this module's
    description.

    :param int board_size: size of a chess board
    :return int: number of ways we can place N (==board_size) bishops on a board without them attacking each other
    """
    if board_size == 1:
        return 1

    def solve_bishop_left(ind: int) -> float:
        """This inner function correspond to the left part of the formula, see page 248 in the book,
        covering positive diagonals on a board.

        :param int ind: a row index
        :return float: the result for the left part of the formula
        """
        sum_left = 0
        for m in range(1, board_size - ind + 1):  # pylint: disable=invalid-name
            sum_left += ((-1) ** m * m ** floor(board_size / 2) * (m + 1) ** floor((board_size + 1) / 2)) / (
                factorial(board_size - ind - m) * factorial(m)
            )
        return sum_left

    def solve_bishop_right(ind: int) -> float:
        """This inner function correspond to the right part of the formula, see page 248 in the book,
        covering negative diagonals on a board.

        :param int ind: a row index
        :return float: the result for the right part of the formula
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
    :return int: number of ways we can place N (==board_size) rooks on a board without them attacking each other
    """
    return factorial(board_size)


def solve_queen(board_size: int) -> int:
    """
    OR-Tools solution to the N-queens problem. Where N == board_size.
    This solution utilizes CSP approach using `ortools` package.
    The solution for the N-queens problem can be found on the official `ortools` website here:
    https://developers.google.com/optimization/cp/queens.
    The idea is to have queens bound to every column. That will define our variables.
    The queens mustn't be in a same column, thus we define a constraint that all values for variables must
    differ. Then, there are cases with diagonals that are handled by adding addition constraints telling
    that there mustn't be two queens on a same diagona, whether it's positive or negative.

    :param int board_size: size of a chess board
    :return int: number of ways we can place N (==board_size) queens on a board without them attacking each others
    """

    # Creates the solver.
    model = cp_model.CpModel()

    # Creates the variables.
    # The array index is the column, and the value is the row.
    queens = [model.NewIntVar(0, board_size - 1, f"x{i}") for i in range(board_size)]

    # Creates the constraints.
    # All rows must be different.
    model.AddAllDifferent(queens)

    # All columns must be different because the indices of queens are all
    # different.

    # No two queens can be on the same diagonal.
    model.AddAllDifferent(queens[i] + i for i in range(board_size))
    model.AddAllDifferent(queens[i] - i for i in range(board_size))

    # Solve the model.
    solver = cp_model.CpSolver()
    solution_printer = _ORToolsSolutionPrinter()
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    return solution_printer.solution_count()
