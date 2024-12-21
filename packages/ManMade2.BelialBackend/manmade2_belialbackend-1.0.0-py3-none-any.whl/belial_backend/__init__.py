from flask import Flask
from .api import assets_blueprint
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(assets_blueprint, url_prefix="/api/v1")

    return app
