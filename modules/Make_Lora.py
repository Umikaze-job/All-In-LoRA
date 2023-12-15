from fastapi import Request
import os
from .file_control import get_savefile_image_paths, get_savefile_image_url_paths

class Make_Lora:
    async def Image_Items(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        base,after = get_savefile_image_url_paths(folder_name)

        return {"base":base,"after":after}