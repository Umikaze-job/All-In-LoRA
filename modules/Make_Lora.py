import asyncio
import math
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
from modules.class_definition.folder_manager import ImageFolderManager

def make_toml(json_data:dict[str,Any],dataset_folder:str) -> str:
    methods = json_data["imageLearningSetting"]["methods"]
    toml = ""
    for index, met in enumerate(methods):
        folder = os.path.join(dataset_folder,"image" + str(index).rjust(3, '0'))
        meta_file = os.path.join(folder,"meta_data.json").replace("\\", "\\\\")
        folder = folder.replace("\\", "\\\\")
        toml += f"""
[[datasets]]
batch_size = {met["setting"]["batchSize"]}
bucket_no_upscale = {str(met["setting"]["bucketNoUpscale"]).lower()}
bucket_reso_steps = {met["setting"]["bucketResoSteps"]}
enable_bucket = {str(met["setting"]["enableBucket"]).lower()}
max_bucket_reso = {met["setting"]["maxBucketReso"]}
min_bucket_reso = {met["setting"]["minBucketReso"]}
resolution = {met["setting"]["resolution"]}
color_aug = {str(met["setting"]["colorAug"]).lower()}
flip_aug = {str(met["setting"]["flipAug"]).lower()}
keep_tokens = {met["setting"]["keepTokens"]}
num_repeats = {met["setting"]["numRepeats"]}
shuffle_caption = {str(met["setting"]["shuffleCaption"]).lower()}
[[datasets.subsets]]
image_dir = "{folder}"
metadata_file = "{meta_file}"
"""
    return toml

def find_file(file_name:str, search_path:str) -> str | None:
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def use_optimizer_command(optimizer_type:str) -> str:
    if optimizer_type in ["Lion"]:
        return "--use_lion_optimizer"
    elif optimizer_type == "AdamW8bit":
        return "--use_8bit_adam"
    else:
        return f"--optimizer_type={optimizer_type}"

# net_argsの取得
def get_net_args(lora_type:str, conv_dim:float, conv_alpha:float, dropout:float, block_size:int=16) -> str:
    if (lora_type == "dylora"):
        return f'"algo=dylora" "conv_dim={conv_dim}" "conv_alpha={conv_alpha}" "dropout={dropout}" "block_size={block_size}"'
    elif (lora_type == "lokr"):
        return f'"algo=lokr" "conv_dim={conv_dim}" "conv_alpha={conv_alpha}" "dropout={dropout}"'
    elif (lora_type == "locon"):
        return f'"algo=locon" "conv_dim={conv_dim}" "conv_alpha={conv_alpha}" "dropout={dropout}"'
    elif (lora_type == "loha"):
        return f'"algo=loha" "conv_dim={conv_dim}" "conv_alpha={conv_alpha}"'
    else:
        return ''
    
# ネットワークモジュールの取得
def get_network_module(lora_type:str) -> str:
    if (lora_type in ["lokr","locon","loha"]):
        return "lycoris.kohya"
    elif (lora_type == "dylora"):
        return "networks.dylora"
    elif (lora_type == "LoRA-FA"):
        return "networks.lora_fa"
    else:
        return "networks.lora"
    
# 文字列を変換する
def process_string(input_string:str) -> str:
    # スペースをアンダースコア(_)に置換
    replaced_spaces = input_string.replace(" ", "_")
    replaced_spaces = replaced_spaces.replace("(", "^(")
    replaced_spaces = replaced_spaces.replace(")", "^)")

    if replaced_spaces == "":
        replaced_spaces = "comment"

    return replaced_spaces

# optimizer_argsの設定
def get_optimizer_args(optimizer_type:str,sd_type:str) -> str:
    if optimizer_type == "AdaFactor" and sd_type == "SDXL":
        return f'"scale_parameter=False", "relative_step=False", "warmup_init=False" '
    elif optimizer_type == "AdaFactor":
        return f'"relative_step=True" "scale_parameter=True" "warmup_init=True" '
    elif optimizer_type == "prodigy":
        return f'"betas=0.9,0.999" "weight_decay=0" '
    elif optimizer_type == "DAdaptLion":
        return f'"weight_decay=0.2" "betas=0.9,0.99" '
    elif optimizer_type in ["DAdaptAdam","DAdaptLion"]:
        return f'"decouple=True" "weight_decay=0.2" "betas=0.9,0.99" '
    else:
        return ""
    
