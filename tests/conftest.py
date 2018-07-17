import os

import pytest
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
    app = create_app({
        'TESTING': True,
        'DATABASE': test_db()
    })

    yield app

    test_db.close()

@pytest.fixture()
def client(app):
    return app.test_client

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
    
