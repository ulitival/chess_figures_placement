from typing import Generator

import pytest
from flask.testing import FlaskClient


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    from phrase_chess_task.api.flask_app import app

    app.config.update({"TESTING": True})
    with app.test_client() as flask_client:
        yield flask_client
