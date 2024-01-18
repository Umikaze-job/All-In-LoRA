import glob
from typing import Any, List
from modules.folder_path import get_root_folder_path
from PIL import Image
from ultralytics import YOLO
import os
from huggingface_hub import hf_hub_download

class EditWithFaceDetect:
    def __init__(self,model_name:str) -> None:
        self.model = self.get_model_path(model_name=model_name)

    @property
    def model_folder(self) -> str:
        return os.path.join(get_root_folder_path(),"models","face_detect_models")
    
    def get_model_path(self,model_name:str) -> Any:
        try:
            folder_name = os.path.join(self.model_folder,model_name)
            if os.path.isdir(folder_name) == False:
                self.download_model(model_name=model_name)
            
            files = glob.glob(os.path.join(folder_name,"*.pt"))

            if len(files) == 0:
                raise Exception("そのようなモデルはありません")
            
            return files[0]
        except Exception as e:
            return {"error":e}
        
    def download_model(self,model_name:str) -> None:
        model_name_pool = ["anime-face-detect01"]
        if len(list(filter(lambda name:name == model_name,model_name_pool))) != 0:
            model_folder = os.path.join(self.model_folder,model_name)
            os.makedirs(model_folder)
            hf_hub_download(repo_id="Umikaze-job/anime-face-detect01",filename="anime-face.pt",local_dir=model_folder)