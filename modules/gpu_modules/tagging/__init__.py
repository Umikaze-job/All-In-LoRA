from typing import Any
from onnxruntime import InferenceSession
import onnxruntime as ort
from PIL import Image
import numpy as np
import csv
import os
from modules.folder_path import get_root_folder_path
from huggingface_hub import hf_hub_download
import glob

__all__ = ["TaggingManager"]

class TaggingManager:
    # model_nameには拡張子がない
    def __init__(self,model_name:str) -> None:
        self.model_name = model_name
        self.folder_exist_check()
        self.tagging_model = self.ready_model()
        self.csv = self.ready_csv()

    @property
    def models_path(self) -> str:
        return os.path.join(get_root_folder_path(),"models","tagger_models")
    
    @property
    def folder_path(self) -> str:
        return os.path.join(self.models_path,self.model_name)
    
    # フォルダの存在を確認して、なかったらダウンロードする
    def folder_exist_check(self) -> None:
        if os.path.exists(self.folder_path) == False:
            hf_hub_download(repo_id=f"SmilingWolf/{self.model_name}",filename="model.onnx",local_dir=self.folder_path)
            hf_hub_download(repo_id=f"SmilingWolf/{self.model_name}",filename="selected_tags.csv",local_dir=self.folder_path)

    def ready_model(self) -> InferenceSession:
        files = glob.glob(os.path.join(self.folder_path,"*.onnx"))
        if len(files) == 0:
            raise Exception("モデルを読み込めませんでした")
        return InferenceSession(files[0], providers=ort.get_available_providers())
    
    def ready_csv(self) -> str:
        files = glob.glob(os.path.join(self.folder_path,"*.csv"))
        if len(files) == 0:
            raise Exception("csvを読み込めませんでした")
        return files[0]
    
    async def do_tagging(self,image:Image.Image,threshold:float, character_threshold:float, exclude_tags:str, trigger_name:str) -> list[str]:
        input = self.tagging_model.get_inputs()[0]
        height = input.shape[1]

        # Reduce to max size and pad with white
        ratio = float(height)/max(image.size)
        new_size = tuple([int(x*ratio) for x in image.size])
        image = image.resize(new_size, Image.LANCZOS)
        square = Image.new("RGB", (height, height), (255, 255, 255))
        square.paste(image, ((height-new_size[0])//2, (height-new_size[1])//2))

        image = np.array(square).astype(np.float32)
        image = image[:, :, ::-1]  # RGB -> BGR
        image = np.expand_dims(image, 0)

        # Read all tags from csv and locate start of each category
        tags = []
        general_index = None
        character_index = None
        with open(self.csv) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if general_index is None and row[2] == "0":
                    general_index = reader.line_num - 2
                elif character_index is None and row[2] == "4":
                    character_index = reader.line_num - 2
                tags.append(row[1])

        label_name = self.tagging_model.get_outputs()[0].name
        probs = self.tagging_model.run([label_name], {input.name: image})[0]

        result = list(zip(tags, probs[0]))

        # rating = max(result[:general_index], key=lambda x: x[1])
        general = [item for item in result[general_index:character_index] if item[1] > threshold]
        character = [item for item in result[character_index:] if item[1] > character_threshold]

        all = character + general
        remove = [s.strip() for s in exclude_tags.lower().split(",")]
        all = [tag for tag in all if tag[0] not in remove]
        all.insert(0,[trigger_name]) if trigger_name != "" else print("No Trigger Word")

        res = ", ".join((item[0].replace("_"," ") for item in all))

        res_list = res.split(",")
        res_list = list(map(lambda word:word.strip(),res_list))

        return res_list