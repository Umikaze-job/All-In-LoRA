from fastapi import Request, UploadFile, Form, File
from .folder_path import get_root_folder_path
from .file_control import get_setting_file_json,write_setting_file_json,get_savefile_image_paths
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
                            data["tag"] = ["1girl","solo","new","tag"] #タグを指定
                else:
                    tag = ["1girl","solo","first","tag"] #タグを指定
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

            return {"tagdata":json_data["taggingData"]}
            pass
        except Exception as e:
            return {"error": "some error"}
        
    # Edit_Tag用のデータ
    async def EditTag_GetData(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        base_paths, after_paths = get_savefile_image_paths(folder_name)

        base = []
        after = []
        if len(json_data["taggingData"]["base"]) != 0:
            for path in base_paths:
                filename = os.path.basename(path)
                baselist = list(filter(lambda item: item.get("image_name") == filename, json_data["taggingData"]["base"]))

                if len(baselist) != 0:
                    base.append({"filename":filename,"tag":baselist[0]})

        if len(json_data["taggingData"]["after"]) != 0:
            for path in after_paths:
                filename = os.path.basename(path)
                afterlist = list(filter(lambda item: item.get("image_name") == filename, json_data["taggingData"]["after"]))

                if len(afterlist) != 0:
                    after.append({"filename":filename,"tag":afterlist[0]})

        return {"base":base,"after":after}