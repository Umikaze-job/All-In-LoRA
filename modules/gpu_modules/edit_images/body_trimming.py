from typing import List
from PIL import Image
from ultralytics import YOLO
import os
import math

from ...folder_path import get_root_folder_path

def get_model_folder():
    return os.path.join(get_root_folder_path(),"models","face_detect_models")

async def body_trimming(image:Image.Image,file_path:str,folder_name:str,data) -> List[Image.Image]:
    model = YOLO(os.path.join(get_model_folder(),data["modelname"]))

    result = model.predict(source=file_path, save=False, imgsz=800, conf=0.4, device=0)

    image_set:List[Image.Image] = []
    for index,xywh in enumerate(result[0].boxes.xywh.tolist()):
        crop_x,crop_y,crop_width,crop_height = xywh
        width,height = image.size

        # 切り取る範囲を12px広げる
        x_min = max(0,crop_x - abs(crop_width / 2) * data["spread_left"])
        y_min = max(0,crop_y - abs(crop_height / 2) * data["spread_top"])
        x_max = min(width, crop_x + abs(crop_width / 2) * data["spread_right"])
        y_max = min(height, crop_y + abs(crop_height / 2) * data["spread_bottom"])
        new_crop = image.crop((x_min,y_min,x_max,y_max))

        new_crop_width,new_crop_height = new_crop.size

        width_rate = data["width_rate"] / data["height_rate"] #幅をとれだけ大きくするか
        if width_rate < 1:
            width_rate = 0
        height_rate = data["height_rate"] / data["width_rate"] #高さをとれだけ大きくするか 
        if height_rate < 1:
            height_rate = 0

        if width_rate != 0:
            x_min = max(0,x_min - new_crop_width * width_rate / 2 - new_crop_width / 2)
            x_max = min(width,x_max + new_crop_width * width_rate / 2 - new_crop_width / 2)

        if height_rate != 0:
            y_max = min(height,y_max + new_crop_height * height_rate - new_crop_height)

        image_set.append(image.crop((x_min,y_min,x_max,y_max)))

    return image_set