from fastapi import Request
import os
from .folder_path import get_fine_tuning_folder,get_root_folder_path
from .file_control import get_savefile_image_paths, write_setting_file_json,get_savefile_image_url_paths,get_setting_file_json,get_user_setting_json
import subprocess
import shutil
from pathlib import Path
import json

def make_toml(json_data,dataset_folder):
    methods:[] = json_data["imageLearningSetting"]["methods"]
    toml = ""
    for index, met in enumerate(methods):
        folder = os.path.join(dataset_folder,"image" + str(index).rjust(3, '0'))
        meta_file = os.path.join(folder,"meta_data.json").replace("\\", "\\\\")
        folder = folder.replace("\\", "\\\\")
        toml += f"""
[[datasets]]
batch_size = 1
bucket_no_upscale = true
bucket_reso_steps = 64
enable_bucket = true
max_bucket_reso = 1024
min_bucket_reso = 128
resolution = 256
color_aug = false
flip_aug = true
keep_tokens = 2
num_repeats = 10
random_crop = false
shuffle_caption = true
[[dataset.subsets]]
image_dir = "{folder}"
metadata_file = "{meta_file}"
"""
    return toml

class Make_Lora:
    async def Image_Items(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        base,after = get_savefile_image_url_paths(folder_name)

        json_data = get_setting_file_json(folder_name)

        return {"base":base,"after":after,"image_items":json_data["imageLearningSetting"]["image_items"],"methods":json_data["imageLearningSetting"]["methods"],"loraData":json_data["loraData"]}
    
    async def Save_Data(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')
        image_items = data.get('ImageItems')
        methods = data.get('methods')
        loraData = data.get('loraData')

        json_data = get_setting_file_json(folder_name)

        json_data["imageLearningSetting"] = {"image_items":image_items,"methods":methods}
        json_data["loraData"] = loraData

        write_setting_file_json(folder_name,json_data)

        return {"message":"OK!!!"}
    
    async def Sd_Model(request:Request):
        json_data = get_user_setting_json()
        folder_path = json_data["sd-model-folder"]

        result = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                result.append({"name":file,"path":relative_path})

        return result
    
    async def Press_Start_Lora(request:Request):
        data = await request.json()
        folder_name = data.get('folderName')

        json_data = get_setting_file_json(folder_name)

        #? 一旦、fine_tuning_folderの中身をすべて削除する。
        main_folder = get_fine_tuning_folder(folder_name)
        shutil.rmtree(main_folder)
        #? フォルダとファイルを作成する

        #? データセットの画像の名前、メソッド名、パスが入った連想配列を作成する。
        base_images = []
        after_images = []
        base_images = json_data["imageLearningSetting"]["image_items"]["base"] #?{"image_name": str, "method_name": str}
        after_images = json_data["imageLearningSetting"]["image_items"]["after"]

        for data in base_images:
            data["path"] = os.path.join(get_root_folder_path(),"savefiles",folder_name,"images_folder",data["image_name"])
            taggingData = [tagdata for tagdata in json_data["taggingData"]["base"] if tagdata.get("image_name") == data["image_name"]]
            if len(taggingData) != 0:
                if taggingData[0].get("caption") != None and taggingData[0].get("caption") != "":
                    data["caption"] = taggingData[0].get("caption")
                if taggingData[0].get("tag") != None and len(taggingData[0].get("tag")) != 0:
                    data["tag"] = taggingData[0].get("tag")

        for data in after_images:
            data["path"] = os.path.join(get_root_folder_path(),"savefiles",folder_name,"character_trimming_folder",data["image_name"])
            taggingData = [tagdata for tagdata in json_data["taggingData"]["after"] if tagdata.get("image_name") == data["image_name"]]
            if len(taggingData) != 0:
                if taggingData[0].get("caption") != None and taggingData[0].get("caption") != "":
                    data["caption"] = taggingData[0].get("caption")
                if taggingData[0].get("tag") != None and len(taggingData[0].get("tag")) != 0:
                    data["tag"] = taggingData[0].get("tag")
        
        #? datasetフォルダを作成
        dataset_folder = os.path.join(main_folder,"dataset")
        Path(dataset_folder).mkdir(parents=True, exist_ok=True)
        #? methodsの数だけ中身のフォルダを増やす
        sub_dataset_folders = []
        for index,item in enumerate(json_data["imageLearningSetting"]["methods"]):
            folder = os.path.join(dataset_folder,"image" + str(index).rjust(3, '0'))
            Path(folder).mkdir(parents=True, exist_ok=True)
            sub_dataset_folders.append(folder)
            #? フォルダに画像をコピーしていれる
            name = item["name"] #メソッド名
            #? base_images,after_imagesの中にある連想配列からmethod_nameキーにさっきのメソッド名が含まれてるもののみを残した配列を作る
            base = [image for image in base_images if image.get("method_name") == name]
            after = [image for image in after_images if image.get("method_name") == name]

            json_write = {}

            for img in base + after:
                shutil.copy(img["path"],folder)
                data = {}
                if img.get("caption") != None:
                    data["caption"] = img.get("caption")
                if img.get("tag") != None:
                    data["tag"] = ', '.join(img.get("tag"))

                if data != {}:
                    json_write[img["path"]] = data

            #? メタデータに書き込む
            with open(os.path.join(folder,"meta_data.json"),"w") as f:
                f.write(json.dumps(json_write))
                

        log_folder = os.path.join(main_folder,"log")
        Path(log_folder).mkdir(parents=True, exist_ok=True)

        output_folder = os.path.join(main_folder,"output")
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        # setting.toml ファイルを作成
        setting_file_path = os.path.join(main_folder, 'setting.toml')
        with open(setting_file_path, 'w') as setting_file:
            # ここに setting.toml の内容を書き込む処理を追加
            setting_file.write(make_toml(json_data,dataset_folder))

        # sample_prompt.txt ファイルを作成
        sample_prompt_file_path = os.path.join(main_folder, 'sample_prompt.txt')
        with open(sample_prompt_file_path, 'w') as sample_prompt_file:
            sample = json_data["loraData"]["sampleImage"]
            # ここに sample_prompt.txt の内容を書き込む処理を追加
            sample_prompt_file.write(f"{sample['positivePrompt']} --n {sample['negativePrompt']} --w {sample['width']} --h {sample['height']} --d 1 --l 7.5 --s {sample['steps']}")
