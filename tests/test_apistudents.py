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

def test_students_limit(client):
    rv = client.get("/api/v1.0/students?limit=1")
    json_data = rv.get_json()
    assert len(json_data["students"]) == 1

def test_student_offset(client):
    rv = client.get("/api/v1.0/students?offset=1")
    json_data = rv.get_json()
    assert len(json_data["students"]) == 1
