from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)

# processing-images 
# start-trimming

#pytest -m trimming -vv
@pytest.mark.trimming
def test_Start_Trimming_Test():
    response = client.post("/api/processing-images/start-trimming",json={
        "folderName": "data01",
        "fileName": "bluearchive0203.webp",
        "setting": {
            "Character_Trimming_Data": {
                "modelname": "isnet-anime",
                "margin": 12
            },
            "Body_Trimming_Data": {
                "modelname": "isnet-anime",
                "TransparencyThreshold": 0.3,
                "ImageSizeThreshold": 0.3,
                "margin": 14
            },
            "Resize": {
                "lengthSide": 512,
                "rateLimitation": 4
            }
        },
        "isResize": False,
        "type": "Face"
    })
    assert response.json() == {"message":"OK!!!"}

#pytest -m delete_character_trimming_folder_images -vv
@pytest.mark.delete_character_trimming_folder_images
def test_delete_character_trimming_folder_images():
    response = client.post('/test/processing-images/delete-character_trimming_folder-images',json={"folderName": "data01"})
    assert response.json() == {"message":"OK!!!"}