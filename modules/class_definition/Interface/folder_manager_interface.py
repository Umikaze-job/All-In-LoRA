import os
import glob
from fastapi import Request, UploadFile, Form, File
import shutil
from PIL import Image

"""
FolderManagerParent:画像フォルダの処理をするクラスの親クラス
"""
class FolderManagerParent:
    def __init__(self,folder_name,folder_path,url_path):
        self.folder_path = folder_path
        self.url_path = url_path
        self.folder_name = folder_name

        self.image_extentions = ['jpg', 'jpeg', 'png', 'gif',"webp"]

    # フォルダ内に存在するすべての画像ファイルを取得する
    def get_all_url_paths(self):
        all_files_path = []
        list(map(lambda ext:all_files_path.extend(glob.glob(os.path.join(self.folder_path,f'*.{ext}'))),self.image_extentions))
        all_files_name = list(map(lambda path:os.path.basename(path),all_files_path))

        return list(map(lambda name:os.path.join(self.url_path,name),all_files_name))
    
    # 画像をフォルダに追加する
    def Input_Image(self,file: UploadFile = File(...)) -> str:
        upload_path = os.path.join(self.folder_path, file.filename)
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return upload_path
