import glob
import os
from ..folder_path import get_root_folder_path,get_localhost_name
from .Interface.folder_manager_interface import FolderManagerParent
from fastapi import Request, UploadFile, Form, File
import shutil
from PIL import Image

"""
ThumbnailBaseFolderManager:savefiles/<fileName>/thumbnail_folder/baseの処理や別のフォルダに画像をコピーする処理をする
images_folderはデータベースの画像を置くフォルダである
"""
class ThumbnailBaseFolderManager(FolderManagerParent):

    def __init__(self,folder_name):
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"thumbnail_folder","base")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","base")
        super().__init__(folder_name,folder_path,url_path)

    def Input_Image(self,file: UploadFile = File(...)):
        # 画像を追加する
        upload_path = super().Input_Image(file)

        #webpファイルに変える
        if os.path.basename(upload_path).endswith(".webp") == True:
            return None
        
        file_name = os.path.splitext(os.path.basename(upload_path))[0]
        print(f"UPLOAD_PATH: {upload_path}")
        image = Image.open(upload_path).convert("RGBA")
        image.thumbnail((600,400))
        image.save(os.path.join(os.path.dirname(upload_path),f"{file_name}.webp"),format="webp",quality=50)