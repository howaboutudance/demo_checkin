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
    @app.route('/api/v1.0/students', methods=['GET'])
    def get_students():
        return jsonify({"students": students})

    @app.route('/api/v1.0/student/<string:anum>', methods=['GET'])
    def get_student(anum):
        student = [student for student in students if student['anum'] == anum]
        if len(student) == 0:
            abort(404)
        return jsonify({"student":student[0]})

    @app.route('/api/v1.0/student/', methods=['POST'])
    def set_student():
        if not request.json or not 'anum' in request.json:
            abort(400)

        student = {
                'anum':request.json['anum'], 
                'firstName':request.json['firstName'], 
                'lastName':request.json['lastName']
        }


        students.append(student)
        return jsonify({'student':student}), 201

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": 'not found'})

    return app
def matchfield(req, record):
    def assignlmb(fi, v):
        record[fi] = v
        return fi
    updated = [assignlmb(fi, req[fi]) for fi in req.keys()]
    return updated
