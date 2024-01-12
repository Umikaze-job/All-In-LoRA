import json
import math
import os
import re
import shutil
import subprocess
import toml
from pathlib import Path
from typing import Any
from modules.folder_path import get_savefiles
from modules.file_util import get_user_setting_json
from modules.class_definition.user_setting_manager import UserSettingManager
"""
FineTuningFolderManager:fine_tuning_folderフォルダの管理をするマネージャー
"""

class FineTuningFolderManager:
    
    def __init__(self,folder_name:str) -> None:
        self.folder_path = os.path.join(get_savefiles(),folder_name,"fine_tuning_folder")
        self.user_setting = get_user_setting_json()
        self.user_setting_manager = UserSettingManager()

    # ルートデータセットのフォルダパス
    @property
    def root_dataset_folder_path(self) -> str:
        return os.path.join(self.folder_path,"dataset")

    # ログファイルのパス
    @property
    def log_folder_path(self) -> str:
        return os.path.join(self.folder_path,"log")
    
    # アウトプットフォイルの作成
    @property
    def output_folder_path(self) -> str:
        return os.path.join(self.folder_path,"output")
    
    #tomlファイルのパス
    @property
    def toml_file_path(self) -> str:
        return os.path.join(self.folder_path,"setting.toml")
    
    #Sample_Promptファイルのパス
    @property
    def sample_prompt_file_path(self) -> str:
        return os.path.join(self.folder_path,"sample_prompt.txt")
    
    #commant.batファイルのパス
    @property
    def command_bat_file_path(self) -> str:
        return os.path.join(self.folder_path,"command.bat")
    
    #commant.txtファイルのパス
    @property
    def command_txt_file_path(self) -> str:
        return os.path.join(self.folder_path,"command.txt")
    
    # データセットが含まれているフォルダの取得
    def get_dataset_folder_path(self,count:int) -> str:
        return os.path.join(self.root_dataset_folder_path,f"image{str(count).rjust(3, '0')}")

    # フォルダの中身をリセットする
    def folder_init(self) -> None:
        shutil.rmtree(self.folder_path)
        os.mkdir(self.folder_path)

    # すべてのフォルダを作成する
    def make_all_folders(self,img_folder_count:int) -> None:
        os.makedirs(self.root_dataset_folder_path,exist_ok=True)
        os.makedirs(self.log_folder_path,exist_ok=True)
        os.makedirs(self.output_folder_path,exist_ok=True)

        for count in range(img_folder_count):
            os.makedirs(self.get_dataset_folder_path(count))

    # 学習方法に従って画像を決まったフォルダに入れる
    # image_paths:特定の学習方法が指定されているImage_folderとCharacter_trimmimg_folderの画像
    def move_images_to_folder(self,folder_index:int,image_paths:list[str]) -> None:
        for path in image_paths:
            shutil.copy(path,self.get_dataset_folder_path(folder_index))

    # meta_data.jsonを作成する
    def make_meta_data(self,folder_index:int,images_data:list[dict[str,str]]) -> None:
        json_write:dict = {}
        for data in images_data:
            if data.get("file_path") == None or data.get("file_path") == "":
                continue
            data["file_path"] = os.path.join(self.get_dataset_folder_path(folder_index),os.path.basename(data["file_path"]))
            if data.get("caption") != None and  data.get("caption") != "":
                if json_write.get(data["file_path"]) == None:
                    json_write[data["file_path"]] = {}
                json_write[data["file_path"]]["caption"] = data.get("caption")

            if data.get("tags") != None and data.get("tags") != [""]:
                if json_write.get(data["file_path"]) == None:
                    json_write[data["file_path"]] = {}
                json_write[data["file_path"]]["tags"] = ", ".join(data["tags"])

        #? メタデータに書き込む
        with open(os.path.join(self.get_dataset_folder_path(folder_index),"meta_data.json"),"w") as f:
            f.write(json.dumps(json_write, indent=2))
    
    # tomlファイルを作成する.
    def make_toml_file(self,method_data:list[dict[str,Any]]) -> None:
        toml = ""
        for index,met in enumerate(method_data):
            image_dir = self.get_dataset_folder_path(index).replace("\\", "\\\\")
            meta_file = os.path.join(self.get_dataset_folder_path(index),"meta_data.json").replace("\\", "\\\\")
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
image_dir = "{image_dir}"
metadata_file = "{meta_file}"
"""
        
        with open(self.toml_file_path,"w") as f:
            f.write(toml)

    # サンプル画像をつくるときのプロンプトファイルを作成
    def make_sample_prompt_file(self,sample:dict[str,Any]) -> None:
        trigger_word = ""
        if sample.get('triggerWord') != None and sample.get('triggerWord') != "":
            trigger_word = f"{sample['triggerWord']},"
        with open(self.sample_prompt_file_path, 'w') as sample_prompt_file:
            # ここに sample_prompt.txt の内容を書き込む処理を追加
            sample_prompt_file.write(f"{trigger_word}{sample['positivePrompt']} --n {sample['negativePrompt']} --w {sample['width']} --h {sample['height']} --d 1 --l 7.5 --s {sample['steps']}")

    # コマンドの実行
    async def execute_bat_file(self) -> None:
        result = subprocess.run(self.command_bat_file_path, shell=True)
        print(result)

    # outputフォルダの中にあるものをすべてLoRAフォルダへ
    def output_files_to_lora_folder(self,lora_data:dict[str,Any]) -> None:
        file_name = lora_data['MainSetting']['outputFileName']
        file_name = re.sub(r".safetensors$","",file_name)
        os.makedirs(os.path.join(self.user_setting_manager.Lora_Folder,file_name),exist_ok=True)
        os.makedirs(os.path.join(self.user_setting_manager.Lora_Folder,file_name,"sample"),exist_ok=True)
        for root, dirs, files in os.walk(self.output_folder_path):
            # 画像を移動する
            if len(dirs) == 0:
                for file in files:
                    shutil.copy(os.path.join(root,file),os.path.join(self.user_setting_manager.Lora_Folder,file_name,"sample"))
            # Loraファイルをコピーする
            else:
                for file in files:
                    shutil.copy(os.path.join(root,file),os.path.join(self.user_setting_manager.Lora_Folder,file_name))
        
    
    #=============ここからbatファイル関係=============
            
    def make_bat_file(self,lora_data:dict[str,Any]) -> None:
        cmd = f"""accelerate launch --num_cpu_threads_per_process {lora_data['performance']['cupThread']} train_network.py ^
