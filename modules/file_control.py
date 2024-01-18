from typing import Any
from .folder_path import get_root_folder_path,get_localhost_name,get_savefiles
import os
import json
import glob
import random

def get_user_setting_json() -> Any:
    file_path = os.path.join(get_root_folder_path(),"user_setting.json")
    with open(file_path,"r") as f:
        return json.load(f)

# setting.jsonを読み込み
def get_setting_file_json(folder_name:str):
    file_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"setting.json")
    with open(file_path,"r") as f:
        return json.load(f)

# setting.jsonに書き込み
def write_setting_file_json(folder_name:str,json_data:any):
    file_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"setting.json")
    with open(file_path,"w") as f:
        f.write(json.dumps(json_data, indent=2))

# 画像フォルダのパスリストを取得
def get_savefile_image_paths(folder_name, image_extensions=['jpg', 'jpeg', 'png', 'gif',"webp"]):
    """
    指定されたフォルダ内の画像ファイルのパスのリストを取得する関数

    Parameters:
    - folder_path: 画像ファイルを検索するフォルダのパス
    - image_extensions: 検索する画像ファイルの拡張子のリスト

    Returns:
    - 画像ファイルのパスのリスト
    """
    base_paths = []
    after_paths = []
    
    # images_folderフォルダ内のファイルを検索
    for extension in image_extensions:
        pattern = os.path.join(get_root_folder_path(),"savefiles",folder_name,"images_folder", f'*.{extension}')
        base_paths.extend(glob.glob(pattern))

    # character_trimming_folder内のファイルを検索
    for extension in image_extensions:
        pattern = os.path.join(get_root_folder_path(),"savefiles",folder_name,"character_trimming_folder", f'*.{extension}')
        after_paths.extend(glob.glob(pattern))
    
    return base_paths, after_paths

# 画像フォルダのurlパスリストを取得
def get_savefile_image_url_paths(folder_name:str, image_extensions=['jpg', 'jpeg', 'png', 'gif',"webp"]) -> tuple[list[str],list[str]]:
    """
    指定されたフォルダ内の画像ファイルのパスのリストを取得する関数

    Parameters:
    - folder_path: 画像ファイルを検索するフォルダのパス
    - image_extensions: 検索する画像ファイルの拡張子のリスト

    Returns:
    - 画像ファイルのパスのリスト
    """
    base_paths, after_paths = get_savefile_image_paths(folder_name,image_extensions)
    base = []
    after = []
    for path in base_paths:
        name = os.path.basename(path)
        base.append(os.path.join(get_localhost_name(),"savefiles",folder_name,"images_folder", name))

    for path in after_paths:
        name = os.path.basename(path)
        after.append(os.path.join(get_localhost_name(),"savefiles",folder_name,"character_trimming_folder", name))
    
    return base, after

def get_thumbnail_url_paths(folder_name:str):
    
    # "images_folder""character_trimming_folder"の中にある画像のパスのリストを取得
    base_files = glob.glob(os.path.join(get_savefiles(),folder_name,"thumbnail_folder","base",f"*{['jpg', 'jpeg', 'png', 'gif','webp']}"))
    after_files = glob.glob(os.path.join(get_savefiles(),folder_name,"thumbnail_folder","after",f"*{['jpg', 'jpeg', 'png', 'gif','webp']}"))

    # すべての要素をファイル名に変換する
    base_files = list(map(lambda path:os.path.basename(path),base_files))
    after_files = list(map(lambda path:os.path.basename(path),after_files))

    # すべての要素をURLパスにする
    base_files = list(map(lambda name:os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","base",name),base_files))
    after_files = list(map(lambda name:os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","after",name),after_files))

    return base_files,after_files


def make_random_tags(num=10) -> list[str]:
    anime_female_characters = ["Sakura", "Hinata", "Asuka", "Mikasa", "ZeroTwo", "Rem", "Nezuko", "Kagome", "Nami", "Lucy",
                            "Erza", "Bulma", "Hinamori", "Rukia", "Sango", "Ino", "Kallen", "Rei", "Winry", "Riza",
                            "Yoruichi", "Faye", "Mai", "C.C.", "Momo", "Holo", "Kushina", "Aqua", "Saber", "Kagura",
                            "Tsunade", "Rias", "Yukino", "Yoko", "Misa", "Ryuko", "Yui", "Kallen", "Anna", "Inori",
                            "Misato", "Shinobu", "Ultear", "Mitsuri", "Toga", "Nico", "Tsukasa", "Miyuki", "Yumeko",
                            "Satsuki", "Yachiyo", "Erina", "Yukino", "Akeno", "Kiyoko", "Homura", "Kyoka", "Tohru"]
    
    return random.sample(anime_female_characters,num)