import glob
import os
from ..folder_path import get_root_folder_path,get_localhost_name
from .Interface.folder_manager_interface import FolderManagerParent
from fastapi import Request, UploadFile, Form, File
import shutil
from PIL import Image
import io
import numpy as np
import cv2

"""
ThumbnailBaseFolderManager:savefiles/<fileName>/thumbnail_folder/baseの処理や別のフォルダに画像をコピーする処理をする
thumbnail_folder/baseはデータベースの画像のサムネイルを置くフォルダである
"""
class ThumbnailBaseFolderManager(FolderManagerParent):

    def __init__(self,folder_name):
        folder_path = os.path.join(get_root_folder_path(),"savefiles",folder_name,"thumbnail_folder","base")
        url_path = os.path.join(get_localhost_name(),"savefiles",folder_name,"thumbnail_folder","base")
        super().__init__(folder_name,folder_path,url_path)

    def get_all_url_paths(self):
        return super().get_all_url_paths()

    # 画像をフォルダに入力する
    async def Input_Image(self,image:Image.Image,file_name:str):
        #webpファイルに変える
        my_file_name = os.path.splitext(os.path.basename(file_name))[0]

        #一旦保存
        image.thumbnail((600,400))
        image.save(os.path.join(self.folder_path,f"{my_file_name}.webp"),format="webp",quality=50)

        # 入力画像を読み込み(-1指定でαチャンネルも読み取る)
        img = cv2.imread(os.path.join(self.folder_path,f"{my_file_name}.webp"), cv2.IMREAD_UNCHANGED)
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
            cv2.imwrite(os.path.join(self.folder_path, f"{my_file_name}.webp"), img)