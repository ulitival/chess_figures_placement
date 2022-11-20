"""
The module defines the API main entrypoint
"""

import mimetypes
from json import dumps as jsonify

from flask import Flask
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response

from phrase_chess_task.api import log

from .v1 import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix="/v1")

# Default (latest stable) API contract version
app.register_blueprint(api_v1, name="latest")


# define an universal error handling
@app.errorhandler(HTTPException)
def error_handler(ex: HTTPException) -> Response:
    """Return JSON instead of HTML for HTTP errors."""
    data = {"code": ex.code, "name": ex.name, "description": ex.description}
    log.warning(f"There was an exception during a request processing: {data}")

    return Response(jsonify(indent=4, sort_keys=True, obj=data), ex.code, mimetype=mimetypes.types_map.get(".json"))
