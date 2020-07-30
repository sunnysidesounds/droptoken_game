from flask import Flask
from . import api
from .api import models
from .support.db import db


def init_app(config):
    app = Flask(__name__)
    # load configurations
    app.config.from_object(config)
    # initialize app database
    db.init_app(app)
    # initialize api app
    api.init_app(app)

    return app