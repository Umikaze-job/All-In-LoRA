import shutil
from fastapi import Request, UploadFile, Form, File
import os

from .gpu_modules.edit_images.body_trimming import body_trimming
from .folder_path import get_savefiles,get_localhost_name,get_root_folder_path
from .file_control import get_savefile_image_url_paths,get_thumbnail_url_paths
from .gpu_modules.edit_images.character_trimming import character_trimming
from .gpu_modules.edit_images.face_trimming import face_trimming
from PIL import Image
import glob
import asyncio
import traceback
from typing import List

# 任意のフォルダの中にある画像ファイルの名前のリスト
def get_images_list(folder_path:str):
    image_list = list(filter(lambda f:f.endswith((".jpg", ".jpeg", ".png", ".gif",".webp")),os.listdir(folder_path)))
    return list(map(lambda f:os.path.basename(f),image_list))

# 画像のファイル名が変更されている画像パス
def add_image_name_path(path,add_name) -> str:
    folder = os.path.dirname(path)
    # 拡張子を含むファイル名からファイル名と拡張子を分割
    file_name, file_extension = os.path.splitext(os.path.basename(path))

    return os.path.join(folder,file_name + add_name + file_extension)
            

class Processing_Images:
    # 作業フォルダのなかにあるデータセット画像のリストを取得
    async def Input_Images(request:Request):
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            image_paths,_ = get_savefile_image_url_paths(folder_name)
            thumbnail_paths,_ = get_thumbnail_url_paths(folder_name)

            return {"data_paths": image_paths,"thumbnail_path":thumbnail_paths}
        except Exception as e:
            return {"error":traceback.format_exc()}
    # 画像をフォルダに追加する処理
    async def Set_Input_Images(file: UploadFile = File(...),folderName:str = Form(...)):
        try:
            # 画像を追加する
            upload_path = os.path.join(get_savefiles(),folderName,"images_folder", file.filename)
            with open(upload_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            file_name, extension = os.path.splitext(upload_path)
            thumbnail_path = os.path.join(get_savefiles(),folderName,"thumbnail_folder","base", file.filename)
            if extension != ".webp":
                image = Image.open(upload_path).convert("RGBA")
                image.save(file_name + ".webp", "webp")

                os.remove(upload_path)

                image.thumbnail((600,400))

                thumbnail_folder,_ = os.path.splitext(thumbnail_path)
                image.save(thumbnail_folder + ".webp",quality=50,format="webp")
            else:
                image = Image.open(upload_path).convert("RGBA")

                image.thumbnail((600,400))

                image.save(thumbnail_path,quality=50,format="webp")

            return {"message": "OK"}
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    # 画像を削除する
    async def Delete_Input_Images(request:Request):
        try:
            data = await request.json()
            filename = data.get('fileName')
            folderName = data.get('folderName')
            os.remove(os.path.join(get_savefiles(),folderName,"images_folder",filename))
            os.remove(os.path.join(get_savefiles(),folderName,"thumbnail_folder","base",filename))
            return {"message":f"File Deleted"}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    # 画像を加工した後の移動先のフォルダの画像の取得
    async def Output_Input_Images(request:Request):
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            _,image_paths = get_savefile_image_url_paths(folder_name)
            _,thumbnail_paths  = get_thumbnail_url_paths(folder_name)

            return {"data_paths": image_paths,"thumbnail_path":thumbnail_paths}
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    # 画像を加工した後の画像の削除
    async def Delete_Output_Images(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        file_name = data.get('fileName')

        file_path = os.path.join(get_savefiles(),folder_name,"character_trimming_folder",file_name)
        thumbnail_path = os.path.join(get_savefiles(),folder_name,"thumbnail_folder","after",file_name)

        try:
            os.remove(file_path)
            os.remove(thumbnail_path)

            return {"message":"OK!!"}
        except FileNotFoundError:
            return {"error":"File Not Found"}
        except Exception as e:
            return {"error":traceback.format_exc()}
    # 
    async def Get_Backup_Images(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        image_list = get_images_list(os.path.join(get_savefiles(),folder_name,"BackUp"))# 画像のパスの一覧

        return {"image_paths":[os.path.join(get_localhost_name(),"savefiles",folder_name,"BackUp",name) for name in image_list ]}
    
    async def Get_Trimming_Models(request:Request):
        models = glob.glob(os.path.join(get_root_folder_path(),"models","face_detect_models","**"))

        models = list(map(lambda path:os.path.basename(path),models))

        return {"models":models}

    # トリミングをする
    async def Start_Trimming(request:Request):
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            file_name = data.get('fileName')
            setting = data.get("setting")
            type_name = data.get("type")
            is_resize = data.get("isResize")

            base_image_path = os.path.join(get_savefiles(),folder_name,"images_folder",file_name)
            after_image_path = os.path.join(get_savefiles(),folder_name,"character_trimming_folder",file_name)
            after_thumbnail_path = os.path.join(get_savefiles(),folder_name,"thumbnail_folder","after",file_name)

            # 画像を開く
            img = Image.open(base_image_path)
            result_imgset:List[Image.Image] = []
            if type_name == "Character":
                # ここでCharacter_Trimmingの処理をする
                ch_setting = setting["Character_Trimming_Data"]
                img = await character_trimming(img,ch_setting)
                if type(img) == "Exception":
                    raise Exception(img)
                result_imgset.append(img)
                after_image_path = add_image_name_path(after_image_path,"_character")
                after_thumbnail_path = add_image_name_path(after_thumbnail_path,"_character")
            elif type_name == "Face":
                # ここでFace_Trimmingの処理をする
                ft_setting = setting["Face_Trimming_Data"]
                result_imgset = await face_trimming(img,base_image_path,folder_name,ft_setting)
                after_image_path = add_image_name_path(after_image_path,"_face")
                after_thumbnail_path = add_image_name_path(after_thumbnail_path,"_face")
            elif type_name == "Body":
                # ここでBody_Trimmingの処理をする
                bd_setting = setting["Body_Trimming_Data"]
                result_imgset = await body_trimming(img,base_image_path,folder_name,bd_setting)
                after_image_path = add_image_name_path(after_image_path,"_body")
                after_thumbnail_path = add_image_name_path(after_thumbnail_path,"_body")
            
            if is_resize == True:
                # ここでResizeの処理をする
                pass

            for index,im in enumerate(result_imgset):
                print(f"{add_image_name_path(after_image_path,str(index).rjust(3, '0'))}======model")
                im.save(add_image_name_path(after_image_path,str(index).rjust(3, '0')))

                im.thumbnail((600,400))

                im.save(add_image_name_path(after_thumbnail_path,str(index).rjust(3, '0')),quality=50)

            return {"message":"OK!!!"}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    # テスト用処理
    # character_trimming_folderフォルダの中にある画像を消す
    async def delete_character_trimming_folder_file_Test(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        images = glob.glob(os.path.join(get_savefiles(),folder_name,"character_trimming_folder","*"))

        for item in images:
            os.remove(item)
        print("delete_files")
        return {"message":"OK!!!"}
