"""
The common functions and constants for two or more solvers.
"""
from ortools.sat.python import cp_model


class ORToolsSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Counts all solutions as a callback."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def solution_count(self):  # pylint: disable=missing-function-docstring
        return self.__solution_count

    def on_solution_callback(self):  # pylint: disable=missing-function-docstring
        self.__solution_count += 1
