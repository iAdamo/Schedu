#!/usr/bin/python3
"""return the status of your API
"""

from flask import Flask, make_response
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close storage
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles a JSON-formatted 404 status code response
    """
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    MGT_API_HOST = getenv('MGT_API_HOST')
    MGT_API_PORT = getenv('MGT_API_PORT')
    app.run(host=MGT_API_HOST, port=MGT_API_PORT, debug=True, threaded=True)