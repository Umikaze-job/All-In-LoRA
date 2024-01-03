import datetime
import json
import os
import re
import shutil
from ..my_exception import DuplicateException
from ..folder_path import get_root_folder_path,get_localhost_name
from ..file_util import get_setting_file_json
import glob
from PIL import Image
from fastapi import UploadFile, Form, File
import io

"""
SaveFileManager:savefiles/<fileName>に関する処理をするクラス
(character_trimming_folderとかimage_folderとかの処理は別のクラスがする)
"""
class SaveFileManager:
    def __init__(self,folder_name):
        print(get_root_folder_path())
        self.__savefile_path = os.path.join(get_root_folder_path(),"savefiles")
        self.__folder_path = os.path.join(self.__savefile_path,folder_name)
        self.__folder_name = folder_name

    # 初期フォルダを作成する
    def make_folder(self):
        if self.__is_folder_exists(self.__folder_name):
            raise DuplicateException()
        else:
            os.makedirs(self.__folder_path, exist_ok=True)
            self.__make_thumbnail()
            self.__create_setting_file()
            self.__make_new_folders()

    # サムネイルを変更する
    async def remake_thumbnail(self,image: UploadFile = File()):
        # ファイルを指定したフォルダに保存
        save_path = os.path.join(self.__folder_path, self.__get_thumbnail_name())
        #既存のサムネイル画像を削除する
        self.__delete_thumbnails()

        content = await image.read()
        img_bin = io.BytesIO(content)
        image = Image.open(img_bin).convert("RGBA")
        image.thumbnail((600,400))
        image.save(save_path)

    # フォルダの名前を変更する
    def rename_folder(self,after_name):
        if self.__is_folder_exists(after_name):
            raise DuplicateException()
        
        old_path = self.__folder_path
        # 新しい名前のパスを生成
        new_path = os.path.join(self.__savefile_path,after_name)
        
        # フォルダの名前を変更
        os.rename(old_path, new_path)

    # フォルダを削除する
    def delete_folder(self):
        shutil.rmtree(self.__folder_path)

    #? private
    # 指定したフォルダの中にサムネイルを作成する
    def __make_thumbnail(self):
        #既存のサムネイル画像を削除する
        self.__delete_thumbnails()
        # ソースフォルダとターゲットフォルダのパスを指定
        source_thunbnail_path = os.path.join(get_root_folder_path(),"assets","thumbnail_pre.png")

        if os.path.isfile(source_thunbnail_path):
            image = Image.open(source_thunbnail_path)
            image.save(os.path.join(self.__folder_path,self.__get_thumbnail_name()))

    # 指定した名前のフォルダは存在するかどうか
    def __is_folder_exists(self,input_name):
        save_files_folders = os.path.join(get_root_folder_path(),"savefiles")

        return any([name == input_name for name in os.listdir(save_files_folders)])

    # setting.jsonを作成する。
    def __create_setting_file(self):
        now = datetime.datetime.now()
        # [年]_[月]_[日]_[時間] 形式の文字列を生成
        date = now.strftime("%Y_%m_%d_%H%M%S") 
        # データ内容
        settings_data = {
            "date":{
                "Folder creation date": date
            },
            "taggingData":{"base":[],"after":[]},
            "imageLearningSetting":{"image_items":{"base":[],"after":[]},"methods":[]},
            "loraData":{}
        }
        # setting.jsonのパスを作成
        setting_file_path = os.path.join(self.__folder_path, "setting.json")

        # setting.jsonを作成し、データを書き込む
        with open(setting_file_path, 'w') as file:
            json.dump(settings_data, file, indent=2)

        print(f"Setting file created at: {setting_file_path}")

    # 新しいフォルダを作成する。
    def __make_new_folders(self):
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

    def __get_thumbnail_name(self):
        now = datetime.datetime.now()

        # [年]_[月]_[日]_[時間] 形式の文字列を生成
        date = now.strftime("%Y_%m_%d_%H%M%S") 

        return f'thumbnail_{date}.png'
    
    # フォルダの中にあるサムネイルを削除する
    def __delete_thumbnails(self):

        thumbnail_name = list(filter(lambda name:re.compile("thumbnail.*\.png").match(name) != None,os.listdir(self.__folder_path)))

        for thumb in thumbnail_name:
            os.remove(os.path.join(self.__folder_path, thumb))

    #指定した名前のフォルダが存在するかどうか
    @staticmethod
    def any_savefiles(folder_name):
        savefiles_path = os.path.join(get_root_folder_path(),"savefiles")
        savefiles_folders = list(filter(lambda name:os.path.isdir(os.path.join(get_root_folder_path(),"savefiles",name)),os.listdir(savefiles_path)))

        return any([path == folder_name for path in savefiles_folders])
    
    @staticmethod
    def get_savefiles_folder_list():
        savefiles_path = os.path.join(get_root_folder_path(),"savefiles")
        directories = list(filter(lambda f: os.path.isdir(os.path.join(savefiles_path, f)),os.listdir(savefiles_path)))

        # 更新日時でソート
        directories_sorted = sorted(directories, key=lambda name: get_setting_file_json(name)["date"]["Folder creation date"], reverse=True)

        def get_path(name):
            file_names = glob.glob(os.path.join(get_root_folder_path(),"savefiles",name,"thumbnail*.png"))
            if len(file_names) == 0:
                raise Exception(f"Thumbnail image is missing")
            
            return os.path.join(get_localhost_name(),"savefiles",name,os.path.basename(file_names[0]))

        thumbnail_paths = list(map(get_path,directories_sorted))
        return {"directoriesName":directories_sorted,"thumbnail":thumbnail_paths}
    
    
