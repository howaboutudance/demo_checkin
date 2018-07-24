from flask import Blueprint

from checkit.apiUtils import *
from checkit.db import get_db
bp  = Blueprint('apiAuth', __name__, url_prefix='/api/v1.0/auth')

@bp.route("/login", methods=["POST"])
def post_login():
    response = jsonify({"apikey":"lolz"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return(response, 200)
