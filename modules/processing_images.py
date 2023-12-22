import shutil
from fastapi import Request, UploadFile, Form, File
import os
from .folder_path import get_savefiles,get_localhost_name
from .gpu_modules.edit_images.character_trimming import character_trimming
from PIL import Image
import asyncio

# 任意のフォルダの中にある画像ファイルの名前のリスト
def get_images_list(folder_path:str):
    return [os.path.basename(f) for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg", ".png", ".gif"))]

# 任意のフォルダのなかにある画像ファイルを削除
def delete_image(file_path:str):
    # 画像ファイルの拡張子を指定
    os.remove(file_path)

# 画像のファイル名が変更されている画像パス
def add_image_name_path(path,add_name):
    folder = os.path.dirname(path)
    # 拡張子を含むファイル名からファイル名と拡張子を分割
    file_name, file_extension = os.path.splitext(os.path.basename(path))

    return os.path.join(folder,file_name + add_name + file_extension)
            

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
    
    # 画像を加工した後の画像の削除
    async def Delete_Output_Images(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        file_name = data.get('fileName')

        file_path = os.path.join(get_savefiles(),folder_name,"character_trimming_folder",file_name)

        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")

            return {"message":"OK!!"}
        except FileNotFoundError:
            return {"error":"File Not Found"}
        except Exception as e:
            return {"error":e}
    # 
    async def Get_Backup_Images(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        image_list = get_images_list(os.path.join(get_savefiles(),folder_name,"BackUp"))# 画像のパスの一覧

        return {"image_paths":[os.path.join(get_localhost_name(),"savefiles",folder_name,"BackUp",name) for name in image_list ]}
    
    # トリミングをする
    async def Start_Trimming(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        file_name = data.get('fileName')
        setting = data.get("setting")
        type_name = data.get("type")
        is_resize = data.get("isResize")

        base_image_path = os.path.join(get_savefiles(),folder_name,"images_folder",file_name)
        after_image_path = os.path.join(get_savefiles(),folder_name,"character_trimming_folder",file_name)

        # 画像を開く
        img = Image.open(base_image_path)
        if type_name == "Character":
            # ここでCharacter_Trimmingの処理をする
            after_image_path = add_image_name_path(after_image_path,"_character")
            pass
        elif type_name == "Face":
            # ここでFace_Trimmingの処理をする
            after_image_path = add_image_name_path(after_image_path,"_face")
            pass
        elif type_name == "Body":
            # ここでBody_Trimmingの処理をする
            after_image_path = add_image_name_path(after_image_path,"_body")
            pass
        
        if is_resize == True:
            # ここでResizeの処理をする
            pass

        await asyncio.sleep(0.5)
        img.save(after_image_path)

        return {"message":"OK!!!"}
        for data in tags:
            image_path = os.path.join(get_savefiles(),folder_name,"images_folder",data["image_name"])
            output_path = os.path.join(get_savefiles(),folder_name,"character_trimming_folder",data["image_name"])
            print(f"array:{data['tagData']};Character in {'Character' in data['tagData']}")
            if "Character" in data["tagData"]:
                await character_trimming(image_path,output_path,setting['Character_Trimming_Data']['modelname'],setting['Character_Trimming_Data']['margin'])
            
        print(f"folder_name:{folder_name}")
        print(f"margin:{setting['Character_Trimming_Data']['margin']}")
        print(f"modelname:{setting['Character_Trimming_Data']['modelname']}")
        return {"message":"OK!!!"}
