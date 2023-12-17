import os

def get_root_folder_path():
    # 現在のファイル（このスクリプト）のディレクトリを取得
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    # ルートフォルダのパスを取得
    root_folder_path = os.path.abspath(os.path.join(current_script_directory, ".."))

    return root_folder_path

def get_savefiles():
    return os.path.join(get_root_folder_path(),"savefiles")

def get_fine_tuning_folder(folder_name:str):
    return os.path.join(get_root_folder_path(),"savefiles",folder_name,"fine_tuning_folder")

def get_localhost_name():
    return f"http://localhost:8000"
