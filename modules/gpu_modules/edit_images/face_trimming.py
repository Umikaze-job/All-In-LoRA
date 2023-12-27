from PIL import Image
from ultralytics import YOLO
import os

from ...folder_path import get_root_folder_path,get_savefiles

def get_model_folder():
    return os.path.join(get_root_folder_path(),"models","face_detect_models")

async def face_trimming(image:Image,file_path:str,folder_name:str,model_name:str = "anime-face-best.pt"):
    model = YOLO(os.path.join(get_model_folder(),model_name))

    result = model.predict(source=file_path, save=False, imgsz=800, conf=0.4, device=0)

    for xyxy in result[0].boxes.xyxy.tolist():
        crop = image.crop((xyxy[0],xyxy[1],xyxy[2],xyxy[3]))

        crop.show()
        