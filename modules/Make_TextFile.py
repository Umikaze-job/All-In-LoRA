from fastapi import Request, UploadFile, Form, File
from .folder_path import get_root_folder_path
from .file_control import get_savefile_image_url_paths, get_setting_file_json,write_setting_file_json,make_random_tags
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

                # 拡張子を抜いた部分を取得
                name_without_extension = os.path.splitext(filename)[0]
                # すでにjson_data["taggingData"]["after"]["image_name"]に同じファイル名が存在するとき
                if any(d.get("image_name") == filename for d in json_data["taggingData"]["after"]):
                    for data in json_data["taggingData"]["after"]:
                        if data["image_name"] == filename:
                            data["tag"] = ["1girl","solo","new","tag"] #タグを指定
                else:
                    tag = ["1girl","solo","first","tag"] #タグを指定
                    json_data["taggingData"]["after"].append({"image_name":filename,"tag":tag})

            for item in tagging_data['deleteBase']:
                # URLからファイル名を取得
                filename = os.path.basename(item)
                # 拡張子を抜いた部分を取得
                name_without_extension = os.path.splitext(filename)[0]
                
                json_data["taggingData"]["base"] = list(filter(lambda item: item.get("image_name") != filename, json_data["taggingData"]["base"]))

            for item in tagging_data['deleteAfter']:
                # URLからファイル名を取得
                filename = os.path.basename(item)
                # 拡張子を抜いた部分を取得
                name_without_extension = os.path.splitext(filename)[0]
                
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
        
    # Edit_Tag用のデータ
    async def EditTag_GetData(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        print(json_data["taggingData"]["base"])

        baseurl, afterurl = get_savefile_image_url_paths(folder_name)

        return {"base":json_data["taggingData"]["base"],"after":json_data["taggingData"]["after"],"beforeurl":baseurl,"afterurl":afterurl}