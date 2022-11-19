"""
The module contains endpoints for the API version 1
"""

from json import dumps as jsonify

from flask import Blueprint
from flask import request as req
from flask.wrappers import Response
from werkzeug.exceptions import BadRequest

import phrase_chess_task.service_layer as solver
from phrase_chess_task.api.common import resp

api: Blueprint = Blueprint("v1", __name__)


@api.route("/solve", methods=["POST"])
def solve() -> Response:
    """
    Solves the chess problem.
    :return: the total numnber of ways `n` given chess pieces `chessPiece` can be placed on a board
    of size `n x n` can be placed without attacking each other
    """
    # TODO: add validation for n and chessPiece
    chess_board_size = req.json["n"]
    chess_piece_type = req.json["chessPiece"]
    total_number = solver.solve(chess_board_size, chess_piece_type)
    return resp(jsonify({"solutionsCount": total_number}))
