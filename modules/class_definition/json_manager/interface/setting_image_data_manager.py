import glob
import os
from typing import Any,Final
from .savefiles_setting_manager import SaveFilesSettingJsonManager
import random
import string

"""
SaveFilesSettingImageDataManager:setting.jsonのデータの中にあるImage_Dataの管理をする
SaveFilesSettingImageFolderManager,SaveFilesSettingTrimmingFolderManagerの親クラスである
self.Image_Dataの中身は
[{"file_name":"ファイル名(Id)","tags":"画像のタグ","caption":"画像のキャプション","method":"学習方法の名前","displayed_name":"フロントエンドに表示される名前"},...]
となっている
"""
class SaveFilesSettingImageDataManager(SaveFilesSettingJsonManager):
    def __init__(self, folder_name: str, subfoldername:str) -> None:
        super().__init__(folder_name)
        self.subFolderName:Final[str] = subfoldername
        self.Image_Data = self.get_image_data

    @property
    def get_image_data(self) -> list[dict[str,Any]]:
        json_data = self.get_setting_file_json()

        return json_data["Image_Data"][self.subFolderName]
    
    # 表示する名前のリスト
    @property
    def displayed_name_list(self) -> list[str]:
        return list(map(lambda data:data["displayed_name"],self.get_image_data))
    
    # 入力した画像の名前をランダムな16桁の英数字に変更して、file_nameとdisplayed_nameを保存する(画像が新規で入力されたらこの処理をする)
    def input_image_init(self,file_name:str,image_format:str):
        folder_id = self.get_random_id()
        self.Image_Data.append({"file_name":f"{folder_id}.{image_format}","displayed_name":os.path.splitext(file_name)[0]})

        self.__write_image_data()

        return folder_id
    
    # タグを変更する
    def change_tags(self,file_name:str,tags:list[str]) -> None:
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
    def delete_tags(self,file_name:str) -> None:
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

    # 画像データのデータIDのリストからdisplayed_nameが含まれているデータリストを取得する
    def get_image_data_with_displayed_name(self,data_list:list[str]):
        result = []
        for data in data_list:
            res_data = list(filter(lambda d:d["file_name"] == os.path.basename(data),self.Image_Data))
            if len(res_data) == 0:
                raise Exception("画像がありません")

            new_data = res_data[0]
            new_data["file_name"] = data
            result.append(new_data)

        return result

    # ある画像データを消去する
    def delete_image_data(self,file_name:str) -> None:
        self.Image_Data = list(filter(lambda data:data.get("file_name") != file_name,self.Image_Data))

        self.__write_image_data()

    #データに書き込む
    def __write_image_data(self) -> None:
        json_data = self.get_setting_file_json()

        if json_data["Image_Data"][self.subFolderName] == self.Image_Data:
            return
        
        json_data["Image_Data"][self.subFolderName] = self.Image_Data

        self.write_setting_file_json(json_data)#

    # ランダムな16桁の英数字のIDを取得する
    def get_random_id(self) -> str:
        savefile_list = list(map(lambda data:data.get("file_name"),self.get_image_data)) #フォルダIDを取得
        savefile_list = list(filter(lambda id:id != None,savefile_list)) #Noneを除く
        while True:
            characters = string.ascii_letters + string.digits  # 英字と数字を含む全ての文字
            random_string = ''.join(random.choice(characters) for i in range(16))

            newsavefile_list = list(filter(lambda name:random_string == name,savefile_list))
            if len(newsavefile_list) == 0:
                return random_string

