import os
from .Interface.folder_manager_interface import FolderManagerParent
from ..folder_path import get_root_folder_path,get_localhost_name

"""
CharacterTrimmingFolderManager:savefiles/<fileName>/character_trimming_folderの処理や別のフォルダに画像をコピーする処理をする
character_trimming_folderはデータベースの画像を加工した画像を置くフォルダである
"""
class CharacterTrimmingFolderManager(FolderManagerParent):

    def __init__(self,folder_name):
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"character_trimming_folder")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"character_trimming_folder")
        super().__init__(folder_name,folder_path,url_path)

    def get_all_url_paths(self):
        return super().get_all_url_paths()