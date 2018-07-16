from flask import flash, Blueprint, g, redirect, render_template, request, session, url_for, jsonify, abort
from checkit.db import get_db
import psycopg2 as pg
bp  = Blueprint('api', __name__, url_prefix='/api/v1.0')

from checkit.db import get_db

student_fields = ["anum","firstName","lastName"]
profile_fields = ["anum","preferredFirstName","firstName","lastName","pronoun"]
schedule_fields = ["session_id","name","starttime","location","length"]

@bp.route('/students/<string:anum>', methods=['GET'])
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


@bp.route('/students/<string:anum>', methods=['POST'])
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

    s = conn.commit()
    return jsonify({'sucess':'ok'}), 201
@bp.route('/students/<string:anum>', methods=['DELETE'])
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

@bp.route('/students', methods=['GET'])
def get_students():
    cur = get_db().cursor()
    cur.execute(
            "SELECT * FROM student")
    pre = cur.fetchall()
    return(tag_many("students", student_fields, pre))
@bp.route('/students', methods=['POST',"PUT",'DELETE'])
def other_students():
    abort(405)

@bp.route("/schedules/<string:anum>", methods=["GET"])
def get_schedule(anum):
    cur = get_db().cursor()
    cur.execute(
            """select se.id, se.name, starttime, location, length
                    from session se 
                    right join studentsession ss on ss.session_id = se.id 
                    inner join student s on ss.anum = s.anum 
                    where s.anum = %s 
                    order by starttime;""", (anum,))
    pre = cur.fetchall()
    return(tag_many("schedule", schedule_fields, pre))

@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": '404', "message": "file not found"}), 404

@bp.errorhandler(405)
def not_allowed(error):
    return jsonify({"error":"405", "message": "method not allowed"}), 405
def matchfield(req, record):
    def assignlmb(fi, v):
        record[fi] = v
        return fi
    updated = [assignlmb(fi, req[fi]) for fi in req.keys()]
    
    return updated

def tag_one(entity, fields, rec):
    if not rec:
        return(jsonify({"error":"404", "message":"no record found"}), 404)

    reponse = jsonify({entity: dict(zip(fields, rec))})
    return(response, 200)

def tag_many(entity, fields, recs, message="record not found"):
    if len(recs) == 0:
        return (jsonify({"error":"404", "message":message}),404)

    response = jsonify({entity:[dict(zip(fields, x)) for x in recs]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return(response, 200)

