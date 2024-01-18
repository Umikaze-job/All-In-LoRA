from .folder_select import Folder_Select
from .Make_Lora import Make_Lora
from .Make_TextFile import Make_TextFile
from .processing_images import Processing_Images
from .welcome_page import Welcome_Page
from fastapi import Request
from modules.class_definition.user_setting_manager import UserSettingManager

__all__ = ["Folder_Select","Make_Lora","Make_TextFile","Processing_Images","Welcome_Page","TopbarManager"]

class TopbarManager:
    @staticmethod
    async def Set_Language(request:Request) -> None:
        try:
            data = await request.json()
            language = data.get('language')
            UserSettingManager().User_Language = language
        except Exception as e:
            print(e)