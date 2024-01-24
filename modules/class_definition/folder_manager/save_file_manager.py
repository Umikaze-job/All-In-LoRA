import datetime
import json
import os
import re
import shutil
from modules.my_exception import DuplicateException
from modules.folder_path import get_root_folder_path,get_localhost_name
from modules.file_util import get_setting_file_json,write_setting_file_json
from modules.class_definition.json_manager import SaveFilesSettingCreateManager
import glob
from PIL import Image
from fastapi import UploadFile, Form, File
import io
import random
import string
from modules.folder_path import get_savefiles

"""
SaveFileManager:savefiles/<fileName>に関する処理をするクラス
(character_trimming_folderとかimage_folderとかの処理は別のクラスがする)
"""
class SaveFileManager:
    def __init__(self,folder_id:str = "") -> None:
        print(get_root_folder_path())
        self.__savefile_path = os.path.join(get_root_folder_path(),"savefiles")
        self.folder_id = folder_id
        self.__folder_path = os.path.join(self.__savefile_path,self.folder_id)

    # 初期フォルダを作成する
    def make_folder(self,folder_name:str) -> None:
        self.folder_id = self.get_random_id()
        self.__folder_path = os.path.join(self.__savefile_path,self.folder_id)
        os.makedirs(self.__folder_path, exist_ok=True)
        self.__make_thumbnail()
        self.__make_new_folders()

        setting_manager = SaveFilesSettingCreateManager(folder_id=self.folder_id,folder_name=folder_name)
        setting_manager.create_setting_file()


    # サムネイルを変更する
    async def remake_thumbnail(self,image: UploadFile = File()) -> None:
        # ファイルを指定したフォルダに保存
        save_path = os.path.join(self.__folder_path, self.__get_thumbnail_name())
        #既存のサムネイル画像を削除する
        self.__delete_thumbnails()

        content = await image.read()
        img_bin = io.BytesIO(content)
        new_image = Image.open(img_bin).convert("RGBA")
        new_image.thumbnail((600,400))
        new_image.save(save_path)

    # フォルダの名前を変更する
    def rename_folder(self,before_name:str,after_name:str) -> None:
        
        setting_json = get_setting_file_json(self.folder_id)
        setting_json["folderData"]["name"] = after_name
        write_setting_file_json(self.folder_id,setting_json)

    # フォルダを削除する
    def delete_folder(self) -> None:
        shutil.rmtree(self.__folder_path)

    #? private
    # 指定したフォルダの中にサムネイルを作成する
    def __make_thumbnail(self) -> None:
        #既存のサムネイル画像を削除する
        self.__delete_thumbnails()
        # ソースフォルダとターゲットフォルダのパスを指定
        source_thunbnail_path_set = glob.glob(os.path.join(get_root_folder_path(),"assets","thumbnail_pre","*.png"))
        id = random.randint(0,len(source_thunbnail_path_set) - 1)
        source_thunbnail_path = source_thunbnail_path_set[id]

        if os.path.isfile(source_thunbnail_path):
            image = Image.open(source_thunbnail_path)
            image.save(os.path.join(self.__folder_path,self.__get_thumbnail_name()))

    # 指定した名前のフォルダは存在するかどうか
    def __is_folder_exists(self,input_name:str) -> bool:
        save_files_folders = os.path.join(get_root_folder_path(),"savefiles")

        return any([name == input_name for name in os.listdir(save_files_folders)])

    # 新しいフォルダを作成する。
    def __make_new_folders(self) -> None:
        folder_names = ["images_folder",
                        "character_trimming_folder",
                        "fine_tuning_folder",
                        "output_folder",
                        "thumbnail_folder",
                        "text_folder",
                        "BackUp"]
        
        for name in folder_names:
            os.makedirs(os.path.join(self.__folder_path,name))

        os.makedirs(os.path.join(self.__folder_path,"thumbnail_folder","base"))
        os.makedirs(os.path.join(self.__folder_path,"thumbnail_folder","after"))

        os.makedirs(os.path.join(self.__folder_path,"text_folder","face_detect"))

    def __get_thumbnail_name(self) -> str:
        now = datetime.datetime.now()

        # [年]_[月]_[日]_[時間] 形式の文字列を生成
        date = now.strftime("%Y_%m_%d_%H%M%S") 

        return f'thumbnail_{date}.png'
    
    # フォルダの中にあるサムネイルを削除する
    def __delete_thumbnails(self) -> None:

        thumbnail_name = list(filter(lambda name:re.compile("thumbnail.*\.png").match(name) != None,os.listdir(self.__folder_path)))

        for thumb in thumbnail_name:
            os.remove(os.path.join(self.__folder_path, thumb))

    # ランダムな16桁の英数字のIDを取得する
    def get_random_id(self) -> str:
        savefile_list = glob.glob(os.path.join(get_savefiles(),"**"))
        savefile_list = list(filter(lambda path:os.path.isdir(path),savefile_list)) #フォルダのみ取得
        savefile_list = list(map(lambda path:os.path.basename(path),savefile_list)) #フォルダ名を取得
        while True:
            characters = string.ascii_letters + string.digits  # 英字と数字を含む全ての文字
            random_string = ''.join(random.choice(characters) for i in range(16))

            newsavefile_list = list(filter(lambda name:random_string == name,savefile_list))
            if len(newsavefile_list) == 0:
                return random_string

    #指定した名前のフォルダが存在するかどうか
    @staticmethod
    def any_savefiles(folder_name:str) -> bool:
        savefiles_path = os.path.join(get_root_folder_path(),"savefiles")
        savefiles_folders = list(filter(lambda name:os.path.isdir(os.path.join(get_root_folder_path(),"savefiles",name)),os.listdir(savefiles_path)))

        return any([path == folder_name for path in savefiles_folders])
    
    @staticmethod
    def get_savefiles_folder_list() -> dict[str,list[str]]:
        savefiles_path = os.path.join(get_root_folder_path(),"savefiles")
        directories = list(filter(lambda f: os.path.isdir(os.path.join(savefiles_path, f)),os.listdir(savefiles_path)))

        # 更新日時でソート
        folder_list_id = sorted(directories, key=lambda name: get_setting_file_json(name)["date"]["Folder creation date"], reverse=True)

        # サムネイルパスを取得
        def get_path(name:str) -> str:
            file_names = glob.glob(os.path.join(get_root_folder_path(),"savefiles",name,"thumbnail*.png"))
            if len(file_names) == 0:
                raise Exception(f"Thumbnail image is missing")
            
            return os.path.join(get_localhost_name(),"savefiles",name,os.path.basename(file_names[0]))

        thumbnail_paths = list(map(get_path,folder_list_id))

        folder_list_name = list(map(lambda name:get_setting_file_json(name)["folderData"]["name"],folder_list_id))

        return {"directoriesName":folder_list_name,"thumbnail":thumbnail_paths,"directoriesId":folder_list_id}
    
    
