"""
The module contains endpoints for the API version 1
"""

from json import dumps as jsonify
from typing import Any

from flask import Blueprint
from flask.wrappers import Response
from voluptuous import All, In, Range, Required, Schema

import phrase_chess_task.service_layer as solver
from phrase_chess_task.api.common import expect, resp

api: Blueprint = Blueprint("v1", __name__)


@api.route("/solve", methods=["POST"])
@expect(
    Schema(
        {
            Required("n"): All(int, Range(min=1, max=8)),
            Required("chessPiece"): All(str, In(["knight", "bishop", "rook", "queen"])),
        }
    )
)
def solve(valid_request: dict[str, Any]) -> Response:
    """
    Solves the chess problem.
    :return: the total number of ways `n` given chess pieces `chessPiece` can be placed on a board
    of size `n x n` without attacking each other
    """
    chess_board_size = valid_request["n"]
    chess_piece_type = valid_request["chessPiece"]
    total_number = solver.solve(chess_board_size, chess_piece_type)
    return resp(jsonify({"solutionsCount": total_number}))