# lr_warmup_stepsの値を取得する
def lr_warmup_steps_from_rate(lr_warmup_steps:int,max_train_epochs:int,toml_path:str,images_count:int) -> int:
    # TOMLファイルを読み込む
    config = toml.load(toml_path)

    # num_repeatsの値を取得
    result = 0

    for data in config["datasets"]:
        num_repeats = data["num_repeats"]
        batch_size = data["batch_size"]

        result += math.floor(num_repeats * max_train_epochs * images_count / batch_size * lr_warmup_steps * 0.01)

    return result

# とあるフォルダの中にある画像ファイルの数
def count_images_recursive(folder_path:Any, image_extensions:list[str]=['.jpg', '.jpeg', '.png', '.gif', '.bmp',".webp"]) -> int:
    folder_path = Path(folder_path)
    
    if not folder_path.is_dir():
        raise ValueError("The provided path is not a directory.")

    image_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = Path(root) / file_name
            if file_path.suffix.lower() in image_extensions:
                image_count += 1

    return image_count

# tomlファイルのすべての[datasets][shuffle_caption]がtureかどうか
def all_prompt_shuffle(toml_path:str) -> bool:
    # TOMLファイルを読み込む
    config = toml.load(toml_path)
    return True
    #return all(list(map(lambda data:data.get("shuffle_caption"),config["datasets"])))
# cache_latents
def can_cache_latents(toml_path:str) -> bool:
    # TOMLファイルを読み込む
    config = toml.load(toml_path)
    return all(list(map(lambda data:data.get("color_aug") == False,config["datasets"])))

