import os
from flask import Flask, render_template, jsonify, abort, make_response, request


students = [
    {"anum": "A00234428",
     'firstName': 'Jeffery',
     'lastName': 'Smith',
    },{
        'anum':'A00234503',
        'firstName': 'Mike',
        'lastName': 'Schütz'
    },{
        'anum':'A00233303',
        'firstName':'Becky',
        'lastName':'Basic'
    }
]

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

    @app.route('/index')
    def index():
        return "Welcome to checkin1"
    return app
