from fastapi.testclient import TestClient
import pytest
from typing import Any

from main import app

client = TestClient(app)

#* Folder_Select

# pytest test_main.py -m folderselectcreate -vv -s
@pytest.mark.folderselectcreate
def test_Folder_Select_Create() -> Any:
    response = client.post("/api/folder-select/create",json={
        "name":"data05",
    })
    assert response.json() == {"message": "Folder Created!!!"}

# pytest test_main.py -m folderselectrename -vv -s
@pytest.mark.folderselectrename
def test_Folder_Select_Rename() -> Any:
    response = client.post("/api/folder-select/rename",json={
        "beforeName":"data04",
        "afterName":"data05",
    })
    # assert response.json() == {"error":"Duplicate names"}
    assert response.json() == {"message": "ok"}

# processing-images 
# start-trimming

# pytest test_main.py -m trimming -vv -s
@pytest.mark.trimming
def test_Start_Trimming_Test() -> Any:
    response = client.post("/api/processing-images/start-trimming",json={
        "folderName": "data02",
        "fileName": "derestefeet03.webp",
        "setting": {
            "Character_Trimming_Data": {
                "modelname": "isnet-anime",
                "spread": 12,
                "erode_size":10,
                "foreground_threshold":180,
                "background_threshold":20
            },
            "Face_Trimming_Data":{
                "modelname":"anime-face.pt",
                "spread_top":1.8,
                "spread_left":1.5,
                "spread_right":1.5,
                "spread_bottom":1,
            },
            "Body_Trimming_Data": {
                "modelname": "anime-face.pt",
                "spread_top":1.8,
                "spread_left":1.5,
                "spread_right":1.5,
                "spread_bottom":1,
                "width_rate":2,
                "height_rate":3,
            },
            "Resize": {
                "lengthSide": 512,
                "rateLimitation": 4
            }
        },
        "isResize": True,
        "type": "Face"
    })
    assert response.json() == {"message":"OK!!!"}

#pytest -m delete_character_trimming_folder_images -vv
@pytest.mark.delete_character_trimming_folder_images
def test_delete_character_trimming_folder_images() -> Any:
    response = client.post('/test/processing-images/delete-character_trimming_folder-images',
                           json={"folderName": "data02"})
    assert response.json() == {"message":"OK!!!"}

# pytest test_main.py -m tagging -vv -s
@pytest.mark.tagging
def test_Tagging_Test() -> Any:
    response = client.post("/api/make-textfile/tagging/write",json={
        "folderName":"data02",
        "fileName":"derestefeet01.webp",
        "type":"base",
        "lotaData":{
            "triggerWord":"dereste",
            "ExcludeTags":"",
            "threshold":0.35,
            "character_threshold":0.8
        }
    })
    assert response.json() == {"message":"OK!!!"}

# pytest test_main.py -m presslora -vv -s
@pytest.mark.presslora
def test_Press_Lora_Test() -> Any:
    response = client.post("/api/make-lora/press-start-lora",json={
        "folderName":"data05",
    })
    assert response.json() == {"message":"OK!!!"}

# pytest test_main.py -m makeloramovefile -vv -s
@pytest.mark.makeloramovefile
def test_Lora_Move_File() -> Any:
    response = client.post("/test/make-lora/move-lora-file",json={
        "folderName":"data03",
        "loraName":"test01"
    })
    assert response.json() == {"message":"OK!!!"}