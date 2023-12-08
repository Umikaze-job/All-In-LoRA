from fastapi import Request, UploadFile, Form, File
from .folder_path import get_root_folder_path
from .file_control import get_setting_file_json,write_setting_file_json
import asyncio
import os

class Make_TextFile:
    async def Tagging(request:Request):
        data = await request.json()
        tagging_data = data.get('taggingData')
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)
        json_data["taggingData"] = {"base":[],"after":[]}

        # item--画像のurlパス ここでtaggingする
        for item in tagging_data['base']:
            # URLからファイル名を取得
            filename = os.path.basename(item)

            # 拡張子を抜いた部分を取得
            name_without_extension = os.path.splitext(filename)[0]
            json_data["taggingData"]["base"].append({"image_name":name_without_extension,"tag":"my tag"})

        for item in tagging_data['after']:
            # URLからファイル名を取得
            filename = os.path.basename(item)

            # 拡張子を抜いた部分を取得
            name_without_extension = os.path.splitext(filename)[0]
            json_data["taggingData"]["after"].append({"image_name":name_without_extension,"tag":"my tag"})

        write_setting_file_json(folder_name,json_data)

        return {"message":tagging_data,"folder_name":folder_name,"setting":get_setting_file_json(folder_name)}