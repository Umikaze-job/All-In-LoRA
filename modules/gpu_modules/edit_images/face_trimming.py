from typing import List
from PIL import Image
from ultralytics import YOLO
import os

from ...folder_path import get_root_folder_path

def get_model_folder():
    return os.path.join(get_root_folder_path(),"models","face_detect_models")

async def face_trimming(image:Image.Image,file_path:str,folder_name:str,data) -> List[Image.Image]:
    model = YOLO(os.path.join(get_model_folder(),data["modelname"]))

    result = model.predict(source=file_path, save=False, imgsz=800, conf=0.4, device=0)

    image_set:List[Image.Image] = []
    for xyxy in result[0].boxes.xyxy.tolist():
        x_min, y_min, x_max, y_max = xyxy
        width,height = image.size

        # 切り取る範囲を12px広げる
        x_min = max(0,x_min - data["spread_left"])
        y_min = max(0,y_min - data["spread_top"])
        x_max = min(width, x_max + data["spread_right"])
        y_max = min(height, y_max + data["spread_bottom"])
        crop = image.crop((x_min,y_min,x_max,y_max))

        image_set.append(crop)

    return image_set
        