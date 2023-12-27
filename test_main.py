from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_Make_TextFile_Tagging():
    response = client.post("/test/mytest")
    print(response.json())
    assert response.json() == {"message": "Message Yes!!!"}

def test_Make_TextFile_Tagging02():
    response = client.post("/test/mytest",json={"chinko":"unko"})
    print(response.json())