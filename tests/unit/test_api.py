from http import HTTPStatus

from flask.testing import FlaskClient


def test_solve_endpoint_correctly_calucate_8_queens(client: FlaskClient) -> None:
    resp = client.post("/solve", json={"n": 8, "chessPiece": "queen"})
    assert resp.status_code == HTTPStatus.OK
    resp_body = resp.json
    assert "solutionsCount" in resp_body
    assert 92 == resp_body["solutionsCount"]
