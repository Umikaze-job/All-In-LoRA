from fastapi import Request, UploadFile, Form, File
from .folder_path import get_root_folder_path
from .file_control import get_savefile_image_paths, get_savefile_image_url_paths, get_setting_file_json,write_setting_file_json,make_random_tags
import asyncio
import os

class Make_TextFile:
    async def Tagging(request:Request):
        try:
            data = await request.json()
            tagging_data = data.get('taggingData')
            folder_name = data.get('folderName')

            json_data = get_setting_file_json(folder_name)
            if "taggingData" not in json_data:
                json_data["taggingData"] = {"base":[],"after":[]}
                write_setting_file_json(folder_name,json_data)

            # item--画像のurlパス ここでtaggingする
            for item in tagging_data['base']:
                # URLからファイル名を取得
                filename = os.path.basename(item)

                # 拡張子を抜いた部分を取得
                name_without_extension = os.path.splitext(filename)[0]
                # すでにjson_data["taggingData"]["base"]["image_name"]に同じファイル名が存在するとき
                if any(d.get("image_name") == filename for d in json_data["taggingData"]["base"]):
                    for data in json_data["taggingData"]["base"]:
                        if data["image_name"] == filename:
                            data["tag"] = make_random_tags(10) #タグを指定
                else:
                    tag = make_random_tags(10) #タグを指定

                    json_data["taggingData"]["base"].append({"image_name":filename,"tag":tag})

            for item in tagging_data['after']:
                # URLからファイル名を取得
                filename = os.path.basename(item)

                # すでにjson_data["taggingData"]["after"]["image_name"]に同じファイル名が存在するとき
                if any(d.get("image_name") == filename for d in json_data["taggingData"]["after"]):
                    for data in json_data["taggingData"]["after"]:
                        if data["image_name"] == filename:
                            data["tag"] = make_random_tags(10) #タグを指定
                else:
                    tag = make_random_tags(10) #タグを指定

                    json_data["taggingData"]["after"].append({"image_name":filename,"tag":tag})

            for item in tagging_data['deleteBase']:
                # URLからファイル名を取得
                filename = os.path.basename(item)
                
                json_data["taggingData"]["base"] = list(filter(lambda item: item.get("image_name") != filename, json_data["taggingData"]["base"]))

            for item in tagging_data['deleteAfter']:
                # URLからファイル名を取得
                filename = os.path.basename(item)
                
                json_data["taggingData"]["after"] = list(filter(lambda item: item.get("image_name") != filename, json_data["taggingData"]["after"]))


            write_setting_file_json(folder_name,json_data)

            return {"message":"File Tagged!!"}
        
        except Exception as e:
            return {"error": "some error"}
        
    async def Tagging_GetData(request:Request):
        try:
            data = await request.json()
            folder_name = data.get('folderName')

            json_data = get_setting_file_json(folder_name)

            if "taggingData" not in json_data:
                json_data["taggingData"] = {"base":[],"after":[]}
                write_setting_file_json(folder_name,json_data)

            return {"tagdata":json_data["taggingData"]}
        except Exception as e:
            return {"error": "some error"}
        
    async def Already_Tag(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        already_base = []
        for data in json_data["taggingData"]["base"]:
            if data.get("tag") != None and data["tag"] != "":
                already_base.append(data["image_name"])

        already_after = []
        for data in json_data["taggingData"]["after"]:
            if data.get("tag") != None and data["tag"] != "":
                already_after.append(data["image_name"])

        return {"base_images":already_base,"after_images":already_after}
        
    # Edit_Tag用のデータ
    async def EditTag_GetData(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        baseurl, afterurl = get_savefile_image_url_paths(folder_name)

        return {"base":json_data["taggingData"]["base"],"after":json_data["taggingData"]["after"],"beforeurl":baseurl,"afterurl":afterurl}
    
    async def EditTag_Write(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        base_data = data.get('base')
        after_data = data.get('after')

        json_data = get_setting_file_json(folder_name)

        print(f"folder_name:{folder_name}")
        print(f"base_data:{base_data}")
        # base_dataの処理
        for data in base_data:
            print(f"data:{data}")
            for base_data_item in json_data["taggingData"]["base"]:
                if base_data_item.get("image_name") == data["file_name"]:
                    base_data_item["tag"] = data["tag"].split(",")

        # # after_dataの処理
        for data in after_data:
            for after_data_item in json_data["taggingData"]["after"]:
                if after_data_item.get("image_name") == data["file_name"]:
                    after_data_item["tag"] = data["tag"].split(",")

        write_setting_file_json(folder_name,json_data)

        return {"message":"OK!!!"}
    

    async def Captioning_Start(request:Request):
        data = await request.json()
        folder_name:str = data.get('folderName')

        json_data = get_setting_file_json(folder_name)
        base, after = get_savefile_image_url_paths(folder_name)

        base_data = []
        # baseデータ
        for data in base:
            file_name = data.split('\\')[-1]
            # json_data["taggingData"]["base"]の中にimage_nameキーが存在し、captionキーと値が存在する場合
            if any(d.get("image_name") == file_name and d.get("caption",None) != None for d in json_data["taggingData"]["base"]):
                # json_data["taggingData"]["base"]からimage_nameキーの値がfile_nameである連想配列を取得する
                image_data = next((item for item in json_data["taggingData"]["base"] if item["image_name"] == file_name), None)
                base_data.append({"path":data,"caption":image_data["caption"]})
            else:
                base_data.append({"path":data,"caption":""})

        after_data = []
        # afterデータ
        for data in after:
            file_name = data.split('\\')[-1]
            # json_data["taggingData"]["after"]の中にimage_nameキーが存在し、captionキーと値が存在する場合
            if any(d.get("image_name") == file_name and d.get("caption",None) != None for d in json_data["taggingData"]["after"]):
                # json_data["taggingData"]["after"]からimage_nameキーの値がfile_nameである連想配列を取得する
                image_data = next((item for item in json_data["taggingData"]["after"] if item["image_name"] == file_name), None)
                after_data.append({"path":data,"caption":image_data["caption"]})
            else:
                after_data.append({"path":data,"caption":""})

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
                if any(d.get("image_name") == data["imageName"] for d in json_data["taggingData"]["base"]):
                    image_data = next((item for item in json_data["taggingData"]["base"] if item["image_name"] == data["imageName"]), None)
                    image_data["caption"] = data["caption"]
                # なければ
                else:
                    json_data["taggingData"]["base"].append({"image_name":data["imageName"],"caption":data["caption"]})

        # json_data["taggingData"]["after"]の各連想配列のデータを更新する
        for data in after_datas:
            if data["caption"] != "":
                # json_data["taggingData"]["after"]のなかにimage_nameキーの値がdata["imageName"]である連想配列があるかどうか
                if any(d.get("image_name") == data["imageName"] for d in json_data["taggingData"]["after"]):
                    image_data = next((item for item in json_data["taggingData"]["after"] if item["image_name"] == data["imageName"]), None)
                    image_data["caption"] = data["caption"]
                # なければ
                else:
                    json_data["taggingData"]["after"].append({"image_name":data["imageName"],"caption":data["caption"]})

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