import os
from typing import Any
from modules.folder_path import get_root_folder_path
from .core import ESRGANCore
import glob

class ESRGANManager:
    def __init__(self,image_path:str,output_folder_path:str,temp_folder_path:str,model_name:str) -> None:
        self.image_path = image_path
        self.output_folder_path = output_folder_path
        self.model_path = self.get_model(model_name=model_name)
        self.temp_folder_path = temp_folder_path

    def get_model(self,model_name:str) -> Any:
        model_folder = os.path.join(get_root_folder_path(),"models","esrgan_models")
        if os.path.isdir(os.path.join(model_folder,model_name)) == False:
            raise Exception("指定したファイルは存在しませんでした")
        
        files = glob.glob(os.path.join(model_folder,model_name,"*.pth"))
        if len(files) == 0:
            raise Exception("フォルダの中にモデルは存在しませんでした")
        
        return files[0]
    
    # リサイズした画像をtempファイルに作成する。
    def create_resize_image(self) -> None:
        ESRGANCore.upscale(model_path=self.model_path,output_path=self.output_folder_path,temp_folder_path=self.temp_folder_path)