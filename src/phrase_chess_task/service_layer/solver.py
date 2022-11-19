"""
The module conists of solvers for the chess task.
Bishop's and rook's solver use a standardised formulas that were discovered by Vaclas Kotesovec et al.
The methematicals formulas can be found in "Non-attacking chess pieces book 6ed" here:
    http://www.kotesovec.cz/books/kotesovec_non_attacking_chess_pieces_2013_6ed.pdf
The queen's and knight's solver in using CSP approach (CP-SAT) as there isn't a known mathematical formula for that.
"""

# TODO: Below are just some mocked data for now, will be replaced by a real implementation later
# Nevertheless all these solutions are valid and were posted to OEIS

# http://oeis.org/A201540
knight = [1, 6, 36, 412, 9386, 257318, 8891854, 379978716]

# http://oeis.org/A002465
bishop = [1, 4, 26, 260, 3368, 53744, 1022320, 22522960]

# simply factorial of given rooks
rook = [1, 2, 6, 24, 120, 720, 5040, 40320]

# http://oeis.org/A000170
queen = [1, 0, 0, 2, 10, 4, 40, 92]