--pretrained_model_name_or_path={self.find_file(lora_data['MainSetting']['useModel'],self.user_setting['sd-model-folder'])} ^
--output_dir={self.output_folder_path} ^
--output_name={lora_data['MainSetting']['outputFileName']} ^
--dataset_config={self.toml_file_path} ^
--max_train_epochs={lora_data['MainSetting']['epochs']} ^
--mixed_precision="{lora_data['MainSetting']['mixed_precision']}" ^
--gradient_checkpointing ^
--sdpa ^
--max_token_length=225 ^
--persistent_data_loader_workers ^
--max_data_loader_n_workers={lora_data['performance']['workers']} ^
--logging_dir={self.log_folder_path} ^
--noise_offset=0.1 ^
--adaptive_noise_scale=0.01 ^
--multires_noise_iterations=6 ^
--multires_noise_discount=0.3 ^
--max_grad_norm=1.0 ^
--save_model_as=safetensors ^
{self.use_optimizer_command(lora_data['MainSetting']['optimizer'])} ^
--lr_scheduler={lora_data['learningSetting']['schduler']} ^
--network_args {self.get_net_args(lora_data)} ^
--max_train_steps=10000 ^
--learning_rate={lora_data['learningSetting']['learningRate']} ^
--unet_lr={lora_data['learningSetting']['textEncoderLr']} ^
--text_encoder_lr={lora_data['learningSetting']['unetLr']} ^
--lr_scheduler_num_cycles=1 ^
--network_dim={lora_data['learningSetting']['networkDim']} ^
--network_alpha={lora_data['learningSetting']['networkAlpha']} ^
--network_module={self.get_network_module(lora_data['MainSetting']['loraType'].lower())} ^
--training_comment={self.process_string(lora_data['MainSetting']['commentLine'])} ^
--bucket_no_upscale ^
--bucket_reso_steps=64 ^
--optimizer_args {self.get_optimizer_args(lora_data=lora_data)} ^
{"--weighted_captions " if lora_data["MainSetting"]["optimizer"] == "prodigy" else ""} ^
--lr_warmup_steps={self.lr_warmup_steps_from_rate(lora_data=lora_data)} ^
--seed=1234 ^
{"--cache_latents --cache_latents_to_disk" if self.can_cache_latents() else ""} ^
{f"--clip_skip=2" if lora_data["MainSetting"]["sdType"] == "sd1.5" else ""} ^
{"--network_train_unet_only --no_half_vae" if lora_data["MainSetting"]["sdType"] == "sdxl" else ""} ^
{"--cache_text_encoder_outputs --cache_text_encoder_outputs_to_disk" if self.all_prompt_shuffle() == False else ""} ^
--sample_every_n_epochs=1 ^
--sample_prompts="{self.sample_prompt_file_path}" ^
--sample_sampler="euler_a"
        """

        mac_cmd = cmd.split("^")
        mac_cmd = list(map(lambda word:word.strip('\n'),mac_cmd))
        print(f"MAC_CMD:{mac_cmd}")
        mac_cmd_str = "".join(mac_cmd)
        with open(self.command_txt_file_path,mode="w",encoding='utf-8', newline='\n') as f:
            f.writelines([
                f"cd {self.user_setting['kohyass-folder']} \n"
                f".\\venv\Scripts\\activate \n"
                f"{mac_cmd_str}"
            ])
        
        with open(self.command_bat_file_path,mode="w",encoding='utf-8', newline='\n') as f:
            f.writelines([
                f"@echo on \n",
                f"call cd {self.user_setting['kohyass-folder']} \n"
                f"call .\\venv\Scripts\\activate \n"
                f"call {cmd}"
            ])

    #region make_bat_fileで使用する処理
    
    # sd_modelのパス
    def find_file(self,file_name:str, search_path:str) -> str | None:
        for root, dirs, files in os.walk(search_path):
            if file_name in files:
                return os.path.join(root, file_name)
        return None
    
    # オプティマイザー系のコマンド
    def use_optimizer_command(self,optimizer_type:str) -> str:
        if optimizer_type in ["Lion"]:
            return "--use_lion_optimizer"
        elif optimizer_type == "AdamW8bit":
            return "--use_8bit_adam"
        else:
            return f"--optimizer_type={optimizer_type}"
        
    # net_argsの取得
    def get_net_args(self,lora_data:dict[str,Any]) -> str:
        lora_type = lora_data["MainSetting"]["loraType"].lower()
        conv_dim = lora_data["netArgs"]["convDim"]
        conv_alpha = lora_data["netArgs"]["convAlpha"]
        dropout = lora_data["netArgs"]["dropout"]
        block_size = 16
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
    def get_network_module(self,lora_type:str) -> str:
        if (lora_type in ["lokr","locon","loha"]):
            return "lycoris.kohya"
        elif (lora_type == "dylora"):
            return "networks.dylora"
        elif (lora_type == "LoRA-FA"):
            return "networks.lora_fa"
        else:
            return "networks.lora"
        
    # 文字列を変換する
    def process_string(self,input_string:str) -> str:
        # スペースをアンダースコア(_)に置換
        replaced_spaces = input_string.replace(" ", "_")
        replaced_spaces = replaced_spaces.replace("(", "^(")
        replaced_spaces = replaced_spaces.replace(")", "^)")

        if replaced_spaces == "":
            replaced_spaces = "comment"

        return replaced_spaces
    
    # optimizer_argsの設定
    def get_optimizer_args(self,lora_data:dict[str,Any]) -> str:
        optimizer_type = lora_data['MainSetting']['optimizer']
        sd_type = lora_data['MainSetting']['sdType']

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
    def lr_warmup_steps_from_rate(self,lora_data:dict[str,Any]) -> int:
        lr_warmup_steps:int = lora_data['learningSetting']['lrWarmupSteps']
        max_train_epochs:int = lora_data['MainSetting']['epochs']
        toml_path:str = self.toml_file_path
        images_count:int = self.count_images_recursive()
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
    def count_images_recursive(self) -> int:
        image_count = 0

        for root, dirs, files in os.walk(self.root_dataset_folder_path):
            for file_name in files:
                file_path = Path(root) / file_name
                if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp',".webp"]:
                    image_count += 1

        return image_count
    
    # tomlファイルのすべての[datasets][shuffle_caption]がtureかどうか
    def all_prompt_shuffle(self) -> bool:
        # TOMLファイルを読み込む
        config = toml.load(self.toml_file_path)
        return True
        #return all(list(map(lambda data:data.get("shuffle_caption"),config["datasets"])))
    
    # cache_latentsコマンドが使えるかどうか
    def can_cache_latents(self) -> bool:
        # TOMLファイルを読み込む
        config = toml.load(self.toml_file_path)
        return all(list(map(lambda data:data.get("color_aug") == False,config["datasets"])))
    
    #endregion
            