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
    for index,xyxy in enumerate(result[0].boxes.xyxy.tolist()):
        x_min, y_min, x_max, y_max = xyxy
        _,_,crop_width,crop_height = result[0].boxes.xywh.tolist()[index]
        print(f"crop_size{index}:{crop_width},{crop_height}")
        width,height = image.size

        width_rate = data["width_rate"] / data["height_rate"] #幅をとれだけ大きくするか
        if width_rate < 1:
            width_rate = 0
        height_rate = data["height_rate"] / data["width_rate"] #高さをとれだけ大きくするか 
        if height_rate < 1:
            height_rate = 0
        # 切り取る範囲を12px広げる
        x_min = max(0,math.floor(x_min - data["spread_left"] - crop_width * width_rate / 2))
        y_min = max(0,y_min - data["spread_top"])
        x_max = min(width, math.floor(x_max + data["spread_right"] + crop_width * width_rate / 2))
        y_max = min(height, math.floor(y_max + data["spread_bottom"] + crop_height * height_rate))
        print(f"max{index}:{x_max},{y_max}")
        crop = image.crop((x_min,y_min,x_max,y_max))

        image_set.append(crop)

    return image_set