from fastapi import Request, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
import re
import json
from datetime import datetime
from .folder_path import get_localhost_name, get_root_folder_path,get_savefiles
import asyncio

from pydantic import BaseModel

def get_thumbnail_name():
        # 現在の日時を取得
    now = datetime.now()

    # [年]_[月]_[日]_[時間] 形式の文字列を生成
    formatted_date = now.strftime("%Y_%m_%d_%H%M%S") 

    return f'thumbnail_{formatted_date}.png'

# setting.jsonを作成する。
def create_setting_file(folder_path):
    # setting.jsonの内容（適宜編集してください）
    now = datetime.now()

    # [年]_[月]_[日]_[時間] 形式の文字列を生成
    formatted_date = now.strftime("%Y_%m_%d_%H%M%S") 
    # データ内容
    settings_data = {
        "date":{
            "Folder creation date": formatted_date
        },
        "taggingData":{"base":[],"after":[]},
        "imageLearningSetting":{"image_items":{"base":[],"after":[]},"methods":[]},
        "loraData":{}
    }

    # setting.jsonのパスを作成
    setting_file_path = os.path.join(folder_path, "setting.json")

    # setting.jsonを作成し、データを書き込む
    with open(setting_file_path, 'w') as file:
        json.dump(settings_data, file, indent=4)

    print(f"Setting file created at: {setting_file_path}")

# 新しいフォルダを作成する。
def make_new_folders(folder_path):
    folder_names = ["images_folder",
                    "character_trimming_folder",
                    "fine_tuning_folder",
                    "output_folder",
                    "BackUp"]
    
    for name in folder_names:
        os.makedirs(os.path.join(folder_path,name))

def get_setting_json(folder_path):
    # setting.jsonのパスを作成
    setting_file_path = os.path.join(folder_path, "setting.json")

    try:
        # setting.jsonを読み込む
        with open(setting_file_path, 'r') as file:
            settings_data = json.load(file)
            return settings_data

    except FileNotFoundError:
        print(f"Setting file not found at: {setting_file_path}")
        return None
    except KeyError:
        print("Key 'Folder creation date' not found in the setting file.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {setting_file_path}")
        return None

# 指定したフォルダの中にサムネイルを作成する
def make_thumbnail(target_folder:str):
    # ソースフォルダとターゲットフォルダのパスを指定
    source_folder = os.path.join(get_root_folder_path(),"assets")

    # ソースフォルダ内のファイルリストを取得
    files = os.listdir(source_folder)

    # 'thumbnail_pre.png' を見つけてコピー
    for file in files:
        if file == 'thumbnail_pre.png': #! 'thumbnail_pre.png'という画像を元にサムネイルを生成
            source_path = os.path.join(source_folder, file)
            target_path = os.path.join(target_folder, get_thumbnail_name())
            delete_thumbnails(target_folder)
            shutil.copyfile(source_path, target_path)

# 任意のフォルダの中にあるサムネイルのパスを取得する
def get_thumbnail_path(folder_path):
    # フォルダ内のファイル一覧を取得
    files = os.listdir(folder_path)

    # 正規表現パターンをコンパイル
    regex_pattern = re.compile(r"thumbnail_.*\.png")

    # パターンにマッチするファイルを抽出
    matching_files = [file for file in files if regex_pattern.match(file)]

    if len(matching_files) != 0:
        return matching_files[0]
    else:
        return "None"

# 各フォルダの中にあるthumbnail.pngのパスを集めた配列
def get_thumbnail_arr(folder_paths:[]):
    # 'thumbnail.png' を探してパスを収集するための空のリスト
    thumbnail_paths = []

    # 各フォルダ内の 'thumbnail.png' を探す
    for folder_path in folder_paths:
        thumbnail_paths.append(get_thumbnail_path(folder_path))

    return thumbnail_paths

# フォルダの中にあるサムネイルを削除する
def delete_thumbnails(folder_path, pattern="thumbnail.*\.png"):
    # フォルダ内のファイル一覧を取得
    files = os.listdir(folder_path)

    # 正規表現パターンをコンパイル
    regex_pattern = re.compile(pattern)

    # パターンにマッチするファイルを削除
    for file in files:
        if regex_pattern.match(file):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

# ファイル名の配列からファイルパスが入っている配列を作成する。
def get_folder_paths_from_savefiles(filenames:[]):

    # 各要素に対して os.path.join(get_root_folder_path(), 要素) を適用する
    thumbnail_paths = []
    for name in filenames:
        thumbnail_path = get_thumbnail_path(os.path.join(get_savefiles(), name))
        thumbnail_name = os.path.basename(thumbnail_path)

        thumbnail_paths.append(os.path.join(get_localhost_name(),"savefiles", name,thumbnail_name))
    
    return thumbnail_paths

# 指定したフォルダの中に指定した名前のフォルダがあるかどうか
def is_folder_exists(parent_folder, target_folder_name):
    # 指定したフォルダ内のすべてのフォルダを取得
    all_folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

    # 指定した名前のフォルダが存在するか確認
    return target_folder_name in all_folders

class Folder_Select:
    # フォルダ作成
    async def Create(request:Request):
        data = await request.json()
        folder_name = data.get('name')
        folder_path = os.path.join(get_savefiles(),folder_name)
        if is_folder_exists(get_savefiles(),folder_name):
            return {"message":"Duplicate names"}
        else:
            try:
                os.makedirs(folder_path, exist_ok=True)
                make_thumbnail(folder_path)
                create_setting_file(folder_path)
                make_new_folders(folder_path)
                return {"message": "Folder Created!!!"}
            except OSError as e:
                return {"message": "Error"}
    
    async def Get_Folders(request:Request):
        dir_path = get_savefiles()
        directories = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]

        # 更新日時でソート
        directories_sorted = sorted(directories, key=lambda f: get_setting_json(os.path.join(dir_path, f))["date"]["Folder creation date"], reverse=True)
        return {"directoriesName":directories_sorted,"thumbnail":get_folder_paths_from_savefiles(directories_sorted)}
    
    # 名前変更
    async def Rename(request:Request):
        data = await request.json()
        before_name = data.get('beforeName')
        after_name = data.get('afterName')
        if is_folder_exists(get_savefiles(), after_name):
            return {"error":"Duplicate names"}
        else:
            try:
                old_path = os.path.join(get_savefiles(),before_name)
                # 新しい名前のパスを生成
                new_path = os.path.join(get_savefiles(),after_name)
                
                # フォルダの名前を変更
                os.rename(old_path, new_path)
                return {"message": "ok"}
            except FileNotFoundError:
                return {"error":"file not found"}
            except Exception as e:
                return {"error":"some error"}
            
    # サムネイル設定
    async def Thumbnail(folderName: str = Form(), image: UploadFile = Form()):
        try:
            # ファイルを指定したフォルダに保存
            save_path = os.path.join(get_savefiles(),folderName, get_thumbnail_name())
            delete_thumbnails(os.path.join(get_savefiles(),folderName))
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            return {"message":"Thumbnails have been set up!!!!"}
        except Exception as e:
            return JSONResponse(content={"message": f"Error uploading file: {e}"}, status_code=500)
        
    async def Delete(request:Request):
        try:
            data = await request.json()
            folder_name = data.get('folderName')
            shutil.rmtree(os.path.join(get_savefiles(),folder_name))
            return {"message": "Folder Deleted!!!"}
        except FileNotFoundError:
            return {"error":"not found"}
        except PermissionError:
            return {"error":"PermissionError"}
        except Exception as e:
            return {"error":"some error"}