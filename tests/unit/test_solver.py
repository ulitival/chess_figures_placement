import pytest
import time

from phrase_chess_task.service_layer import solve

knights_data = [
    (1, 1),
    (2, 6),
    (3, 36),
    (4, 412),
    (5, 9386),
    (6, 257318),
    # TODO: optimize the solution for 7x7 and 8x8 chessboard, currently CSP isn't able to solve it in a reasonable time
    # (7, 8891854),
    # (8, 379978716),
]

# http://oeis.org/A002465
bishops_data = [
    (1, 1),
    (2, 4),
    (3, 26),
    (4, 260),
    (5, 3368),
    (6, 53744),
    (7, 1022320),
    (8, 22522960),
]

# this is simply a factorial
rooks_data = [
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (7, 5040),
    (8, 40320),
]

# http://oeis.org/A000170
queens_data = [
    (1, 1),
    (2, 0),
    (3, 0),
    (4, 2),
    (5, 10),
    (6, 4),
    (7, 40),
    (8, 92),
]


@pytest.mark.parametrize("board_size, expected_number_of_ways", knights_data)
def test_solver_correctly_solves_knights(board_size: int, expected_number_of_ways: int):
    assert expected_number_of_ways == solve(board_size, "knight")


def test_solver_knights_cache_speeds_up_calculation():
    solve(6, "knight")
    time_start = time.time()
    solve(6, "knight")
    time_end = time.time()
    assert 1 > time_end - time_start


@pytest.mark.parametrize("board_size, expected_number_of_ways", bishops_data)
def test_solver_correctly_solves_bishops(board_size: int, expected_number_of_ways: int):
    assert expected_number_of_ways == solve(board_size, "bishop")


@pytest.mark.parametrize("board_size, expected_number_of_ways", rooks_data)
def test_solver_correctly_solves_rooks(board_size: int, expected_number_of_ways: int):
    assert expected_number_of_ways == solve(board_size, "rook")


@pytest.mark.parametrize("board_size, expected_number_of_ways", queens_data)
def test_solver_correctly_solves_queens(board_size: int, expected_number_of_ways: int):
    assert expected_number_of_ways == solve(board_size, "queen")
