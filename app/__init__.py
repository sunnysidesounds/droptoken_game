from flask import Flask
from . import api
from .api import models
from .support.db import db


def init_app(config):
    app = Flask(__name__, template_folder='./assets/templates', static_url_path=None)
    app.static_url_path = "/assets"
    app.static_folder = app.root_path + app.static_url_path
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    # load configurations
    app.config.from_object(config)
    # initialize app database
    db.init_app(app)
    # initialize api app
    api.init_app(app)

    return app