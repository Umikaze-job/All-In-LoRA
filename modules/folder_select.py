from fastapi import FastAPI, Request
import asyncio
import os

from pydantic import BaseModel

def get_root_folder_path():
    # 現在のファイル（このスクリプト）のディレクトリを取得
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    # ルートフォルダのパスを取得
    root_folder_path = os.path.abspath(os.path.join(current_script_directory, ".."))

    return root_folder_path

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"フォルダ '{folder_path}' を作成しました。")
    except OSError as e:
        print(f"フォルダの作成中にエラーが発生しました: {e}")

class Folder_Select:
    async def Create(request:Request):
        data = await request.json()
        folder_name = data.get('name')
        create_folder(os.path.join(get_root_folder_path(),"savefiles",folder_name))
        return {"message": "OK"}
    
    async def Get_Folders(request:Request):
        dir_path = os.path.join(get_root_folder_path(),"savefiles")
        directories = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]

        # 更新日時でソート
        directories_sorted = sorted(directories, key=lambda f: os.path.getmtime(os.path.join(dir_path, f)), reverse=True)
        return directories_sorted