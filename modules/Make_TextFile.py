import traceback
from fastapi import Request, UploadFile, Form, File
from .folder_path import get_root_folder_path,get_savefiles,get_localhost_name
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
            return {"error": traceback.format_exc()}
        
    async def Tagging02(request:Request):
        data = await request.json()
        file_name = data.get('fileName')
        folder_name = data.get('folderName')
        type_name = data.get('type')

        json_data = get_setting_file_json(folder_name)

        if type_name == "base":
            file_path = os.path.join(get_savefiles(),folder_name,"images_folder",file_name)
            # json_data["taggingData"]["base"]["image_name"]の値がfile_nameと同じ名前の連想配列があるとき
            if any(file_name == item.get('image_name') for item in json_data["taggingData"]["base"]):
                rensou = [item for item in json_data["taggingData"]["base"] if item.get('image_name') == file_name]
                rensou[0]["tag"] = make_random_tags(10) #タグを指定
            else:
                tag = make_random_tags(10) #タグを指定
                json_data["taggingData"]["base"].append({"image_name":file_name,"tag":tag})
        elif type_name == "after":
            file_path = os.path.join(get_savefiles(),folder_name,"images_folder",file_name)
            # json_data["taggingData"]["after"]["image_name"]の値がfile_nameと同じ名前の連想配列があるとき
            if any(file_name == item.get('image_name') for item in json_data["taggingData"]["after"]):
                rensou = [item for item in json_data["taggingData"]["after"] if item.get('image_name') == file_name]
                rensou[0]["tag"] = make_random_tags(10) #タグを指定
            else:
                tag = make_random_tags(10) #タグを指定
                json_data["taggingData"]["after"].append({"image_name":file_name,"tag":tag})
        elif type_name == "deleteBase":
            # json_data["taggingData"]["base"]["image_name"]の値がfile_nameと同じ名前の連想配列があるとき
            if any(file_name == item.get('image_name') for item in json_data["taggingData"]["base"]):
                rensou = [item for item in json_data["taggingData"]["base"] if item.get('image_name') == file_name]
                if rensou[0].get("tag") != None:
                    rensou[0]["tag"] = [""]
            pass
        elif type_name == "deleteAfter":
            # json_data["taggingData"]["after"]["image_name"]の値がfile_nameと同じ名前の連想配列があるとき
            if any(file_name == item.get('image_name') for item in json_data["taggingData"]["after"]):
                rensou = [item for item in json_data["taggingData"]["after"] if item.get('image_name') == file_name]
                if rensou[0].get("tag") != None:
                    rensou[0]["tag"] = [""]

        write_setting_file_json(folder_name,json_data)

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
        
    # Edit_Tag用のデータ
    async def EditTag_GetData(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        base_image_dir = os.path.join(get_savefiles(),folder_name,"images_folder")
        after_image_dir = os.path.join(get_savefiles(),folder_name,"character_trimming_folder")
        #base

        #images_folderフォルダの中にある画像の名前
        base_image_names = list(filter(lambda file:os.path.isfile(os.path.join(base_image_dir, file)),os.listdir(base_image_dir)))
        base_data = []
        for name in base_image_names:
            image_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"images_folder",name)
            thumbnali_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","base",name)
            
            tag_data = []
            #配列内の連想配列の中にnameと同じ値の'image_name'が存在し、'tag'キーと値が存在するか
            main_data = list(filter(lambda data:data.get("image_name") == name,json_data["taggingData"]["base"]))
            if len(main_data) != 0 and main_data[0].get("tag") != None:
                tag_data = main_data[0].get("tag")

            base_data.append({"image_path":image_path,"thumbnail_path":thumbnali_path,"file_name":name,"tag":tag_data})

        #after
        
        #images_folderフォルダの中にある画像の名前
        after_image_names = list(filter(lambda file:os.path.isfile(os.path.join(after_image_dir, file)),os.listdir(after_image_dir)))
        after_data = []
        for name in after_image_names:
            image_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"character_trimming_folder",name)
            thumbnali_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","after",name)
            
            tag_data = []
            #配列内の連想配列の中にnameと同じ値の'image_name'が存在し、'tag'キーと値が存在するか
            main_data = list(filter(lambda data:data.get("image_name") == name,json_data["taggingData"]["after"]))
            if len(main_data) != 0 and main_data[0].get("tag") != None:
                tag_data = main_data[0].get("tag")

            after_data.append({"image_path":image_path,"thumbnail_path":thumbnali_path,"file_name":name,"tag":tag_data})


        return {"base":base_data,"after":after_data}
    
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
                base_data[0]["tag"] = data["tag"].split(",")
            else:
                json_data["taggingData"]["base"].append({'image_name':data["file_name"],"tag":data["tag"].split(",")})

        # after_dataの処理
        for data in after_data:
            # json_data["taggingData"]["after"]にdataの"file_name"と同じ名前の"image_name"キーの値が存在するか
            after_data = list(filter(lambda item:item.get("image_name") == data["file_name"],json_data["taggingData"]["after"]))
            if len(after_data) != 0:
                after_data[0]["tag"] = data["tag"].split(",")
            else:
                json_data["taggingData"]["after"].append({'image_name':data["file_name"],"tag":data["tag"].split(",")})

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
                base_data.append({"path":image_url,"thumbnail_path":thumbnail_path,"caption":main_data[0]["caption"]})
            else:
                base_data.append({"path":image_url,"thumbnail_path":thumbnail_path,"caption":""})

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