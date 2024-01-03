import os
import json
from .folder_path import get_root_folder_path

def get_user_setting_json():
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