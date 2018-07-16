from flask import flash, Blueprint, g, redirect, render_template, request, session, url_for, jsonify, abort
from checkit.db import get_db
import psycopg2 as pg
bp  = Blueprint('api', __name__, url_prefix='/api/v1.0')

from checkit.db import get_db

student_fields = ["anum","firstName","lastName"]
profile_fields = ["anum","preferredFirstName","firstName","lastName","pronoun"]
schedule_fields = ["session_id","name","starttime","location","length"]
session_fields = ["id","name","location","starttime","length", "kind","total_seats","seats_taken"]
faculty_fields = ["id","name"]

# student methods
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

    conn.commit()
    return jsonify({'sucess':'ok'}), 201

@bp.route('/students/<string:anum>', methods=["PUT","PATCH"])
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

@bp.route('/students', methods=['POST',"PUT","PATCH",'DELETE'])
def other_students():
    abort(405)

# schedule methods
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

# session methods
@bp.route("/sessions/<string:sessionid>", methods=["GET"])
def get_session(sessionid):
    cur = get_db().cursor()
    cur.execute("""select id, name, location, starttime, length, kind, seats,
                        (select count(id) from studentsession sus where sus.session_id = se.id)
                        from session se where se.id = %s""", (int(sessionid),))
    try:
        session_basic = dict(zip(session_fields, cur.fetchone()))
    except TypeError:
        abort(404)

    cur.execute("""select fa.id, fa.name from faculty fa right join facultyteam ft on fa.id = ft.faculty_id where ft.session_id = %s""",(sessionid,))

    session_basic["faculty"] = [dict(zip(faculty_fields, r)) for r in cur.fetchall()]
    return jsonify({"session": session_basic}), 200

@bp.route("/sessions/<string:sessionid>", methods=["POST"])
def post_session(sessionid):
    js = request.json
    js["id"] = sessionid
    conn = get_db()
    cur = conn.cursor()
    if (not "seats" in js) or (js["seats"] == ""):
        js["seats"] = None
    try:
        cur.execute("INSERT INTO session(id, name, location, length, starttime, seats, kind) VALUES (%(id)s, %(name)s, %(location)s, %(length)s , %(starttime)s, %(seats)s, %(kind)s)", js)
        conn.commit()
    except pg.IntegrityError:
        return jsonify({"error":"400","message":"duplicate key"}),400

    return jsonify({"sucess":"ok"}), 201

@bp.route("/sessions/<string:sessionid>",methods=["PUT","PATCH"])
def put_session(sessionid):
    js = request.json
    conn = get_db()
    cur = conn.cursor()
    qvalues = ",".join(map(qiy, js.items()))
    cur.execute("update session set {0} where id = {1}".format(qvalues, queryify(sessionid)))
    conn.commit()
        
    return(jsonify({"status":"ok"})) 

@bp.route("/sessions/<string:sessionid>",methods=["DELETE"])
def delete_session(sessionid):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("delete from session where id = %s", (sessionid,))
        cur.execute("delete from studentsession where session_id = %s", (sessionid,))
        cur.execute("delete from facultyteam where session_id = %s", (sessionid,))
        conn.commit()
    except pg.ProgrammingError:
        abort(404)
    return jsonify({"sucess":"ok"}), 200

@bp.route("/sessions", methods=["GET"])
def get_sessions():
    cur = get_db().cursor()
    cur.execute("""select id, name, location, starttime, length, kind, seats,
                        (select count(id) from studentsession sus where sus.session_id = ss.id)
                        from session ss""")
    pre = cur.fetchall()
    return tag_many("sessions",session_fields, pre)

@bp.route("sessions", methods=["POST","PUT","PATCH","DELETE"])
def no_access_sessions():
    abort(405)

#errorhandlers
@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": '404', "message": "file not found"}), 404

@bp.errorhandler(405)
def not_allowed(error):
    return jsonify({"error":"405", "message": "method not allowed"}), 405

#helper functions
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

queryify = lambda x:{True: "'{0}'".format(x), False:str(x)}[type(x)==str]
qiy = lambda x:"{0} = {1}".format(str.lower(x[0]), queryify(x[1]))
