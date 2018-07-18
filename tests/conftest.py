import os

import pytest
import checkit
from checkit import create_app

from flask import g

import psycopg2 as pg

TEST_DATABASE = "checkit-testing"
TEST_USER = "checkincl"
TEST_PASSWORD = "clrocks59"

# sql loading -- skipped
def init_db():
    test_db = pg.connect(dbname = TEST_DATABASE, user = TEST_USER, password = TEST_PASSWORD)
    return test_db
 
@pytest.fixture
def app():
    test_db = init_db()

    cur = test_db.cursor()
    with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'r') as f:
        cur.execute(f.read())

    test_db.commit()

    app = create_app({
        'TESTING': True,
        'DATABASE': 'postgresql://checkincl:clrocks59@127.0.0.1:5432/checkit-testing'
    })

    yield app

    test_db.close()

@pytest.fixture()
def client(app):
    client = app.test_client()

    yield client

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
    
