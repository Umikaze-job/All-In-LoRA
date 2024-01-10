import os
import glob
from typing import Any
from PIL import Image
from modules.folder_path import get_savefiles
import json
from modules.gpu_modules.tagging import do_tagging
from modules.class_definition.json_manager import SaveFilesSettingImageDataManager

"""
FolderManagerParent:画像フォルダの処理をするクラスの親クラス
"""
class FolderManagerParent:
    def __init__(self,folder_name:str,folder_path:str,url_path:str) -> None:
        self.folder_path = folder_path
        self.url_path = url_path
        self.folder_name = folder_name
        self.Image_Data_Manager:SaveFilesSettingImageDataManager

        self.image_extentions = ['jpg', 'jpeg', 'png', 'gif',"webp"]

    # フォルダ内に存在するすべての画像ファイルのURLパスを取得する
    def get_all_url_paths(self) -> list[str]:
        all_files_path = []
        # self.image_extentionsで指定した拡張子が含まれている画像をすべて取得する
        list(map(lambda ext:all_files_path.extend(glob.glob(os.path.join(self.folder_path,f'*.{ext}'))),self.image_extentions))
        all_files_name = list(map(lambda path:os.path.basename(path),all_files_path))

        return list(map(lambda name:os.path.join(self.url_path,name),all_files_name))
    
    # フォルダ内に存在するすべての画像ファイルのパスを取得する
    def get_all_image_paths(self) -> list[str]:
        all_files_path = []
        # self.image_extentionsで指定した拡張子が含まれている画像をすべて取得する
        list(map(lambda ext:all_files_path.extend(glob.glob(os.path.join(self.folder_path,f'*.{ext}'))),self.image_extentions))
        return all_files_path

    #指定した名前を持つ、ファイルの中に存在する画像のパスを取得
    def get_selected_image_path(self,name:str) -> str:
        return os.path.join(self.folder_path,name)
        
    # 追加の名前が付いたファイルパス
    def additional_named_path(self,file_path:str,addName:str) -> str:
        # 拡張子を含むファイル名からファイル名と拡張子を分割
        name, extension = os.path.splitext(os.path.basename(file_path))

        return os.path.join(self.folder_path,name + addName + extension)
    
    # 画像をフォルダに追加する
    async def Input_Image(self,image:Image.Image,file_name:str) -> None:
        pass

    # 画像ファイルを消去する
    def delete_file(self,file_name:str) -> None:
        os.remove(os.path.join(self.folder_path,file_name))

    # setting.jsonのデータを取得
    def get_setting_json(self) -> Any:
        with open(os.path.join(get_savefiles(),self.folder_name,"setting.json"),"r") as f:
            return json.load(f)
        
    def write_setting_json(self,json_data:str) -> None:
        file_path = os.path.join(get_savefiles(),self.folder_name,"setting.json")
        with open(file_path,"w") as f:
            f.write(json.dumps(json_data, indent=2))

    # タグを生成して変更する
    async def tags_generate(self,file_name:str,Tagging_Model:Any,lora_data:dict[str,Any]) -> None:
        if self.Image_Data_Manager == False:
            return
        
        file_path = os.path.join(self.folder_path,file_name)
        image = Image.open(file_path)
        # json_data["taggingData"]["---"]["file_name"]の値がfile_nameと同じ名前の連想配列があるとき
        tags = await do_tagging(image,Tagging_Model,threshold=lora_data["threshold"],character_threshold=lora_data["character_threshold"],exclude_tags=lora_data["ExcludeTags"],trigger_name=lora_data["triggerWord"]) #タグを指定
        
        self.Image_Data_Manager.change_tags(file_name=file_name,tags=tags)

    # タグを消去する
    def tags_delete(self,file_name:str) -> None:
        if self.Image_Data_Manager == False:
            return
        
        self.Image_Data_Manager.delete_tags(file_name=file_name)

    # タグ情報が入っている画像のファイル名を配列にしてすべて取得
    def all_Images_has_tags(self) -> list[str]:
        all_files_path = self.get_all_image_paths()
        all_files_path = list(map(lambda path:os.path.basename(path),all_files_path))

        result = []
        for name in all_files_path:
            # Image_Dataないに画像の名前が存在しないとき
            if self.Image_Data_Manager.is_exists_tags_data(file_name=name):
                result.append(name)

        return result
    
    #文字列で送られてくる画像タグ情報をsetting.jsonに書き込む
    #data_set:{image_url:item.str,thumbnail_path:str,file_name:str,imgtag:str}
    def str_tags_write_to_json(self,data_set:list[dict[str,Any]]) -> None:
        for data in data_set:
            imgtag = data["imgtag"].split(",")
            imgtag = list(map(lambda st:st.strip(),imgtag))

            self.Image_Data_Manager.change_tags(file_name=data["file_name"],tags=imgtag)

    # 指定した画像のタグを取得
    def get_Image_tags(self,file_name:str) -> list[str]:
        return self.Image_Data_Manager.get_tags_data(file_name=file_name)
        
    # キャプション情報が入っている画像のファイル名を配列にしてすべて取得
    def all_Images_has_caption(self) -> list[str]:
        all_files_path = self.get_all_image_paths()
        all_files_path = list(map(lambda path:os.path.basename(path),all_files_path))

        result = []
        for name in all_files_path:
            # Image_Dataないに画像の名前が存在しないとき
            if self.Image_Data_Manager.is_exists_caption_data(file_name=name):
                result.append(name)

        return result
        
    
