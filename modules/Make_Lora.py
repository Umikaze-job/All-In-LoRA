import asyncio
import math
import time
import traceback
from typing import Any
from fastapi import Request
import os

import toml
from .folder_path import get_fine_tuning_folder,get_root_folder_path
from .file_control import get_savefile_image_paths, write_setting_file_json,get_savefile_image_url_paths,get_setting_file_json,get_user_setting_json,get_thumbnail_url_paths,get_user_setting_json
from .folder_path import get_savefiles
import subprocess
import shutil
from pathlib import Path
import json
from modules.class_definition.folder_manager import ImageFolderManager,CharacterTrimmingFolderManager,ThumbnailBaseFolderManager,ThumbnailAfterFolderManager,FineTuningFolderManager
from modules.class_definition.json_manager import SettingLearningMethodsManager,SettingLoraDataManager,SaveFilesSettingImageFolderManager,SaveFilesSettingTrimmingFolderManager
from fastapi.responses import StreamingResponse

class Make_Lora:
    @staticmethod
    async def Image_Items(request:Request) -> dict[str,Any]:
        data = await request.json()
        folder_name = data.get('folderName')

        base = ImageFolderManager(folder_name=folder_name).get_all_url_paths()
        after = CharacterTrimmingFolderManager(folder_name=folder_name).get_all_url_paths()
        base_thumbnail = ThumbnailBaseFolderManager(folder_name=folder_name).get_all_url_paths()
        after_thumbnail = ThumbnailAfterFolderManager(folder_name=folder_name).get_all_url_paths()

        image_items:dict[str,list[Any]] = {"base":[],"after":[]}

        image_items["base"] = SaveFilesSettingImageFolderManager(folder_name=folder_name).get_image_path_and_learning_data(base)
        image_items["after"] = SaveFilesSettingTrimmingFolderManager(folder_name=folder_name).get_image_path_and_learning_data(after)

        methods = SettingLearningMethodsManager(folder_name=folder_name).get_learning_methods_data()
        loraData = SettingLoraDataManager(folder_name=folder_name).get_lora_data()

        return {"base":base,"after":after,"base_thumbnail":base_thumbnail,
                "after_thumbnail":after_thumbnail,"image_items":image_items,
                "methods":methods,"loraData":loraData}
    
    @staticmethod
    async def Save_Data(request:Request) -> dict[str,str]:
        data = await request.json()
        folder_name = data.get('folderName')
        image_items = data.get('ImageItems')
        methods = data.get('methods')
        loraData = data.get('loraData')

        # 画像に与えられた学習方法をデータにして保存する
        base_manager = SaveFilesSettingImageFolderManager(folder_name=folder_name)
        after_manager = SaveFilesSettingTrimmingFolderManager(folder_name=folder_name)

        for data in image_items["base"]:
            base_manager.set_learning_method_to_data(file_name=data["image_name"],method_name=data["method_name"])

        for data in image_items["after"]:
            after_manager.set_learning_method_to_data(file_name=data["image_name"],method_name=data["method_name"])

        # 学習方法を保存する
        LM_manager = SettingLearningMethodsManager(folder_name=folder_name)
        LM_manager.set_learning_methods_data(data=methods)
        # Lora情報を保存する
        Lora_manager = SettingLoraDataManager(folder_name=folder_name)
        Lora_manager.set_lora_data(loraData)

        return {"message":"OK!!!"}
    
    @staticmethod
    async def Sd_Model(request:Request) -> list[dict[str,Any]]:
        json_data = get_user_setting_json()
        folder_path = json_data["sd-model-folder"]

        result = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                result.append({"name":file,"path":relative_path})

        return result
    
    @staticmethod
    async def Press_Make_Command(request:Request) -> dict[str,str]:
        try:
            data = await request.json()
            folder_name = data.get('folderName')

            fine_tuning_manager = FineTuningFolderManager(folder_name=folder_name)

            base_image_manager = ImageFolderManager(folder_name=folder_name)
            after_image_manager = CharacterTrimmingFolderManager(folder_name=folder_name)

            base_setting_manager = SaveFilesSettingImageFolderManager(folder_name=folder_name)
            after_setting_manager = SaveFilesSettingTrimmingFolderManager(folder_name=folder_name)

            learning_method_set = SettingLearningMethodsManager(folder_name=folder_name).get_learning_methods_data()
            lora_data_set = SettingLoraDataManager(folder_name=folder_name).get_lora_data()

            fine_tuning_manager.output_files_to_lora_folder(lora_data=lora_data_set)

            #? 一旦、fine_tuning_folderの中身をすべて削除する。
            fine_tuning_manager.folder_init()
            #? フォルダとファイルを作成する
            fine_tuning_manager.make_all_folders(img_folder_count=len(learning_method_set))

            #? 画像フォルダを移動させる
            for index,LM in enumerate(learning_method_set):
                # base
                # 学習方法が指定されている画像のパスのリストを取得
                base_images = base_setting_manager.get_image_data_with_learning_method(method=LM["name"])
                base_images_name = list(map(lambda data:data["file_name"],base_images))
                base_images_path = list(filter(lambda path:os.path.basename(path) in base_images_name,base_image_manager.get_all_image_paths()))

                # after
                after_images = after_setting_manager.get_image_data_with_learning_method(method=LM["name"])
                after_images_name = list(map(lambda data:data["file_name"],after_images))
                after_images_path = list(filter(lambda path:os.path.basename(path) in after_images_name,after_image_manager.get_all_image_paths()))

                #移動する
                fine_tuning_manager.move_images_to_folder(folder_index=index,image_paths=base_images_path + after_images_path)

                #meta_data.jsonを作る
                for data in base_images:
                    data["file_path"] = base_image_manager.get_selected_image_path(data["file_name"])

                for data in after_images:
                    data["file_path"] = after_image_manager.get_selected_image_path(data["file_name"])

                fine_tuning_manager.make_meta_data(folder_index=index,images_data=base_images + after_images)

            # tomlファイルを作成する
            fine_tuning_manager.make_toml_file(method_data=learning_method_set)

            # sample_prompt.txtを作成する
            fine_tuning_manager.make_sample_prompt_file(sample=lora_data_set["sampleImage"])

            # batファイルを作成する
            fine_tuning_manager.make_bat_file(lora_data=lora_data_set)
        
            # batファイルの実行
            await fine_tuning_manager.execute_bat_file()

            fine_tuning_manager.output_files_to_lora_folder(lora_data=lora_data_set)

            return {"message":"OK!!!"}
        except Exception as e:
            return {"error":traceback.format_exc()}
    
    @staticmethod
    async def test_moveLoRa(request:Request) -> dict[str,str]:
        data = await request.json()
        folder_name = data.get('folderName')
        lora_name = data.get('loraName')

        main_folder = get_fine_tuning_folder(folder_name)

        for curDir,dir,files in os.walk(os.path.join(main_folder,"output")):
            safetensor = list(filter(lambda file:file.endswith(".safetensors"),files))

            print(safetensor)
            if len(safetensor) != 0:
                print(curDir)
                break

        return {"message":"OK!!!"}

