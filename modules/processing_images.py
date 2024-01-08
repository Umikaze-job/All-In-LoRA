import shutil
from fastapi import Request, UploadFile, Form, File
import os
import io

from .gpu_modules.edit_images.body_trimming import body_trimming
from .folder_path import get_savefiles,get_localhost_name,get_root_folder_path
from .gpu_modules.edit_images.character_trimming import character_trimming
from .gpu_modules.edit_images.face_trimming import face_trimming
from PIL import Image
import glob
import asyncio
import traceback
from typing import Any, List
import re
import math

from .class_definition.folder_manager import ImageFolderManager,CharacterTrimmingFolderManager,ThumbnailBaseFolderManager,ThumbnailAfterFolderManager

# 任意のフォルダの中にある画像ファイルの名前のリスト
def get_images_list(folder_path:str) -> list[str]:
    image_list = list(filter(lambda f:f.endswith((".jpg", ".jpeg", ".png", ".gif",".webp")),os.listdir(folder_path)))
    return list(map(lambda f:os.path.basename(f),image_list))

# 画像のファイル名を変更する_outから_resizeに変更する
def image_name_change_to_resize(path:str) -> str:
    filename,ext = os.path.splitext((os.path.basename(path)))

    filename = re.sub(r'_out$', '_resize',filename)

    return f"{filename}{ext}"

            

