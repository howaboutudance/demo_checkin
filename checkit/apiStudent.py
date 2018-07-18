from flask import flash, Blueprint, g, redirect, render_template, request, session, url_for, jsonify, abort
from checkit.db import get_db
from checkit.apiUtils import *
import psycopg2 as pg

from checkit.db import get_db
bp  = Blueprint('apistudent', __name__, url_prefix='/api/v1.0/students')

student_fields = ["anum","firstName","lastName"]
profile_fields = ["anum","preferredFirstName","firstName","lastName","pronoun"]

@bp.route('/<string:anum>', methods=['GET'])
def get_student(anum):
    cur = get_db().cursor()
    cur.execute(
            """SELECT s.anum, preferredfirstname, 
                    firstname, lastname, pronouns 
                    FROM student s 
                    left join preferredname pf on s.anum = pf.anum
                    where s.anum = %s""", (anum,))
    pre = cur.fetchone()

    return tag_one("student",profile_fields, pre) 


@bp.route('/<string:anum>', methods=['POST'])
def post_student(anum):
    if not request.json or not 'firstName' in request.json:
        return jsonify(error=400, message="primary key not found"), 400
    js = request.json
    js['anum'] = anum
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO student(anum, firstName, lastName) VALUES ('{anum}','{firstName}','{lastName}')".format(**js))
    except pg.IntegrityError:
        return jsonify({"error":"400","message":"duplicate key"}),400

    conn.commit()
    return jsonify({'sucess':'ok'}), 201

@bp.route('/<string:anum>', methods=["PUT","PATCH"])
def put_students(anum):
    js = request.json
    conn = get_db()
    cur = conn.cursor()

    qvalues = ",".join(map(qiy, js.items()))

    cur.execute("update student set {0} where anum = {1}".format(qvalues, queryify(anum)))
    conn.commit()
    v = {"sucess":"ok"}
    if 'anum' in js:
        v["anum"] = anum

    return jsonify(v), 203

@bp.route('/<string:anum>', methods=['DELETE'])
def delete_student(anum):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
                "DELETE FROM student where anum = %s", (anum,))
        conn.commit()
    except pg.ProgrammingError:
        abort(404)

    return jsonify({'success':'ok'}), 200

@bp.route('', methods=['GET'])
def get_students():
    cur = get_db().cursor()
    cur.execute(
            "SELECT * FROM student")
    pre = cur.fetchall()
    return(tag_many("students", student_fields, pre))

@bp.route('/', methods=['POST',"PUT","PATCH",'DELETE'])
def other_students():
    abort(405)
#errorhandlers
@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": '404', "message": "file not found"}), 404

@bp.errorhandler(405)
def not_allowed(error):
    return jsonify({"error":"405", "message": "method not allowed"}), 405
