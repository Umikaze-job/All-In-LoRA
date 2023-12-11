from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_Make_TextFile_Tagging():
    response = client.post("/api/make-textfile/tagging")
    assert response.json() == {"error": "some error"}