"""
The package conists of solvers for the chess task.

Bishop's and rook's solver use a standardised formulas that were discovered by Vaclas Kotesovec et al.

The queen's and knight's solver are using CSP approach (CP-SAT) as there isn't a known mathematical formula that
return the number of ways they can be placed on a board.
"""
from .bishop import solve_bishop
from .knight import solve_knight
from .queen import solve_queen
from .rook import solve_rook

chess_solvers = {"knight": solve_knight, "bishop": solve_bishop, "rook": solve_rook, "queen": solve_queen}