class Processing_Images:
    # 作業フォルダのなかにあるデータセット画像のリストを取得
    @staticmethod
    async def Input_Images(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            image_manager = ImageFolderManager(folder_name)
            base_manager = ThumbnailBaseFolderManager(folder_name)

            data_paths = image_manager.get_all_url_paths()
            thumbnail_path = base_manager.get_all_url_paths()

            return {"data_paths": data_paths,"thumbnail_path":thumbnail_path}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    # 画像をフォルダに追加する処理
    @staticmethod
    async def Set_Input_Images(file: UploadFile = File(...),folder_name:str = Form(...)) -> dict[str,str]:
        try:
            image_manager = ImageFolderManager(folder_name)
            base_manager = ThumbnailBaseFolderManager(folder_name)

            # 画像ファイルと名前を取得する
            # UploadFileからの画像の読み込みは1回しかできない
            content = await file.read()
            file_name = file.filename

            img_bin = io.BytesIO(content)
            image = Image.open(img_bin).convert("RGBA")

            await image_manager.Input_Image(image,file_name)
            await base_manager.Input_Image(image,file_name)

            return {"message": "OK"}
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    # 画像を削除する
    @staticmethod
    async def Delete_Input_Images(request:Request) -> dict[str,str]:
        try:
            data = await request.json()
            filename = data.get('fileName')
            folder_name = data.get('folderName')

            image_manager = ImageFolderManager(folder_name)
            base_manager = ThumbnailBaseFolderManager(folder_name)

            image_manager.delete_file(filename)
            base_manager.delete_file(filename)
            return {"message":f"File Deleted"}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    # 画像を加工した後の移動先のフォルダの画像の取得
    @staticmethod
    async def Output_Input_Images(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_name = data.get('folderName')

            character_trimming_manager = CharacterTrimmingFolderManager(folder_name)
            after_manager = ThumbnailAfterFolderManager(folder_name)

            image_paths = character_trimming_manager.get_all_url_paths()
            thumbnail_paths  = after_manager.get_all_url_paths()

            return {"data_paths": image_paths,"thumbnail_path":thumbnail_paths}
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    # 画像を加工した後の画像の削除
    @staticmethod
    async def Delete_Output_Images(request:Request) -> dict[str,str]:
        data = await request.json()
        folder_name = data.get('folderName')
        file_name = data.get('fileName')

        try:
            character_trimming_manager = CharacterTrimmingFolderManager(folder_name)
            after_manager = ThumbnailAfterFolderManager(folder_name)

            character_trimming_manager.delete_file(file_name)
            after_manager.delete_file(file_name)

            return {"message":"OK!!"}
        except FileNotFoundError:
            return {"error":"File Not Found"}
        except Exception as e:
            return {"error":traceback.format_exc()}
    # 
    @staticmethod
    async def Get_Backup_Images(request:Request) -> dict[str,list[Any]]:
        data = await request.json()
        folder_name = data.get('folderName')
        image_list = get_images_list(os.path.join(get_savefiles(),folder_name,"BackUp"))# 画像のパスの一覧

        return {"image_paths":[os.path.join(get_localhost_name(),"savefiles",folder_name,"BackUp",name) for name in image_list ]}
    
    @staticmethod
    async def Get_Trimming_Models(request:Request) -> dict[str,list[str]]:
        models = glob.glob(os.path.join(get_root_folder_path(),"models","face_detect_models","**"))

        models = list(map(lambda path:os.path.basename(path),models))

        return {"models":models}

    # トリミングをする
    @staticmethod
    async def Start_Trimming(request:Request) -> dict[str,str]:
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            file_name = data.get('fileName')
            setting = data.get("setting")
            type_name = data.get("type")
            is_resize = data.get("isResize")

            base_image_path = ImageFolderManager(folder_name=folder_name).get_selected_image_path(name=file_name)

            after_image_manager = CharacterTrimmingFolderManager(folder_name=folder_name)
            after_thumbnail_manager = ThumbnailAfterFolderManager(folder_name=folder_name)

            after_image_path = after_image_manager.get_selected_image_path(name=file_name)
            after_thumbnail_path = after_thumbnail_manager.get_selected_image_path(name=file_name)

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
                after_image_path = after_image_manager.additional_named_path(file_path=after_image_path,addName="_character")
                after_thumbnail_path = after_thumbnail_manager.additional_named_path(file_path=after_thumbnail_path,addName="_character")
            elif type_name == "Face":
                # ここでFace_Trimmingの処理をする
                ft_setting = setting["Face_Trimming_Data"]
                result_imgset = await face_trimming(img,base_image_path,folder_name,ft_setting)
                after_image_path = after_image_manager.additional_named_path(file_path=after_image_path,addName="_face")
                after_thumbnail_path = after_thumbnail_manager.additional_named_path(file_path=after_thumbnail_path,addName="_face")
            elif type_name == "Body":
                # ここでBody_Trimmingの処理をする
                bd_setting = setting["Body_Trimming_Data"]
                result_imgset = await body_trimming(img,base_image_path,folder_name,bd_setting)
                after_image_path = after_image_manager.additional_named_path(file_path=after_image_path,addName="_body")
                after_thumbnail_path = after_thumbnail_manager.additional_named_path(file_path=after_thumbnail_path,addName="_body")
            
            # リサイズをする必要がないときは
            if is_resize == False:
                for index,im in enumerate(result_imgset):
                    im.save(after_image_manager.additional_named_path(file_path=after_image_path,addName=str(index).rjust(3, '0')))

                    im.thumbnail((600,400))

                    im.save(after_thumbnail_manager.additional_named_path(file_name=after_thumbnail_path,addName=str(index).rjust(3, '0')),quality=50)

                    return {"message":"OK!!!"}
            
            #リサイズ処理
            temp_path = os.path.join(get_savefiles(),folder_name,"character_trimming_folder","temp")
            os.makedirs(temp_path,exist_ok=True)

            for index,im in enumerate(result_imgset):
                # 拡大する倍率を決める
                im_width,im_height = im.size
                re_setting = setting["Resize"]

                print(f"WIDTH,HEIGHT:{im_width},{im_height}")
                print(f"LENGTH_SIDE:{re_setting['lengthSide'] * 2}")
                side01 = re_setting["lengthSide"] * 2
                side02 = im_width + im_height
                rate = side01 / side02
                print(f"RATE:{rate}")
                rate = min(re_setting["rateLimitation"],round(rate))
                
                #倍率が1以下なら普通に保存する
                if rate <= 1:
                    im.save(after_image_manager.additional_named_path(file_path=after_image_path,addName=str(index).rjust(3, '0')))
                    im.thumbnail((600,400))
                    im.save(after_thumbnail_manager.additional_named_path(file_path=after_thumbnail_path,addName=str(index).rjust(3, '0')),quality=50)
                    continue

                tamp_file_name = after_image_manager.additional_named_path_for_temp(file_path=after_image_path,addName=str(index).rjust(3, '0'))
                im.save(tamp_file_name)
                # 外部ファイルのrembgで拡大する
                cmd = ["python",f"{os.path.join(get_root_folder_path(),'tools','Real-ESRGAN','inference_realesrgan.py')}",
                            "-i",tamp_file_name,
                            "-o",temp_path,
                            "-n","RealESRGAN_x4plus_anime_6B",
                            "-s",str(rate)]
                print(" ".join(cmd))
                proc = await asyncio.create_subprocess_shell(
                    " ".join(cmd),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)

                await proc.wait()

                print(os.path.join(get_root_folder_path(),'tools','Real-ESRGAN','inference_realesrgan.py'))

                # 最終的に.webpファイルにする
                resize_path = after_image_manager.additional_named_path_for_temp(file_path=f"{os.path.join(os.path.dirname(tamp_file_name),os.path.splitext(os.path.basename(tamp_file_name))[0])}.webp",addName="_out")
                # リサイズされた画像を取得する
                out_resize_path = glob.glob(os.path.join(os.path.dirname(resize_path),"**"))
                out_resize_path = list(filter(lambda path:re.match(r'.*_out\.(webp|png)$', path) != None,out_resize_path))
                if len(out_resize_path) == 0:
                    raise Exception("画像が消滅しました。")
                out_resize_path_0 = out_resize_path[0]
                # 画像をCharacter_trimming_folderに移して、サムネイルを作成する
                resize_image = Image.open(out_resize_path_0)
                resize_image.save(os.path.join(get_savefiles(),folder_name,"character_trimming_folder",image_name_change_to_resize(resize_path)))
                
                resize_image.thumbnail((600,400))

                resize_image.save(os.path.join(get_savefiles(),folder_name,"thumbnail_folder","after",image_name_change_to_resize(resize_path)),quality=50)

            shutil.rmtree(temp_path)

            return {"message":"OK!!!"}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    # テスト用処理
    # character_trimming_folderフォルダの中にある画像を消す
    @staticmethod
    async def delete_character_trimming_folder_file_Test(request:Request) -> dict[str,str]:
        data = await request.json()
        folder_name = data.get('folderName')
        images = glob.glob(os.path.join(get_savefiles(),folder_name,"character_trimming_folder","*"))

        for item in images:
            os.remove(item)

        images02 = glob.glob(os.path.join(get_savefiles(),folder_name,"thumbnail_folder","after","*"))

        for item in images02:
            os.remove(item)
        print("delete_files")
        return {"message":"OK!!!"}
