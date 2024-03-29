import os
from typing import Any
from .Interface.folder_manager_interface import FolderManagerParent
from modules.folder_path import get_root_folder_path,get_localhost_name
from modules.class_definition.json_manager import SaveFilesSettingTrimmingFolderManager
from modules.folder_path import get_savefiles

"""
CharacterTrimmingFolderManager:savefiles/<fileName>/character_trimming_folderの処理や別のフォルダに画像をコピーする処理をする
また、json形式の画像データも管理する
character_trimming_folderはデータベースの画像を加工した画像を置くフォルダである
"""
class CharacterTrimmingFolderManager(FolderManagerParent):

    def __init__(self,folder_name:str) -> None:
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"character_trimming_folder")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"character_trimming_folder")
        super().__init__(folder_name,folder_path,url_path)

        self.Image_Data_Manager = SaveFilesSettingTrimmingFolderManager(folder_name=folder_name)

    def get_all_url_paths(self) -> list[str]:
        return super().get_all_url_paths()
    
    def get_temp_folder(self) -> str:
        return os.path.join(self.folder_path,"temp")
    
    # 追加の名前が付いたtempフォルダ上のファイルパス
    def additional_named_path_for_temp(self,file_path:str,addName:str) -> str:
        # 拡張子を含むファイル名からファイル名と拡張子を分割
        name, extension = os.path.splitext(os.path.basename(file_path))

        return os.path.join(self.get_temp_folder(),name + addName + extension)

    
