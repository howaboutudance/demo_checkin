import os
from flask import Flask, render_template, jsonify, abort, make_response, request



def create_app(test_config=None):
    app = Flask (__name__, instance_relative_config=True)

    app.config.from_mapping(
            DATABASE = 'postgresql://checkincl:clrocks59@127.0.0.1:5432/crimson-dev',
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
    from . import apiStudent
    app.register_blueprint(apiStudent.bp)
    from . import apiSession
    app.register_blueprint(apiSession.bp)
    from . import apiSchedule
    app.register_blueprint(apiSchedule.bp)
    return app
