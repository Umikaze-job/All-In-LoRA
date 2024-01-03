import traceback
from fastapi import Request, UploadFile, Form
from .class_definition.save_file_manager import SaveFileManager
from .my_exception import DuplicateException

class Folder_Select:
    # フォルダ作成
    async def Create(request:Request):
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
    
    async def Get_Folders(request:Request):
        try:
            return SaveFileManager.get_savefiles_folder_list()
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    # 名前変更
    async def Rename(request:Request):
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
    async def Thumbnail(folderName: str = Form(), image: UploadFile = Form()):
        try:
            manager = SaveFileManager(folderName)
            await manager.remake_thumbnail(image)
            return {"message":"Thumbnails have been set up!!!!"}
        except Exception as e:
            return {"error": traceback.format_exc()}
        
    async def Delete(request:Request):
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