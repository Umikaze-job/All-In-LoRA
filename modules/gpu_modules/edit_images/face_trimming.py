from typing import Any, List
from PIL import Image
from ultralytics import YOLO
import os

from modules.folder_path import get_root_folder_path
from .edit_with_facedetect import EditWithFaceDetect

class FaceTrimmingManager(EditWithFaceDetect):

    async def face_trimming(self,image:Image.Image,file_path:str,folder_name:str,data:Any) -> List[Image.Image]:
        model = YOLO(self.model)

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
            crop = image.crop((x_min,y_min,x_max,y_max))

            image_set.append(crop)

        return image_set
        