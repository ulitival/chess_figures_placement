"""N-bishop solver.

Based on mathematical formulas discovered by Vaclav Kotesovec and described
in his book "Non-attacking chess pieces book 6ed":
http://www.kotesovec.cz/books/kotesovec_non_attacking_chess_pieces_2013_6ed.pdf

The N-bishop problem is covered on page 242. The formula that was used for
the calculation can be found on page 246 (the first one on the page).
"""
from math import factorial, floor

from phrase_chess_task.service_layer import log


def solve_bishop(board_size: int) -> int:
    """Solves placement of N bishops on a NxN chess board.
    Where N == board_size.

    This solution utilises a formula that was discoverd by Vaclav Kotesovec, for more details
    please check the "Non-attacking chess pieces book 6ed" book, page 246. The link is in this module's
    description.

    :param int board_size: size of a chess board
    :return int: number of ways N (==board_size) bishops can be placed on a board without them attacking each other
    """
    log.info(f"Solving N-bishops problem for {board_size} bishops.")
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
