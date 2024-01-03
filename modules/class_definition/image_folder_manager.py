import os
import glob
from ..folder_path import get_root_folder_path,get_localhost_name
from .Interface.folder_manager_interface import FolderManagerParent
from fastapi import Request, UploadFile, Form, File
from PIL import Image
import io

"""
ImageFolderManager:savefiles/<fileName>/images_folderの処理や別のフォルダに画像をコピーする処理をする
images_folderはデータベースの画像を置くフォルダである
"""
class ImageFolderManager(FolderManagerParent):

    def __init__(self,folder_name):
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"images_folder")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"images_folder")
        super().__init__(folder_name,folder_path,url_path)

    def get_all_url_paths(self):
        return super().get_all_url_paths()

    async def Input_Image(self,image:Image.Image,file_name:str):
        #webpファイルに変える
        my_file_name = os.path.splitext(os.path.basename(file_name))[0]
        image.save(os.path.join(self.folder_path,f"{my_file_name}.webp"),format="webp")
