import os
import traceback
from typing import Any
from fastapi import Request
from modules.class_definition.user_setting_manager import UserSettingManager
from modules.class_definition.folder_manager import SaveFileManager

class Welcome_Page:

    @staticmethod
    async def Sd_Models_Folder(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_path = data.get("folder_path")
            manager = UserSettingManager()
            if folder_path != "":
                manager.Sd_Model_Folder = folder_path
            result = os.path.isdir(manager.Sd_Model_Folder)
            return {"isfolder":result}
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    @staticmethod
    async def Kohyass_Folder(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_path = data.get("folder_path")
            manager = UserSettingManager()
            if folder_path != "":
                manager.Kohyass_Folder = folder_path
            result = os.path.isdir(manager.Kohyass_Folder)
            return {"isfolder":result}
        except Exception as e:
            return {"error":traceback.format_exc()}

    
    @staticmethod
    async def Lora_Folder(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_path = data.get("folder_path")
            manager = UserSettingManager()
            if folder_path != "":
                manager.Lora_Folder = folder_path
            result = os.path.isdir(manager.Lora_Folder)
            return {"isfolder":result}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    @staticmethod
    async def Init_Setting() -> dict[str,Any]:
        try:
            # フォルダパスの確認
            manager = UserSettingManager()
            path_set = [
                manager.Sd_Model_Folder,
                manager.Kohyass_Folder,
                manager.Lora_Folder
            ]
            isfolder = all(list(map(lambda path:os.path.isdir(path),path_set)))

            # 選択しているフォルダ名の取得
            folderName = manager.Select_Folder_Name
            if (SaveFileManager.any_savefiles(folder_name=folderName) == False):
                folderName = ""

            # 言語の取得
            language = manager.User_Language

            # フォルダ名の取得
            return {"isfolder":isfolder,"folderName":manager.Select_Folder_Name,"language":language}
        except Exception as e:
            return {"error":traceback.format_exc()}