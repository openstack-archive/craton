from flask import Flask

from craton.inventory.api import v1


def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1.bp, url_prefix='/v1')
    return app
