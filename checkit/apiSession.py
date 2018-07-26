from flask import flash, Blueprint, g, redirect, render_template, request, session, url_for, jsonify, abort
from checkit.db import get_db
from checkit.apiUtils import *
import psycopg2 as pg

from checkit.db import get_db
bp  = Blueprint('apisession', __name__, url_prefix='/api/v1.0/sessions')

session_fields = ["id","name","location","starttime","length", "kind","total_seats","seats_taken"]
faculty_fields = ["id","name"]

# session methods
@bp.route("/<string:sessionid>", methods=["GET"])
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

@bp.route("/<string:sessionid>", methods=["POST"])
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

    return jsonify({"success":"ok"}), 201

@bp.route("/<string:sessionid>",methods=["PUT","PATCH"])
def put_session(sessionid):
    js = request.json
    conn = get_db()
    cur = conn.cursor()
    qvalues = ",".join(map(qiy, js.items()))
    cur.execute("update session set {0} where id = {1}".format(qvalues, queryify(sessionid)))
    conn.commit()
        
    return(jsonify({"status":"ok"})) 

@bp.route("/<string:sessionid>",methods=["DELETE"])
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
    return jsonify({"success":"ok"}), 200

@bp.route("", methods=["GET"])
def get_sessions():
    cur = get_db().cursor()
    cur.execute("""select id, name, location, starttime, length, kind, seats,
                        (select count(id) from studentsession sus where sus.session_id = ss.id)
                        from session ss""")
    pre = cur.fetchall()
    return tag_many("sessions",session_fields, pre)

@bp.route("", methods=["POST","PUT","PATCH","DELETE"])
def no_access_sessions():
    abort(405)
#errorhandlers
@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": '404', "message": "file not found"}), 404

@bp.errorhandler(405)
def not_allowed(error):
    return jsonify({"error":"405", "message": "method not allowed"}), 405
