import traceback
from fastapi import Request, UploadFile, Form
from .class_definition.save_file_manager import SaveFileManager
from .my_exception import DuplicateException
from typing import Any

class Folder_Select:
    # フォルダ作成
    @staticmethod
    async def Create(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_name = data.get('name')
            manager = SaveFileManager(folder_name)
            manager.make_folder()
            return {"message": "Folder Created!!!"}
        except DuplicateException as e:
            return {"error":"Duplicate names"}
        except Exception as e:
            return {"error":traceback.format_exc()}
    # フォルダ取得
    @staticmethod
    async def Get_Folders(request:Request) -> dict[str,Any]:
        try:
            return SaveFileManager.get_savefiles_folder_list()
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    # 名前変更
    @staticmethod
    async def Rename(request:Request) -> dict[str,str]:
        try:
            data = await request.json()
            before_name = data.get('beforeName')
            after_name = data.get('afterName')
            manager = SaveFileManager(before_name)
            manager.rename_folder(after_name)
            return {"message": "ok"}
        except DuplicateException as e:
            return {"error":"Duplicate names"}
        except FileNotFoundError:
            return {"error":"File Not Found"}
        except Exception as e:
            return {"error":traceback.format_exc()}
            
    # サムネイル設定
    @staticmethod
    async def Thumbnail(folderName: str = Form(), image: UploadFile = Form()) -> dict[str,str]:
        try:
            manager = SaveFileManager(folderName)
            await manager.remake_thumbnail(image)
            return {"message":"Thumbnails have been set up!!!!"}
        except Exception as e:
            return {"error": traceback.format_exc()}
        
    @staticmethod
    async def Delete(request:Request) -> dict[str,str]:
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            manager = SaveFileManager(folder_name)
            manager.delete_folder()
            return {"message": "Folder Deleted!!!"}
        except FileNotFoundError as e:
            return {"error":f"not found\n {e}"}
        except PermissionError as e:
            return {"error":f"PermissionError\n {e}"}
        except Exception as e:
            return {"error":traceback.format_exc()}