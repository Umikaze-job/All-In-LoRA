import os
from typing import Any
from modules.folder_path import get_root_folder_path
from .core02 import ESRGANCore
import glob

class ESRGANManager:
    # model_nameには拡張子はつかない
    def __init__(self,image_path:str,output_folder_path:str,model_name:str,resize_scale:int) -> None:
        self.image_path = image_path
        self.output_folder_path = output_folder_path
        self.model_name = model_name
        self.resize_scale = resize_scale
    
    # リサイズした画像をtempファイルに作成する。
    def create_resize_image(self) -> None:
        ESRGANCore.main(model_name=self.model_name,output_folder_path=self.output_folder_path,resize_scale=self.resize_scale,input_image_path=self.image_path)