import os
from fastapi import Request
from modules.class_definition.user_setting_manager import UserSettingManager

class Welcome_Page:

    @staticmethod
    async def Sd_Models_Folder(request:Request) -> dict[str,bool]:
        data = await request.json()
        folder_path = data.get("folder_path")
        manager = UserSettingManager()
        if folder_path != "":
            manager.Sd_Model_Folder = folder_path
        result = os.path.isdir(manager.Sd_Model_Folder)
        return {"isfolder":result}
    
    @staticmethod
    async def Kohyass_Folder(request:Request) -> dict[str,bool]:
        data = await request.json()
        folder_path = data.get("folder_path")
        manager = UserSettingManager()
        if folder_path != "":
            manager.Kohyass_Folder = folder_path
        result = os.path.isdir(manager.Kohyass_Folder)
        return {"isfolder":result}
    
    @staticmethod
    async def Lora_Folder(request:Request) -> dict[str,bool]:
        data = await request.json()
        folder_path = data.get("folder_path")
        manager = UserSettingManager()
        if folder_path != "":
            manager.Lora_Folder = folder_path
        result = os.path.isdir(manager.Lora_Folder)
        return {"isfolder":result}