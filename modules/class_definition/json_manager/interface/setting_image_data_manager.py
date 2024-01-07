from typing import Any
from .savefiles_setting_manager import SaveFilesSettingJsonManager

"""
SaveFilesSettingImageDataManager:setting.jsonのデータの中にあるImage_Dataの管理をする
SaveFilesSettingImageFolderManager,SaveFilesSettingTrimmingFolderManagerの親クラスである
"""
class SaveFilesSettingImageDataManager(SaveFilesSettingJsonManager):
    def __init__(self, folder_name: str, subfoldername:str) -> None:
        super().__init__(folder_name)
        self.subFolderName = subfoldername
        self.Image_Data = self.__get_image_data()

    def __get_image_data(self) -> dict[str,Any]:
        json_data = self.get_setting_file_json()

        return json_data["Image_Data"][self.subFolderName]
    
    # タグを変更する
    def change_tags(self,file_name:str,tags:list[str]):
        # file_nameのデータが存在しない場合
        if len(list(filter(lambda data:data.get("file_name") != None and data.get("file_name") == file_name,self.Image_Data))) == 0:
            self.Image_Data.append({"file_name":file_name,"tags":tags})
            return

        # file_nameのデータが存在する場合
        for data in self.Image_Data:
            if data.get("file_name") == None or data.get("file_name") != file_name:
                continue

            data["tags"] = tags

        # jsonに書き込む
        self.__write_image_data()

    # タグを消去する
    def delete_tags(self,file_name:str):
        # file_nameのデータが存在しない場合
        if len(list(filter(lambda data:data.get("file_name") != None and data.get("file_name") == file_name,self.Image_Data))) == 0:
            return
        
        # file_nameのデータが存在する場合
        for data in self.Image_Data:
            if data.get("file_name") == None or data.get("file_name") != file_name:
                continue

            data["tags"] = [""]

        # jsonに書き込む
        self.__write_image_data()

    # 指定したファイル名のタグ情報を取得する
    def get_tags_data(self,file_name:str) -> list[str]:
        im_list = list(filter(lambda data:data.get("file_name") != None and data.get("file_name") == file_name,self.Image_Data))
        # file_nameのデータが存在しない場合
        if len(im_list) == 0:
            return [""]
        
        if im_list[0].get("tags") != None and im_list[0].get("tags") != [""]:
            return im_list[0]["tags"]
        else:
            return [""]


    # 指定したファイル名のタグ情報が存在するかどうか
    def is_exists_tags_data(self,file_name:str) -> bool:
        im_list = list(filter(lambda data:data.get("file_name") != None and data.get("file_name") == file_name,self.Image_Data))
        # file_nameのデータが存在しない場合
        if len(im_list) == 0:
            return False
        
        return im_list[0].get("tags") != None and im_list[0].get("tags") != [""]
    
    # 指定したファイル名のキャプション情報が存在するかどうか
    def is_exists_caption_data(self,file_name:str) -> bool:
        im_list = list(filter(lambda data:data.get("file_name") != None and data.get("file_name") == file_name,self.Image_Data))
        # file_nameのデータが存在しない場合
        if len(im_list) == 0:
            return False
        
        return im_list[0].get("caption") != None and im_list[0].get("caption") != [""]
    
    # 指定したファイル名のキャプション情報を取得する
    def get_caption_data(self,file_name:str) -> list[str]:
        im_list = list(filter(lambda data:data.get("file_name") != None and data.get("file_name") == file_name,self.Image_Data))
        # file_nameのデータが存在しない場合
        if len(im_list) == 0:
            return [""]
        
        if im_list[0].get("caption") != None and im_list[0].get("caption") != [""]:
            return im_list[0]["caption"]
        else:
            return [""]

    #データに書き込む
    def __write_image_data(self) -> None:
        json_data = self.get_setting_file_json()

        if json_data["Image_Data"][self.subFolderName] == self.Image_Data:
            return
        
        json_data["Image_Data"][self.subFolderName] = self.Image_Data

        self.write_setting_file_json(json_data)