class Make_Lora:
    @staticmethod
    async def Image_Items(request:Request) -> dict[str,Any]:
        data = await request.json()
        folder_name = data.get('folderName')

        base,after = get_savefile_image_url_paths(folder_name)

        json_data = get_setting_file_json(folder_name)

        base_thumbnail,after_thumbnail = get_thumbnail_url_paths(folder_name)
        return {"base":base,"after":after,"base_thumbnail":base_thumbnail,"after_thumbnail":after_thumbnail,"image_items":json_data["imageLearningSetting"]["image_items"],"methods":json_data["imageLearningSetting"]["methods"],"loraData":json_data["loraData"]}
    
    @staticmethod
    async def Save_Data(request:Request) -> dict[str,str]:
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
                f.write(json.dumps(json_write, indent=2))
                

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

        user_setting = get_user_setting_json()

        lora_data = json_data["loraData"]

        #region
        # cmd = ["accelerate", "launch", "--num_cpu_threads_per_process",
        # str(lora_data["performance"]["cupThread"]), 
        # f"train_network.py",
        # f"--pretrained_model_name_or_path={find_file(lora_data['MainSetting']['useModel'],user_setting['sd-model-folder'])}",
        # f"--output_dir={output_folder}",
        # f"--output_name={lora_data['MainSetting']['outputFileName']}",
        # f"--dataset_config={os.path.join(main_folder,'setting.toml')}",
        # f"--max_train_epochs={lora_data['MainSetting']['epochs']}",
        # f"--mixed_precision={lora_data['MainSetting']['mixed_precision']}",
        # f"--gradient_checkpointing",
        # f"--sdpa",
        # f"--max_token_length=225",
        # f"--persistent_data_loader_workers",
        # f"--max_data_loader_n_workers={lora_data['performance']['workers']}",
        # f"--logging_dir={os.path.join(main_folder,'log')}",
        # f"--noise_offset=0.1",
        # f"--adaptive_noise_scale=0.01",
        # f"--multires_noise_iterations=6",
        # f"--multires_noise_discount=0.3",
        # f"--max_grad_norm=1.0",
        # f"--save_model_as=safetensors",
        # f"{use_optimizer_command(lora_data['MainSetting']['optimizer'])}",
        # f"{learning_content_command('')}",
        # f"--lr_scheduler={lora_data['learningSetting']['schduler']}",
        # f'--network_args {get_net_args(lora_data["MainSetting"]["loraType"].lower(), lora_data["netArgs"]["convDim"], lora_data["netArgs"]["convAlpha"], lora_data["netArgs"]["dropout"])}',
        # f"--max_train_steps=10000",
        # f"--learning_rate={lora_data['learningSetting']['learningRate']}",
        # f"--unet_lr={lora_data['learningSetting']['textEncoderLr']}",
        # f"--text_encoder_lr={lora_data['learningSetting']['unetLr']}",
        # f"--lr_scheduler_num_cycles=1",
        # f"--network_dim={lora_data['learningSetting']['networkDim']}",
        # f"--network_alpha={lora_data['learningSetting']['networkAlpha']}",
        # f"--network_module={get_network_module(lora_data['MainSetting']['loraType'].lower())}",
        # f"--training_comment={process_string(lora_data['MainSetting']['commentLine'])}",
        # f"--bucket_no_upscale",
        # f"--bucket_reso_steps=64",
        # f"--optimizer_args {get_optimizer_args(lora_data['MainSetting']['optimizer'],lora_data['MainSetting']['sdType'])}",
        # "--weighted_captions " if lora_data["MainSetting"]["optimizer"] == "prodigy" else "",
        # f"--lr_warmup_steps={lr_warmup_steps_from_rate(lora_data['learningSetting']['lrWarmupSteps'],lora_data['MainSetting']['epochs'],os.path.join(main_folder,'setting.toml'),count_images_recursive(os.path.join(main_folder,'dataset')))}",
        # f"--seed=1234",
        # "--clip_skip=2" if lora_data["MainSetting"]["sdType"] == "SD1.5" else "",
        # "--network_train_unet_only --no_half_vae" if lora_data["MainSetting"]["sdType"] == "SDXL" else "",
        # "--cache_text_encoder_outputs --cache_text_encoder_outputs_to_disk" if all_prompt_shuffle(os.path.join(main_folder,"setting.toml")) == False else "",
        # "--sample_every_n_epochs=1",
        # f"--sample_prompts={os.path.join(main_folder,'sample_prompt.txt')}",
        # "--sample_sampler=euler_a"]
        #endregion
        
        cmd = f"""accelerate launch --num_cpu_threads_per_process {lora_data['performance']['cupThread']} train_network.py ^
--pretrained_model_name_or_path={find_file(lora_data['MainSetting']['useModel'],user_setting['sd-model-folder'])} ^
--output_dir={output_folder} ^
--output_name={lora_data['MainSetting']['outputFileName']} ^
--dataset_config={os.path.join(main_folder,'setting.toml')} ^
--max_train_epochs={lora_data['MainSetting']['epochs']} ^
--mixed_precision="{lora_data['MainSetting']['mixed_precision']}" ^
--gradient_checkpointing ^
--sdpa ^
--max_token_length=225 ^
--persistent_data_loader_workers ^
--max_data_loader_n_workers={lora_data['performance']['workers']} ^
--logging_dir={os.path.join(main_folder,'log')} ^
--noise_offset=0.1 ^
--adaptive_noise_scale=0.01 ^
--multires_noise_iterations=6 ^
--multires_noise_discount=0.3 ^
--max_grad_norm=1.0 ^
--save_model_as=safetensors ^
{use_optimizer_command(lora_data['MainSetting']['optimizer'])} ^
--lr_scheduler={lora_data['learningSetting']['schduler']} ^
--network_args {get_net_args(lora_data["MainSetting"]["loraType"].lower(), lora_data["netArgs"]["convDim"], lora_data["netArgs"]["convAlpha"], lora_data["netArgs"]["dropout"])} ^
--max_train_steps=10000 ^
--learning_rate={lora_data['learningSetting']['learningRate']} ^
--unet_lr={lora_data['learningSetting']['textEncoderLr']} ^
--text_encoder_lr={lora_data['learningSetting']['unetLr']} ^
--lr_scheduler_num_cycles=1 ^
--network_dim={lora_data['learningSetting']['networkDim']} ^
--network_alpha={lora_data['learningSetting']['networkAlpha']} ^
--network_module={get_network_module(lora_data['MainSetting']['loraType'].lower())} ^
--training_comment={process_string(lora_data['MainSetting']['commentLine'])} ^
--bucket_no_upscale ^
--bucket_reso_steps=64 ^
--optimizer_args {get_optimizer_args(lora_data['MainSetting']['optimizer'],lora_data['MainSetting']['sdType'])} ^
{"--weighted_captions " if lora_data["MainSetting"]["optimizer"] == "prodigy" else ""} ^
--lr_warmup_steps={lr_warmup_steps_from_rate(lora_data['learningSetting']['lrWarmupSteps'],lora_data['MainSetting']['epochs'],os.path.join(main_folder,'setting.toml'),count_images_recursive(os.path.join(main_folder,'dataset')))} ^
--seed=1234 ^
{"--cache_latents --cache_latents_to_disk" if can_cache_latents(os.path.join(main_folder,"setting.toml")) else ""} ^
{f"--clip_skip=2" if lora_data["MainSetting"]["sdType"] == "sd1.5" else ""} ^
{"--network_train_unet_only --no_half_vae" if lora_data["MainSetting"]["sdType"] == "sdxl" else ""} ^
{"--cache_text_encoder_outputs --cache_text_encoder_outputs_to_disk" if all_prompt_shuffle(os.path.join(main_folder,"setting.toml")) == False else ""} ^
--sample_every_n_epochs=1 ^
--sample_prompts="{os.path.join(main_folder,'sample_prompt.txt')}" ^
--sample_sampler="euler_a"
        """

        #region

        # print(" ".join(cmd))

        # proc = await asyncio.create_subprocess_shell(
        #     f"call D:\\ai\\LyCORIS\\MyMade\\2ji\\anime\\k_on\\K_on_style02\\start_lora.bat",
        #     stdout=asyncio.subprocess.PIPE,
        #     stderr=asyncio.subprocess.PIPE)
        # while True:
        #     print(f"RETURN_CODE:{proc.returncode}")
        #     if proc.stdout.at_eof() and proc.stderr.at_eof():
        #         print("Break!!!!")
        #         break
        #     stdout = (await proc.stdout.readline()).decode('utf-8', 'replace')
        #     if stdout:
        #         print(f"STDOUT:{stdout}") 
        #     stderr = (await proc.stderr.readline()).decode('utf-8', 'replace')
        #     if stderr:
        #         print(stderr) 
        #     await asyncio.sleep(0.02)

        # await proc.communicate(input='cd & echo %CD%')
        #endregion
        
        command_txt_path = os.path.join(main_folder,"command.txt")
        command_bat_path = os.path.join(main_folder,"command.bat")

        mac_cmd = cmd.split("^")
        mac_cmd = list(map(lambda word:word.strip('\n'),mac_cmd))
        print(f"MAC_CMD:{mac_cmd}")
        mac_cmd_str = "".join(mac_cmd)
        with open(command_txt_path,mode="w",encoding='utf-8', newline='\n') as f:
            f.writelines([
                f"cd {user_setting['kohyass-folder']} \n"
                f".\\venv\Scripts\\activate \n"
                f"{mac_cmd_str}"
            ])
        
        with open(command_bat_path,mode="w",encoding='utf-8', newline='\n') as f:
            f.writelines([
                f"@echo on \n",
                f"call cd {user_setting['kohyass-folder']} \n"
                f"call .\\venv\Scripts\\activate \n"
                f"call {cmd}"
            ])

        result = subprocess.run(command_bat_path, shell=True)
        print(result)

        return {"message":"OK!!!"}
    
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

