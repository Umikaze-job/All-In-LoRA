import os
import glob
from typing import Any
import cv2

import numpy as np
from modules.folder_path import get_root_folder_path,get_localhost_name
from .Interface.folder_manager_interface import FolderManagerParent
from modules.class_definition.json_manager import SaveFilesSettingImageFolderManager
from fastapi import Request, UploadFile, Form, File
from PIL import Image
import io

"""
ImageFolderManager:savefiles/<fileName>/images_folderの処理や別のフォルダに画像をコピーする処理をする
また、json形式の画像データも管理する
images_folderはデータベースの画像を置くフォルダである
"""
class ImageFolderManager(FolderManagerParent):

    def __init__(self,folder_name:str) -> None:
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"images_folder")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"images_folder")
        super().__init__(folder_name,folder_path,url_path)

        self.Image_Data_Manager = SaveFilesSettingImageFolderManager(folder_name=folder_name)

    def get_all_url_paths(self) -> list[str]:
        return super().get_all_url_paths()

    # 画像をフォルダに入力する
    async def Input_Image(self,image:Image.Image,file_name:str,image_format:str) -> None:
        await super().Input_Image(image,file_name)
        #webpファイルに変える
        my_file_name = file_name

        #一旦保存
        image.save(os.path.join(self.folder_path,f"{my_file_name}.{image_format}"),format=image_format)

        # 入力画像を読み込み(-1指定でαチャンネルも読み取る)
        img = cv2.imread(os.path.join(self.folder_path,f"{my_file_name}.{image_format}"), cv2.IMREAD_UNCHANGED)
        # αチャンネルが0となるインデックスを取得
        # ex) ([0, 1, 3, 3, ...],[2, 4, 55, 66, ...])
        # columnとrowがそれぞれ格納されたタプル(長さ２)となっている
        if img.shape[2] == 4:  # アルファチャンネルがある場合
            # αチャンネルが0となるインデックスを取得
            index = np.where(img[:, :, 3] == 0)
            # 白塗りする
            img[index] = [255, 255, 255, 255]
            # アルファチャンネルが1-254の場合、元の色を維持しつつ不透明度を保持
            alpha_nonzero_indices = np.where((img[:, :, 3] > 0) & (img[:, :, 3] < 255))
            img[alpha_nonzero_indices[:2]] = img[alpha_nonzero_indices[:2]] * (255 / img[alpha_nonzero_indices[0], alpha_nonzero_indices[1], 3])[:, None]
            # 出力
            cv2.imwrite(os.path.join(self.folder_path, f"{my_file_name}.{image_format}"), img)


            

    

