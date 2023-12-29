from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)

# processing-images 
# start-trimming

# pytest -m trimming -vv -s
@pytest.mark.trimming
def test_Start_Trimming_Test():
    response = client.post("/api/processing-images/start-trimming",json={
        "folderName": "data01",
        "fileName": "arknights10.webp",
        "setting": {
            "Character_Trimming_Data": {
                "modelname": "isnet-anime",
                "margin": 12,
                "erode_size":10,
                "foreground_threshold":180,
                "background_threshold":20
            },
            "Face_Trimming_Data":{
                "modelname":"anime-face.pt",
                "spread_top":30,
                "spread_left":14,
                "spread_right":14,
                "spread_bottom":8,
            },
            "Body_Trimming_Data": {
                "modelname": "anime-face.pt",
                "width_rate":2,
                "height_rate":3,
                "spread_top":30,
                "spread_left":14,
                "spread_right":14,
                "spread_bottom":8,
            },
            "Resize": {
                "lengthSide": 512,
                "rateLimitation": 4
            }
        },
        "isResize": False,
        "type": "Body"
    })
    assert response.json() == {"message":"OK!!!"}

#pytest -m delete_character_trimming_folder_images -vv
@pytest.mark.delete_character_trimming_folder_images
def test_delete_character_trimming_folder_images():
    response = client.post('/test/processing-images/delete-character_trimming_folder-images',json={"folderName": "data01"})
    assert response.json() == {"message":"OK!!!"}