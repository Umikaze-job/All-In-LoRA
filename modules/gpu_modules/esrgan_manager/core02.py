import argparse
import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url

from modules.folder_path import get_root_folder_path

from .realesrgan import RealESRGANer
import requests

class ESRGANCore:
    @staticmethod
    def main(model_name:str,output_folder_path:str,resize_scale:int,input_image_path:str) -> None:
        """Inference demo for Real-ESRGAN.
        """
        # region parser = argparse.ArgumentParser()
        # parser.add_argument('-i', '--input', type=str, default='inputs', help='Input image or folder')
        # parser.add_argument(
        #     '-n',
        #     '--model_name',
        #     type=str,
        #     default='RealESRGAN_x4plus',
        #     help=('Model names: RealESRGAN_x4plus | RealESRNet_x4plus | RealESRGAN_x4plus_anime_6B | RealESRGAN_x2plus | '
        #           'realesr-animevideov3 | realesr-general-x4v3'))
        # parser.add_argument('-o', '--output', type=str, default='results', help='Output folder')
        # parser.add_argument(
        #     '-dn',
        #     '--denoise_strength',
        #     type=float,
        #     default=0.5,
        #     help=('Denoise strength. 0 for weak denoise (keep noise), 1 for strong denoise ability. '
        #           'Only used for the realesr-general-x4v3 model'))
        # parser.add_argument('-s', '--outscale', type=float, default=4, help='The final upsampling scale of the image')
        # parser.add_argument(
        #     '--model_path', type=str, default=None, help='[Option] Model path. Usually, you do not need to specify it')
        # parser.add_argument('--suffix', type=str, default='out', help='Suffix of the restored image')
        # parser.add_argument('-t', '--tile', type=int, default=0, help='Tile size, 0 for no tile during testing')
        # parser.add_argument('--tile_pad', type=int, default=10, help='Tile padding')
        # parser.add_argument('--pre_pad', type=int, default=0, help='Pre padding size at each border')
        # parser.add_argument('--face_enhance', action='store_true', help='Use GFPGAN to enhance face')
        # parser.add_argument(
        #     '--fp32', action='store_true', help='Use fp32 precision during inference. Default: fp16 (half precision).')
        # parser.add_argument(
        #     '--alpha_upsampler',
        #     type=str,
        #     default='realesrgan',
        #     help='The upsampler for the alpha channels. Options: realesrgan | bicubic')
        # parser.add_argument(
        #     '--ext',
        #     type=str,
        #     default='auto',
        #     help='Image extension. Options: auto | jpg | png, auto means using the same extension as inputs')
        # parser.add_argument(
        #      '-g', '--gpu-id', type=int, default=None, help='gpu device to use (default=None) can be 0,1,2 for multi-gpu')

        # endregion args = parser.parse_args()
        
        # ここまでargsの定義
        # determine models according to model names
        # args.model_name = args.model_name.split('.')[0]
        model = None
        netscale = 0
        file_url:str = ""
        if model_name == 'RealESRGAN_x4plus':  # x4 RRDBNet model
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            netscale = 4
            file_url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
        elif model_name == 'RealESRNet_x4plus':  # x4 RRDBNet model
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            netscale = 4
            file_url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth'
        elif model_name == 'RealESRGAN_x4plus_anime_6B':  # x4 RRDBNet model with 6 blocks
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
            netscale = 4
            file_url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth'
        elif model_name == 'RealESRGAN_x2plus':  # x2 RRDBNet model
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
            netscale = 2
            file_url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth'
        else:
            raise Exception("そのようなモデルは存在しません")

        # determine model paths
        model_path = os.path.join(get_root_folder_path(),"models","esrgan_models",f"{model_name}.pth")

        # region use dni to control the denoise strength
        # dni_weight = None
        # if args.model_name == 'realesr-general-x4v3' and args.denoise_strength != 1:
        #     wdn_model_path = model_path.replace('realesr-general-x4v3', 'realesr-general-wdn-x4v3')
        #     model_path = [model_path, wdn_model_path]
        #     dni_weight = [args.denoise_strength, 1 - args.denoise_strength]
        # endregion

        # モデルがなければダウンロードする
        if os.path.exists(model_path) == False:
            # ダウンロード対象のURLからデータを取得
            response = requests.get(file_url)

            # 取得したデータをファイルに書き込む
            with open(model_path, 'wb') as file:
                file.write(response.content)

        # restorer
        upsampler = RealESRGANer(
            scale=netscale,
            model_path=model_path,
            dni_weight=None,
            model=model,
            tile=0,
            tile_pad=10,
            pre_pad=10,
            half=False,
            gpu_id=0)

        # region if args.face_enhance:  # Use GFPGAN for face enhancement
        #     from gfpgan import GFPGANer
        #     face_enhancer = GFPGANer(
        #         model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
        #         upscale=args.outscale,
        #         arch='clean',
        #         channel_multiplier=2,
        # endregion         bg_upsampler=upsampler)

        paths = [input_image_path]

        for idx, path in enumerate(paths):
            imgname, extension = os.path.splitext(os.path.basename(path))
            print('Testing', idx, imgname)

            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if len(img.shape) == 3 and img.shape[2] == 4:
                img_mode = 'RGBA'
            else:
                img_mode = None

            try:
                output, _ = upsampler.enhance(img, outscale=resize_scale) #これが拡大処理
            except RuntimeError as error:
                print('Error', error)
                print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')

            extension = "webp"

            save_path = os.path.join(output_folder_path,f'{imgname}.{extension}')

            cv2.imwrite(save_path, output)