import shutil
from fastapi import Request, UploadFile, Form, File
import os
from .folder_path import get_savefiles,get_localhost_name

# 任意のフォルダの中にある画像ファイルの名前のリスト
def get_images_list(folder_path:str):
    return [os.path.basename(f) for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg", ".png", ".gif"))]

# 任意のフォルダのなかにある画像ファイルを削除
def delete_image(file_path:str):
    # 画像ファイルの拡張子を指定
    os.remove(file_path)
            

class Processing_Images:
    # 作業フォルダのなかにあるデータセット画像のリストを取得
    async def Input_Images(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        image_list = get_images_list(os.path.join(get_savefiles(),folder_name,"images_folder"))# 画像のパスの一覧

        image_paths = [] #fastapi経由で取得するためのパスの一覧
        for image in image_list:
            image_paths.append(os.path.join(get_localhost_name(),"savefiles",folder_name,"images_folder",image))

        return {"data_paths": image_paths}
    # 画像をフォルダに追加する処理
    async def Set_Input_Images(file: UploadFile = File(...),folderName:str = Form(...)):
        # 画像を追加する
        upload_path = os.path.join(get_savefiles(),folderName,"images_folder", file.filename)
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": "OK"}
    
    # 画像を削除する
    async def Delete_Input_Images(request:Request):
        try:
            data = await request.json()
            filename = data.get('fileName')
            folderName = data.get('folderName')
            print(f"folder_name:{folderName}")
            delete_image(os.path.join(get_savefiles(),folderName,"images_folder",filename))
            return {"message":f"File Deleted"}
        except Exception as e:
            return {"error":"some error"}
        
    # 画像を加工した後の移動先のフォルダの画像の取得
    async def Output_Input_Images(request:Request):
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            image_list = get_images_list(os.path.join(get_savefiles(),folder_name,"character_trimming_folder"))# 画像のパスの一覧

            image_paths = [] #fastapi経由で取得するためのパスの一覧
            for image in image_list:
                image_paths.append(os.path.join(get_localhost_name(),"savefiles",folder_name,"character_trimming_folder",image))

            return {"data_paths": image_paths}
        except Exception as e:
            return {"error":"some error"}
        
    # 
    async def Get_Backup_Images(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        image_list = get_images_list(os.path.join(get_savefiles(),folder_name,"BackUp"))# 画像のパスの一覧

        return {"image_paths":[os.path.join(get_localhost_name(),"savefiles",folder_name,"BackUp",name) for name in image_list ]}
