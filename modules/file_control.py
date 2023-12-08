from .folder_path import get_root_folder_path
import os
import json

# setting.jsonを読み込み
def get_setting_file_json(folder_name:str):
    file_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"setting.json")
    with open(file_path,"r") as f:
        return json.load(f)

# setting.jsonに書き込み
def write_setting_file_json(folder_name:str,json_data:any):
    file_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"setting.json")
    with open(file_path,"w") as f:
        f.write(json.dumps(json_data))

# 任意のフォルダの画像ファイルのリスト
def get_image_files(folder_path):
    # フォルダ内の全てのファイルを取得
    all_files = os.listdir(folder_path)

    # 画像ファイルの拡張子
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # 画像ファイルのリストを取得
    image_files = [file for file in all_files if os.path.splitext(file)[1].lower() in image_extensions]

    return image_files