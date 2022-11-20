from http import HTTPStatus

from flask.testing import FlaskClient


def test_solve_endpoint_correctly_calucate_8_queens(client: FlaskClient) -> None:
    resp = client.post("/solve", json={"n": 8, "chessPiece": "queen"})
    assert resp.status_code == HTTPStatus.OK
    resp_body = resp.json
    assert "solutionsCount" in resp_body
    assert 92 == resp_body["solutionsCount"]  # the number 92 is based on the following data http://oeis.org/A000170


def test_solve_endpoint_invalid_chessboard_field(client: FlaskClient) -> None:
    resp_body = client.post("/solve", json={"n": 0, "chessPiece": "queen"}).json
    assert resp_body.get("code") == HTTPStatus.NOT_ACCEPTABLE
    assert resp_body.get("name").lower() == HTTPStatus.NOT_ACCEPTABLE.phrase.lower()
    assert resp_body.get("description") == "value must be at least 1 for dictionary value @ data['n']"


def test_solve_endpoint_unsupported_chess_piece(client: FlaskClient) -> None:
    resp_body = client.post("/solve", json={"n": 3, "chessPiece": "king"}).json
    assert resp_body.get("code") == HTTPStatus.NOT_ACCEPTABLE
    assert resp_body.get("name").lower() == HTTPStatus.NOT_ACCEPTABLE.phrase.lower()
    assert resp_body.get("description") == "value must be one of ['bishop', 'knight', 'queen', 'rook'] for dictionary value @ data['chessPiece']"
