import os.path as osp
import glob
from typing import Any
import cv2
import numpy as np
import torch
from .RRDBNet_arch import RRDBNet
import os
from PIL import Image

class ESRGANCore:

    # model_path: .pthが拡張子であるESRGANモデル
    @staticmethod
    def upscale(model_path:str,output_path:str,temp_folder_path:str) -> None:
        device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu
        # device = torch.device('cpu')

        test_img_folder = 'LR/*'

        model = RRDBNet(3, 3, 64, 23, gc=32)
        model.load_state_dict(torch.load(model_path), strict=False)
        model.eval()
        model = model.to(device)

        print('Model path {:s}. \nTesting...'.format(model_path))

        idx = 0
        for path in glob.glob(os.path.join(temp_folder_path,"*")):
            idx += 1
            base = osp.splitext(osp.basename(path))[0]
            print(idx, base)
            # read images
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            img = img * 1.0 / 255
            img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
            img_LR = img.unsqueeze(0)
            img_LR = img_LR.to(device)

            with torch.no_grad():
                output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
            output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
            output = (output * 255.0).round()
            cv2.imwrite(os.path.join(output_path,"output.png"), output)