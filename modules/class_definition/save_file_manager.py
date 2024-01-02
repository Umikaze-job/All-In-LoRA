import datetime
import json
import os
import re
import shutil
from ..my_exception import DuplicateException
from ..folder_path import get_root_folder_path,get_localhost_name
from ..file_util import get_setting_file_json

"""
SaveFileManager:savefiles/<fileName>に関する処理をするクラス
(character_trimming_folderとかimage_folderとかの処理は別のクラスがする)
"""
class SaveFileManager:
    def __init__(self,folder_name):
        print(get_root_folder_path())
        self.__folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name)
        self.__folder_name = folder_name

    def make_folder(self):
        if self.__is_folder_exists():
            raise DuplicateException()
        else:
            os.makedirs(self.__folder_path, exist_ok=True)
            self.make_thumbnail()
            self.__create_setting_file()
            self.__make_new_folders()

    # 指定したフォルダの中にサムネイルを作成する
    def make_thumbnail(self):
        #既存のサムネイル画像を削除する
        self.__delete_thumbnails()
        # ソースフォルダとターゲットフォルダのパスを指定
        source_thunbnail_path = os.path.join(get_root_folder_path(),"assets",self.__get_thumbnail_name())

        if os.path.isfile(source_thunbnail_path):
            shutil.copy(source_thunbnail_path,os.path.join(get_root_folder_path(),"savefiles"))

    def __is_folder_exists(self):
        save_files_folders = os.path.join(get_root_folder_path(),"savefiles")

        return any([name == self.__folder_name for name in os.listdir(save_files_folders)])

    # setting.jsonを作成する。
    def __create_setting_file(self):
        # データ内容
        settings_data = {
            "date":{
                "Folder creation date": self.__get_formatted_date
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

        return f'thumbnail_{self.__get_formatted_date}.png'
    
    # フォルダの中にあるサムネイルを削除する
    def __delete_thumbnails(self):

        thumbnail_name = list(filter(lambda name:re.compile("thumbnail.*\.png").match(name) != None,os.listdir(self.__folder_path)))

        for thumb in thumbnail_name:
            os.remove(os.path.join(self.__folder_path, thumb))

    #フォーマットされた日にちを取得する
    def __get_formatted_date():
                    # 現在の日時を取得
        now = datetime.datetime.now()

        # [年]_[月]_[日]_[時間] 形式の文字列を生成
        return now.strftime("%Y_%m_%d_%H%M%S") 

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
        thumbnail_paths = list(map(lambda name:os.path.join(get_localhost_name(),"savefiles",name),directories_sorted))
        return {"directoriesName":directories_sorted,"thumbnail":thumbnail_paths}
    
    
