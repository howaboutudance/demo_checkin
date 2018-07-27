from flask import flash, Blueprint, g, redirect, render_template, request, session, url_for, jsonify, abort
from checkit.db import get_db
from checkit.apiUtils import *
import psycopg2 as pg

from checkit.db import get_db
bp  = Blueprint('apiforms', __name__, url_prefix='/api/v1.0/forms')

form_fields = {"id","name","schema","uischema"}
@bp.route("/<string:name>", methods=["GET"])
def get_form(name):
    cur = get_db().cursor()
    cur.execute("SElECT id, name, schema from form where name = %s", (name,))
    pre = cur.fetchone()
    return(tag_one("form", form_fields, pre))

