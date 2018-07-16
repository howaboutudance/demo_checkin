import os
from flask import Flask, render_template, jsonify, abort, make_response, request



def create_app(test_config=None):
    app = Flask (__name__, instance_relative_config=True)

    app.config.from_mapping(
            SECRET_key = 'dev')

    if test_config is None:
        app.config.from_pyfile('config.pg', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)
    from . import api
    app.register_blueprint(api.bp)
    return app
