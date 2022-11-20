from typing import Generator

import pytest
from flask.testing import FlaskClient

from phrase_chess_task.api.flask_app import app


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    """A mocked http client provided by Flask.

    :yield Generator[FlaskClient, None, None]: a flask client for tests
    """
    app.config.update({"TESTING": True})
    with app.test_client() as flask_client:
        yield flask_client
