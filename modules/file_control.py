from .folder_path import get_root_folder_path
import os
import json
import glob

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

# 画像フォルダのパスリストを取得
def get_savefile_image_paths(folder_name, image_extensions=['jpg', 'jpeg', 'png', 'gif']):
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