import psycopg2 as pg
import urllib.parse as urlparse

from flask import current_app, g

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(get_db)

def get_db():
    if 'db' not in g:
        g.db = pg.connect(parseDBURI(current_app.config["DATABASE"]))
    return g.db
def close_db(error=None):
    if hasattr(g, 'db'):
        g.db.close()

def parseDBURI(s):
    ps = urlparse.urlparse(s)
    return "user={user} password={password} dbname={dbname} host={host}".format(**{
        "user":ps.username, "password":ps.password, 
        "host":ps.hostname, "dbname":ps.path[1:]})
    
