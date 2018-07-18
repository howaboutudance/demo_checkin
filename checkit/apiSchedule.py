from flask import flash, Blueprint, g, redirect, render_template, request, session, url_for, jsonify, abort
from checkit.apiUtils import *
from checkit.db import get_db
bp  = Blueprint('apischedule', __name__, url_prefix='/api/v1.0/schedules')

@bp.route("/<string:anum>", methods=["GET"])
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
