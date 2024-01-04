import traceback
from fastapi import Request, UploadFile, Form, File
from .folder_path import get_root_folder_path,get_savefiles,get_localhost_name
from .file_control import get_savefile_image_paths, get_savefile_image_url_paths, get_setting_file_json,write_setting_file_json,make_random_tags
import asyncio
import os
from .gpu_modules.tagging import ready_model,do_tagging
from PIL import Image

from .class_definition.image_folder_manager import ImageFolderManager
from .class_definition.character_trimming_folder_manager import CharacterTrimmingFolderManager

Tagging_Model = None

class Make_TextFile:
    async def Tagging02(request:Request):
        try:
            data = await request.json()
            file_name = data.get('fileName')
            folder_name = data.get('folderName')
            type_name = data.get('type')

            global Tagging_Model
            if Tagging_Model == None:
                Tagging_Model = ready_model("wd-v1-4-vit-tagger-v2.onnx")

            if type_name == "base":
                manager = ImageFolderManager(folder_name)
                await manager.tags_generate(file_name,Tagging_Model)
            elif type_name == "after":
                manager = CharacterTrimmingFolderManager(folder_name)
                await manager.tags_generate(file_name,Tagging_Model)
            elif type_name == "deleteBase":
                manager = ImageFolderManager(folder_name)
                manager.tags_delete(file_name)
            elif type_name == "deleteAfter":
                manager = CharacterTrimmingFolderManager(folder_name)
                manager.tags_delete(file_name)

            return {"message":"OK!!!"}
        except Exception as e:
            return {"error": traceback.format_exc()}
    
    async def Clear_Tagging_Model(request:Request):
        global Tagging_Model
        Tagging_Model = None
        return {"message":"OK!!!"}

    async def Tagging_GetData(request:Request):
        try:
            data = await request.json()
            folder_name = data.get('folderName')

            json_data = get_setting_file_json(folder_name)

            if "taggingData" not in json_data:
                json_data["taggingData"] = {"base":[],"after":[]}
                write_setting_file_json(folder_name,json_data)

            taggingData = {"base":[],"after":[]}
            taggingData["base"] = [item for item in json_data["taggingData"]["base"] if item["tag"] != [""] and item["tag"] != None and item["tag"] != []]
            taggingData["after"] = [item for item in json_data["taggingData"]["after"] if item["tag"] != [""] and item["tag"] != None and item["tag"] != []]

            return {"tagdata":taggingData}
        except Exception as e:
            return {"error": traceback.format_exc()}
        
    async def Already_Tag(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        already_base = []
        for data in json_data["taggingData"]["base"]:
            if data.get("tag") != None and data["tag"] != [""]:
                already_base.append(data["image_name"])

        already_after = []
        for data in json_data["taggingData"]["after"]:
            if data.get("tag") != None and data["tag"] != [""]:
                already_after.append(data["image_name"])

        return {"base_images":already_base,"after_images":already_after}
    
    async def EditTag_GetData(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        base_url,after_url = get_savefile_image_url_paths(folder_name)

        base = []
        for url in base_url:
            file_name = os.path.basename(url)
            thunbnail_url = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","base",file_name)

            tag_data = []
            #配列内の連想配列の中にnameと同じ値の'image_name'が存在し、'tag'キーと値が存在するか
            main_data = list(filter(lambda data:data.get("image_name") == file_name,json_data["taggingData"]["base"]))
            if len(main_data) != 0 and main_data[0].get("tag") != None:
                tag_data = main_data[0].get("tag")

            base.append({"image_path":url,"thumbnail_path":thunbnail_url,"file_name":file_name,"tag":tag_data})

        after = []
        for url in after_url:
            file_name = os.path.basename(url)
            thunbnail_url = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","after",file_name)

            tag_data = []
            #配列内の連想配列の中にnameと同じ値の'image_name'が存在し、'tag'キーと値が存在するか
            main_data = list(filter(lambda data:data.get("image_name") == file_name,json_data["taggingData"]["after"]))
            if len(main_data) != 0 and main_data[0].get("tag") != None:
                tag_data = main_data[0].get("tag")

            after.append({"image_path":url,"thumbnail_path":thunbnail_url,"file_name":file_name,"tag":tag_data})

        return {"base":base,"after":after}
    
    async def EditTag_Write(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        base_data = data.get('base')
        after_data = data.get('after')

        json_data = get_setting_file_json(folder_name)

        # base_dataの処理
        for data in base_data:
            # json_data["taggingData"]["base"]にdataの"file_name"と同じ名前の"image_name"キーの値が存在するか
            base_data = list(filter(lambda item:item.get("image_name") == data["file_name"],json_data["taggingData"]["base"]))
            if len(base_data) != 0:
                base_data[0]["tag"] = data["imgtag"].split(",")
            else:
                json_data["taggingData"]["base"].append({'image_name':data["file_name"],"tag":data["imgtag"].split(",")})

        # after_dataの処理
        for data in after_data:
            # json_data["taggingData"]["after"]にdataの"file_name"と同じ名前の"image_name"キーの値が存在するか
            after_data = list(filter(lambda item:item.get("image_name") == data["file_name"],json_data["taggingData"]["after"]))
            if len(after_data) != 0:
                after_data[0]["tag"] = data["imgtag"].split(",")
            else:
                json_data["taggingData"]["after"].append({'image_name':data["file_name"],"tag":data["imgtag"].split(",")})

        write_setting_file_json(folder_name,json_data)

        return {"message":"OK!!!"}
    

    async def Captioning_Start(request:Request):
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
    
    async def Captioning_Write(request:Request):
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
                    image_data = next((item for item in json_data["taggingData"]["base"] if item["image_name"] == data["file_name"]), None)
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
    
    async def Caption_Tag(request:Request):
        data = await request.json()
        folder_name:str = data.get('folderName')

        json_data = get_setting_file_json(folder_name)
        
        base_paths, after_paths = get_savefile_image_paths(folder_name)

        base_paths = [d.split('\\')[-1] for d in base_paths]
        after_paths = [d.split('\\')[-1] for d in after_paths]

        base = []
        for data in json_data["taggingData"]["base"]:
            if data.get("image_name") != None and any(data.get("image_name") == name for name in base_paths):
                if data.get("caption","") != "":
                    base.append(data.get("image_name"))

        after = []
        for data in json_data["taggingData"]["after"]:
            if data.get("image_name") != None and any(data.get("image_name") == name for name in after_paths):
                if data.get("caption","") != "":
                    after.append(data.get("image_name"))

        return {"base_images":base,"after_images":after}
    
    async def Start_Caption(request:Request):
        data = await request.json()
        folder_name:str = data.get('folderName')
        image_data:{"folderId":int,"ImageName":str} = data.get('captionImage')

        return {"caption":"Made in Caption"}