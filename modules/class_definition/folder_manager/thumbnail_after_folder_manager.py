import os
from typing import Any
from .Interface.folder_manager_interface import FolderManagerParent
from modules.folder_path import get_root_folder_path,get_localhost_name

"""
ThumbnailAfterFolderManager:savefiles/<fileName>/thumbnail_folder/afterの処理や別のフォルダに画像をコピーする処理をする
thumbnail_folder/afterはデータベースの画像を加工した画像のサムネイルを置くフォルダである
"""
class ThumbnailAfterFolderManager(FolderManagerParent):

    def __init__(self,folder_name:str) -> None:
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"thumbnail_folder","after")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","after")
        super().__init__(folder_name,folder_path,url_path)

    def get_all_url_paths(self) -> list[Any]:
        return super().get_all_url_paths()