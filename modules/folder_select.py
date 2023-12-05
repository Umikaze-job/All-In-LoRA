from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse
import asyncio
import os
import shutil

from pydantic import BaseModel

def get_root_folder_path():
    # 現在のファイル（このスクリプト）のディレクトリを取得
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    # ルートフォルダのパスを取得
    root_folder_path = os.path.abspath(os.path.join(current_script_directory, ".."))

    return root_folder_path

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
            target_path = os.path.join(target_folder, 'thumbnail.png')
            shutil.copyfile(source_path, target_path)

# 各フォルダの中にあるthumbnail.pngのパスを集めた配列
def get_thumbnail_arr(folder_paths:[]):
    # 'thumbnail.png' を探してパスを収集するための空のリスト
    thumbnail_paths = []

    # 各フォルダ内の 'thumbnail.png' を探す
    for folder_path in folder_paths:
        thumbnail_path = os.path.join(folder_path, 'thumbnail.png')
        
        # 'thumbnail.png' が存在する場合、リストに追加
        if os.path.exists(thumbnail_path):
            thumbnail_paths.append(thumbnail_path)

    return thumbnail_paths

# ファイル名の配列からファイルパスが入っている配列を作成する。
def get_folder_paths_from_savefiles(filenames:[]):

    # 各要素に対して os.path.join(get_root_folder_path(), 要素) を適用する
    
    return [os.path.join(f"http://localhost:8000","savefiles", s,"thumbnail.png") for s in filenames]

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
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name)
        if is_folder_exists(os.path.join(get_root_folder_path(),"savefiles"),folder_name):
            return {"message":"Duplicate names"}
        else:
            try:
                os.makedirs(folder_path, exist_ok=True)
                make_thumbnail(folder_path)
                return {"message": "Folder Created!!!"}
            except OSError as e:
                return {"message": "Error"}
    
    async def Get_Folders(request:Request):
        dir_path = os.path.join(get_root_folder_path(),"savefiles")
        directories = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]

        # 更新日時でソート
        directories_sorted = sorted(directories, key=lambda f: os.path.getmtime(os.path.join(dir_path, f)), reverse=True)
        return {"directoriesName":directories_sorted,"thumbnail":get_folder_paths_from_savefiles(directories_sorted)}
    
    # 名前変更
    async def Rename(request:Request):
        data = await request.json()
        before_name = data.get('beforeName')
        after_name = data.get('afterName')
        if is_folder_exists(os.path.join(get_root_folder_path(),"savefiles"), after_name):
            return {"error":"Duplicate names"}
        else:
            try:
                old_path = os.path.join(get_root_folder_path(),"savefiles",before_name)
                # 新しい名前のパスを生成
                new_path = os.path.join(get_root_folder_path(),"savefiles",after_name)
                
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
            print(folderName)
            print(image)
            # ファイルを指定したフォルダに保存
            save_path = os.path.join(get_root_folder_path(),"savefiles",folderName, "thumbnail.png")
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            return {"message":"Thumbnails have been set up!!!!"}
        except Exception as e:
            return JSONResponse(content={"message": f"Error uploading file: {e}"}, status_code=500)