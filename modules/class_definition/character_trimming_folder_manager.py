import os
from .Interface.folder_manager_interface import FolderManagerParent
from ..folder_path import get_root_folder_path,get_localhost_name

"""
CharacterTrimmingFolderManager:savefiles/<fileName>/character_trimming_folderの処理や別のフォルダに画像をコピーする処理をする
また、json形式の画像データも管理する
character_trimming_folderはデータベースの画像を加工した画像を置くフォルダである
"""
class CharacterTrimmingFolderManager(FolderManagerParent):

    def __init__(self,folder_name):
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"character_trimming_folder")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"character_trimming_folder")
        super().__init__(folder_name,folder_path,url_path)

        self.Image_Data = self.get_setting_json()["Image_Data"]["after"]

    def get_all_url_paths(self):
        return super().get_all_url_paths()
    
    # タグを生成して変更する
    async def tags_generate(self,file_name:str,Tagging_Model):
        await super().tags_generate(file_name,Tagging_Model)

        json_data = self.get_setting_json()
        json_data["Image_Data"]["after"] = self.Image_Data

        self.write_setting_json(json_data)

    # タグを消去する
    def tags_delete(self,file_name:str):
        super().tags_delete(file_name=file_name)

        json_data = self.get_setting_json()
        json_data["Image_Data"]["after"] = self.Image_Data

        self.write_setting_json(json_data)