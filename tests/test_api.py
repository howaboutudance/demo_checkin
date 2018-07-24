from checkit.db import get_db
from datetime import datetime
def test_students_overview(client):
    rv = client.get("/api/v1.0/students")
    json_data = rv.get_json()

    assert "students" in json_data
    assert type(json_data["students"]) == list
def test_get_student(client):
    rv = client.get("/api/v1.0/students/A4")
    json_data = rv.get_json()

    assert "student" in json_data
    assert "anum" in json_data["student"]
    assert json_data["student"]["anum"].rstrip() == "A4"
    assert json_data["student"]["firstName"] == "Adam"
def test_add_student(client):
    rv = client.post("api/v1.0/students/A6", json={"firstName":"Michael","lastName":"FitzPatrick"})
    json_data = rv.get_json()
    assert "success" in json_data

    getjson_data = client.get("api/v1.0/students").get_json()

    assert "A6" in [x["anum"].rstrip() for x in getjson_data["students"]]

def test_get_preferredname(client):
    rv = client.get("/api/v1.0/students/A5")
    json_data = rv.get_json()

    assert json_data["student"]["pronoun"] == "he/his"

def test_get_session(client):
    rv = client.get("/api/v1.0/sessions")
    json_data = rv.get_json()
    
    assert not "sessions" in json_data
def test_add_session(client):
    rv = client.post("/api/v1.0/sessions/1", json = {"name":"Orientation Seminar", "location":"SEM II B1105","starttime":datetime.now(), "length":2, "kind":"seminar"})
    json_data = rv.get_json()

    assert "success" in json_data

    getjson_data = client.get("api/v1.0/sessions").get_json()
    assert "sessions" in getjson_data
    assert "Orientation Seminar" in [x["name"] for x in getjson_data["sessions"]]

def test_login_post(client):
    rv = client.post("/api/v1.0/auth/login", json = {"username":"dota", "password":"L33t"})
    json_data = rv.get_json()
    assert "apikey" in json_data

