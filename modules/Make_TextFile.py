import traceback
from typing import Any
from fastapi import Request, UploadFile, Form, File
from .folder_path import get_root_folder_path,get_savefiles,get_localhost_name
from .file_control import get_savefile_image_paths, get_savefile_image_url_paths, get_setting_file_json,write_setting_file_json,make_random_tags
import asyncio
import os
from modules.gpu_modules.tagging import TaggingManager

from .class_definition.folder_manager import ImageFolderManager,CharacterTrimmingFolderManager,ThumbnailBaseFolderManager,ThumbnailAfterFolderManager
from .class_definition.json_manager import SettingLoraDataManager,SaveFilesSettingImageFolderManager,SaveFilesSettingTrimmingFolderManager

Tagging_Model:TaggingManager | None = None

class Make_TextFile:
    @staticmethod
    async def Tagging02(request:Request) -> dict[str, str]:
        try:
            data = await request.json()
            file_name:str = data.get('fileName')
            folder_name:str = data.get('folderName')
            type_name:str = data.get('type')
            loraData:dict[str,Any] = data.get('lotaData')

            global Tagging_Model
            if Tagging_Model == None:
                Tagging_Model = TaggingManager("wd-v1-4-vit-tagger-v2")

            if type_name == "base":
                manager = ImageFolderManager(folder_name=folder_name)
                await manager.tags_generate(file_name,Tagging_Model,lora_data=loraData)
            elif type_name == "after":
                ca_manager = CharacterTrimmingFolderManager(folder_name=folder_name)
                await ca_manager.tags_generate(file_name,Tagging_Model,lora_data=loraData)
            elif type_name == "deleteBase":
                manager = ImageFolderManager(folder_name=folder_name)
                manager.tags_delete(file_name)
            elif type_name == "deleteAfter":
                ca_manager = CharacterTrimmingFolderManager(folder_name=folder_name)
                ca_manager.tags_delete(file_name)

            return {"message":"OK!!!"}
        except Exception as e:
            return {"error": traceback.format_exc()}
        
    @staticmethod
    async def Clear_Tagging_Model(request:Request) -> dict[str, str]:
        global Tagging_Model
        Tagging_Model = None
        return {"message":"OK!!!"}
    
    # 使ってないかも
    @staticmethod
    async def Tagging_GetData(request:Request) -> dict:
        try:
            data = await request.json()
            folder_name = data.get('folderName')

            json_data = get_setting_file_json(folder_name)

            if "taggingData" not in json_data:
                json_data["taggingData"] = {"base":[],"after":[]}
                write_setting_file_json(folder_name,json_data)

            taggingData:dict = {"base":[],"after":[]}
            taggingData["base"] = [item for item in json_data["taggingData"]["base"] if item["tag"] != [""] and item["tag"] != None and item["tag"] != []]
            taggingData["after"] = [item for item in json_data["taggingData"]["after"] if item["tag"] != [""] and item["tag"] != None and item["tag"] != []]

            return {"tagdata":taggingData}
        except Exception as e:
            return {"error": traceback.format_exc()}
    
    # トリガーワードをデータに保存する
    @staticmethod
    async def Set_Trigger_Word(request:Request) -> None:
        data = await request.json()
        folder_name:str = data.get('folderName')
        trigger_word:str = data.get('triggerWord')

        manager = SettingLoraDataManager(folder_name=folder_name)

        manager.triggerWord = trigger_word
        
    @staticmethod
    async def Already_Tag(request:Request) -> dict[str,list[str]]:
        data = await request.json()
        folder_name:str = data.get('folderName')

        base_manager = ImageFolderManager(folder_name)
        after_manager = CharacterTrimmingFolderManager(folder_name)

        return {"base_images":base_manager.all_Images_has_tags(),"after_images":after_manager.all_Images_has_tags()}
    
    @staticmethod
    # タグ編集画面のデータ取得
    async def EditTag_GetData(request:Request) -> dict[str,Any]:
        data = await request.json()
        folder_name = data.get('folderName')

        base_manager = ImageFolderManager(folder_name)
        after_manager = CharacterTrimmingFolderManager(folder_name)
        base_thumbnail_manager = ThumbnailBaseFolderManager(folder_name)
        after_thumbnail_manager = ThumbnailAfterFolderManager(folder_name)

        base_url_data = base_manager.get_all_url_paths()
        after_url_data = after_manager.get_all_url_paths()

        base:list[dict[str,Any]] = []
        for url_data in base_url_data:
            file_name = os.path.basename(url_data)

            # サムネイルのURLを取得
            thumbnail_url_list = list(filter(lambda path:os.path.basename(path) == file_name,base_thumbnail_manager.get_all_url_paths()))
            if len(thumbnail_url_list) == 0:
                raise Exception("通常の画像とサムネイル画像のセットが欠けています")
            thumbnail_url = thumbnail_url_list[0]

            #表示名を取得する
            setting_image_data_manager = SaveFilesSettingImageFolderManager(folder_name)
            data_list = setting_image_data_manager.get_image_data
            data_list = list(filter(lambda data:data["file_name"] == file_name,data_list))
            if len(data_list) == 0:
                raise Exception("表示名が存在しません")

            base.append({"image_path":url_data,"thumbnail_path":thumbnail_url,"file_name":data_list[0]["displayed_name"],"tag":base_manager.get_Image_tags(file_name)})

        after:list[dict[str,Any]] = []
        for url_data in after_url_data:
            file_name = os.path.basename(url_data)

            # サムネイルのURLを取得
            thumbnail_url_list = list(filter(lambda path:os.path.basename(path) == file_name,after_thumbnail_manager.get_all_url_paths()))
            if len(thumbnail_url_list) == 0:
                raise Exception("通常の画像とサムネイル画像のセットが欠けています")
            thumbnail_url = thumbnail_url_list[0]

            #表示名を取得する
            setting_image_data_manager = SaveFilesSettingTrimmingFolderManager(folder_name)
            data_list = setting_image_data_manager.get_image_data
            data_list = list(filter(lambda data:data["file_name"] == file_name,data_list))
            if len(data_list) == 0:
                raise Exception("表示名が存在しません")

            after.append({"image_path":url_data,"thumbnail_path":thumbnail_url,"file_name":data_list[0]["displayed_name"],"tag":after_manager.get_Image_tags(file_name=file_name)})

        return {"base":base,"after":after}
    
    @staticmethod
    async def EditTag_Write(request:Request) -> dict[str,str]:
        data = await request.json()
        folder_name = data.get('folderName')
        base_data = data.get('base')
        after_data = data.get('after')

        base_manager = ImageFolderManager(folder_name)
        after_manager = CharacterTrimmingFolderManager(folder_name)

        base_manager.str_tags_write_to_json(base_data)
        after_manager.str_tags_write_to_json(after_data)

        return {"message":"OK!!!"}
    
    @staticmethod
    async def Captioning_Start(request:Request) -> dict[str,Any]:
        data = await request.json()
        folder_name:str = data.get('folderName')

        json_data = get_setting_file_json(folder_name)
        base_image_url, after_image_url = get_savefile_image_url_paths(folder_name)

        base_data = []
        after_data = []

        # baseデータ
        for image_url in base_image_url:
            file_name = os.path.basename(image_url)
            thumbnail_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","base",file_name)

            main_data = list(filter(lambda item:item.get("image_name") == file_name,json_data["taggingData"]["base"]))
            if len(main_data) != 0 and main_data[0].get("caption") != None:
                base_data.append({"path":image_url,"thumbnail_path":thumbnail_path,"caption":main_data[0]["caption"]})
            else:
                base_data.append({"path":image_url,"thumbnail_path":thumbnail_path,"caption":""})

        # afterデータ
        for image_url in after_image_url:
            file_name = os.path.basename(image_url)
            thumbnail_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","after",file_name)

            main_data = list(filter(lambda item:item.get("image_name") == file_name,json_data["taggingData"]["after"]))
            if len(main_data) != 0 and main_data[0].get("caption") != None:
                after_data.append({"path":image_url,"thumbnail_path":thumbnail_path,"caption":main_data[0]["caption"]})
            else:
                after_data.append({"path":image_url,"thumbnail_path":thumbnail_path,"caption":""})

        return {"base":base_data,"after":after_data}
    
    @staticmethod
    async def Captioning_Write(request:Request) -> dict[str,Any]:
        data = await request.json()
        folder_name:str = data.get('folderName')
        base_datas = data.get('baseImages')
        after_datas = data.get('afterImages')

        json_data = get_setting_file_json(folder_name)

        # json_data["taggingData"]["base"]の各連想配列のデータを更新する
        for data in base_datas:
            if data["caption"] != "":
                # json_data["taggingData"]["base"]のなかにimage_nameキーの値がdata["imageName"]である連想配列があるかどうか
                if any(d.get("image_name") == data["file_name"] for d in json_data["taggingData"]["base"]):
                    image_data:Any = next((item for item in json_data["taggingData"]["base"] if item["image_name"] == data["file_name"]), None)
                    image_data["caption"] = data["caption"]
                # なければ
                else:
                    json_data["taggingData"]["base"].append({"image_name":data["file_name"],"caption":data["caption"]})

        # json_data["taggingData"]["after"]の各連想配列のデータを更新する
        for data in after_datas:
            if data["caption"] != "":
                # json_data["taggingData"]["after"]のなかにimage_nameキーの値がdata["file_name"]である連想配列があるかどうか
                if any(d.get("image_name") == data["file_name"] for d in json_data["taggingData"]["after"]):
                    image_data = next((item for item in json_data["taggingData"]["after"] if item["image_name"] == data["file_name"]), None)
                    image_data["caption"] = data["caption"]
                # なければ
                else:
                    json_data["taggingData"]["after"].append({"image_name":data["file_name"],"caption":data["caption"]})

        write_setting_file_json(folder_name,json_data)

        return {"message":"OK!!!"}
    
    @staticmethod
    async def Caption_Tag(request:Request) -> dict[str,Any]:
        data = await request.json()
        folder_name:str = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        base_manager = ImageFolderManager(folder_name)
        after_manager = CharacterTrimmingFolderManager(folder_name)

        return {"base_images":base_manager.all_Images_has_caption(),"after_images":after_manager.all_Images_has_caption()}
    
    @staticmethod
    async def Start_Caption(request:Request) -> dict[str,str]:
        data = await request.json()
        folder_name:str = data.get('folderName')
        image_data = data.get('captionImage')

        return {"caption":"Made in Caption"}