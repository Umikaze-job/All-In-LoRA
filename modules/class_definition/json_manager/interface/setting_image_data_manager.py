import os
from typing import Any,Final
from .savefiles_setting_manager import SaveFilesSettingJsonManager

"""
SaveFilesSettingImageDataManager:setting.jsonのデータの中にあるImage_Dataの管理をする
SaveFilesSettingImageFolderManager,SaveFilesSettingTrimmingFolderManagerの親クラスである
self.Image_Dataの中身は
[{"file_name":"ファイル名","tags":"画像のタグ","caption":"画像のキャプション","method":"学習方法の名前"},...]
となっている
"""
class SaveFilesSettingImageDataManager(SaveFilesSettingJsonManager):
    def __init__(self, folder_name: str, subfoldername:str) -> None:
        super().__init__(folder_name)
        self.subFolderName:Final[str] = subfoldername
        self.Image_Data = self.__get_image_data()

    def __get_image_data(self) -> list[dict[str,Any]]:
        json_data = self.get_setting_file_json()

        return json_data["Image_Data"][self.subFolderName]
    
    # タグを変更する
    def change_tags(self,file_name:str,tags:list[str]):
        # file_nameのデータが存在しない場合
        if len(list(filter(lambda data:data.get("file_name") != None and data.get("file_name") == file_name,self.Image_Data))) == 0:
            self.Image_Data.append({"file_name":file_name,"tags":tags})
            
            # jsonに書き込む
            self.__write_image_data()
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
        
    # ある画像のデータに指定したLearning_Methodの名前を書き込む
    def set_learning_method_to_data(self,file_name:str,method_name:str) -> None:
        #指定した画像のデータを取得する
        for data in self.Image_Data:
            # あったら
            if data.get("file_name") == file_name:
                data["method"] = method_name
                self.__write_image_data()
                return
        # なかったら
        self.Image_Data.append({"file_name":file_name,"method":method_name})
        self.__write_image_data()
        return
    
    # 画像パスと学習方法のセットを取得する
    #{"image_name": string, "method_name": string}[]
    #all_image_paths: Image_Folder_Managerから受け取った全ての画像パスの配列
    def get_image_path_and_learning_data(self,all_image_paths:list[str]) -> list[dict[str,str]]:
        result = []
        for image_path in all_image_paths:
            data = list(filter(lambda d:d.get("file_name") == os.path.basename(image_path) and d.get("method") != None,self.Image_Data))
            if len(data) == 0:
                result.append({"image_name":os.path.basename(image_path),"method_name":""})
            else:
                result.append({"image_name":os.path.basename(image_path),"method_name":data[0]["method"]})

        return result
        
    # 指定したLearningMethodが含まれている画像の名前を取得する
    def get_image_with_learning_method(self,method:str) -> list[str]:
        image_data = list(filter(lambda data:data.get("method") == method,self.Image_Data))

        return list(map(lambda data:data["file_name"],image_data))
    
    # 指定したLearningMethodが含まれている画像のデータを取得する
    def get_image_data_with_learning_method(self,method:str) -> list[dict[str,Any]]:
        return list(filter(lambda data:data.get("method") == method,self.Image_Data))

    #データに書き込む
    def __write_image_data(self) -> None:
        json_data = self.get_setting_file_json()

        if json_data["Image_Data"][self.subFolderName] == self.Image_Data:
            return
        
        json_data["Image_Data"][self.subFolderName] = self.Image_Data

        self.write_setting_file_json(json_data)#

