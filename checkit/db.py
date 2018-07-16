import psycopg2 as pg

from flask import current_app, g

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(get_db)

def get_db():
    if 'db' not in g:
        g.db = pg.connect(dbname = "crimson-dev", user="checkincl", password="clrocks59")
    return g.db
def close_db(error=None):
    if hasattr(g, 'db'):
        g.db.close()
