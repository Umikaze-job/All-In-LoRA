import os
import traceback
from typing import Any
from fastapi import Request
from modules.class_definition.user_setting_manager import UserSettingManager
from modules.class_definition.folder_manager import SaveFileManager
from modules.class_definition.folder_manager import ShellCommandManager
import torch
from torch.backends import cudnn

class Welcome_Page:

    @staticmethod
    async def Sd_Models_Folder(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_path = data.get("folder_path")
            manager = UserSettingManager()
            # 初期化処理でない場合floder_pathを入力する
            if folder_path != "":
                manager.Sd_Model_Folder = folder_path
            result = os.path.isdir(manager.Sd_Model_Folder)

            model_count = 0
            for curDir, dirs, files in os.walk(manager.Sd_Model_Folder):
                model_count += len(list(filter(lambda file:file.endswith(".safetensors"),files)))

            return {"isfolder":result,"modelCount":model_count}
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    @staticmethod
    async def Kohyass_Folder(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_path = data.get("folder_path")
            manager = UserSettingManager()
            # 初期化処理でない場合floder_pathを入力する
            if folder_path != "":
                manager.Kohyass_Folder = folder_path
            # フォルダが存在するか判定する
            isfolder = os.path.isdir(manager.Kohyass_Folder)
            # フォルダが存在しないとき
            if isfolder == False:
                return {"isfolder":False}
            # train_network.pyがないとき
            if os.path.isfile(os.path.join(manager.Kohyass_Folder,"train_network.py")) == False:
                return {"notrain":False}
            # sdxl_train_network.pyがないとき
            if os.path.isfile(os.path.join(manager.Kohyass_Folder,"sdxl_train_network.py")) == False:
                return {"nosdxl":False}
            return {"isfolder":True}
        except Exception as e:
            return {"error":traceback.format_exc()}

    
    @staticmethod
    async def Lora_Folder(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            folder_path = data.get("folder_path")
            manager = UserSettingManager()
            if folder_path != "":
                manager.Lora_Folder = folder_path
            result = os.path.isdir(manager.Lora_Folder)
            return {"isfolder":result}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    @staticmethod
    async def RealESRGAN_Install(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            isInit = data.get("isInit")
            # 初期化処理の場合
            if isInit:
                # フォルダが存在しない時
                if os.path.isdir(ShellCommandManager.get_real_esrgan_folder()) == False:
                    return {"result":"no"}
            else:
                await ShellCommandManager.RealESRGAN_Install()
            return {"result":"ok"}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    @staticmethod
    async def Setting_Mixed_Precision(request:Request) -> dict[str,Any]:
        try:
            data = await request.json()
            isInit = data.get("isInit")
            value = data.get("value")
            manager = UserSettingManager()
            print(f"value:{value}")
            # 初期化処理の場合
            if isInit:
                # データが存在しない場合
                if manager.Init_LoraData["MainSetting"]["mixed_precision"] == "":
                    return {"result":"no"}
            else:
                data = manager.Init_LoraData
                data["MainSetting"]["mixed_precision"] = value
                manager.Init_LoraData = data
                # データが存在しない場合
                if manager.Init_LoraData["MainSetting"]["mixed_precision"] == "":
                    return {"result":"no"}
            return {"result":"ok"}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    @staticmethod
    async def Check_Cuda_Cudnn() -> dict[str,Any]:
        try:
            # CUDAが利用可能かどうかを確認
            cuda_available = torch.cuda.is_available()
            # cuDNNが利用可能かどうかを確認
            cudnn_available = cudnn.is_available()
            if cuda_available == False:
                return {"result":"nocuda"}
            elif cudnn_available == None:
                return {"result":"nocudnn"}
            return {"result":"ok"}
        except Exception as e:
            return {"error":traceback.format_exc()}
        
    # 初期化設定
    @staticmethod
    async def Init_Setting() -> dict[str,Any]:
        try:
            # フォルダパスの確認
            manager = UserSettingManager()
            manager.setting_file_refresh()
            path_set = [
                manager.Sd_Model_Folder,
                manager.Kohyass_Folder,
                manager.Lora_Folder
            ]
            isfolder = all(list(map(lambda path:os.path.isdir(path),path_set)))

            # 選択しているフォルダ名の取得
            folderName = manager.Select_Folder_Name
            if (SaveFileManager.any_savefiles(folder_name=folderName) == False):
                folderName = ""

            # 言語の取得
            language = manager.User_Language

            # usersetting.jsonの訂正
            lora_data = manager.Init_LoraData
            # lora_data["performance"]["cupThread"]をlora_data["performance"]["cpuThreads"]に修正
            if lora_data["performance"].get("cupThread") != None:
                lora_data["performance"]["cpuThreads"] = lora_data["performance"]["cupThread"]

            manager.Init_LoraData = lora_data

            # フォルダ名の取得
            return {"isfolder":isfolder,"folderName":manager.Select_Folder_Name["name"],"folderId":manager.Select_Folder_Name["id"],"language":language}
        except Exception as e:
            return {"error":traceback.format_exc()}