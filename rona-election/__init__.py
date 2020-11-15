from configparser import ConfigParser

import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder='static', instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import index

    app.register_blueprint(index.bp)

    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)

    return app