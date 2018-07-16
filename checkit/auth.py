import functools
from flask import (flash, Blueprint, g, redirect, request, session, url_for, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash
from checkit.db import get_db
bp  = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        cur = get_db.cursor()
        g.user = cur.execute(
                "SELECT * FROM user WHERE id = ?", (user_id)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth:login'))
        return view(**kwargs)
    return wrapped_view
@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        error = None

        if not username:
            error = "username is required"
        elif not password:
            error = 'Password is requiredR'
        elif cur.execute("SELECT * FROM user WHERE username = ?", (username,)
                ).fetchone() is not None: 
            error = "User {} is already registered".format(username)
        if eror is None:
            cur.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)))
            cur.commit()
            return redirect(url_for('auth.login'))

        return jsonify({"error":error}), 401

    return jsonify({'register':'start'})

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

