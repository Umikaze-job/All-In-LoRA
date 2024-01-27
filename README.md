# All-In-LoRA
From dataset construction to LoRA training, all in one app.

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](/example/example01.png)

## Features

- Prepare image data.
- Preparing text data.
- Image data processing.
- Automatic generation of text data.
- Editing text data.
- Creating a learning directory.
- Creation of toml files.
- Creation of learning bat and shell files.
- **All in one App.**

## Installation and Running

### Automatic Installation on Windows

#### Windows Required Dependencies

Python 3.10.6 and Git:
 
- Python 3.10.6: https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe
- git: https://git-scm.com/download/win

Give unrestricted script access to powershell so venv can work:

- Open an administrator powershell window
- Type `Set-ExecutionPolicy Unrestricted` and answer A
- Close admin powershell window

#### Automatic Setup on Windows

1. Install `CUDA 11.8` + `CUDNN`.
2. Run `install.bat`
3. Run `start.bat`
4. Open `http://127.0.0.1:8000`

#### Manual Setup

1. Install `CUDA 11.8` + `CUDNN`.
2. Enter the following command to create a python virtual environment:
```
git clone https://github.com/Umikaze-job/All-In-LoRA
cd All-In-LoRA

py -3.10 -m venv venv
.\venv\Scripts\activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

pip install -r requirements.txt
deactivate
```
3. Install sd-scripts on the `tools` folder and create a python virtual environment for sd-scripts:
```
cd tools
git clone https://github.com/kohya-ss/sd-scripts.git
cd sd-scripts

py -3.10 -m venv venv
.\venv\Scripts\activate

pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118
pip install --upgrade -r requirements.txt
pip install xformers==0.0.20

accelerate config
```
Note: Now bitsandbytes is optional. Please install any version of bitsandbytes as needed. Installation instructions are in the following section.

Answers to accelerate config:
```
- This machine
- No distributed training
- NO
- NO
- NO
- all
- fp16
```

note: Some user reports ValueError: fp16 mixed precision requires a GPU is occurred in training. In this case, answer 0 for the 6th question: What GPU(s) (by id) should be used for training on this machine as a comma-separated list? [all]:

(Single GPU with id 0 will be used.)

##### Optional: Use `bitsandbytes` (8bit optimizer)

Please install the Windows version from the command below.
```
python -m pip install bitsandbytes==0.41.1 --prefer-binary --extra-index-url=https://jllllll.github.io/bitsandbytes-windows-webui
```

4. Install additional required packages in sd-scripts
```
cd ../../
pip install -r requirements-kohyass.txt
deactivate
```

5.Run the `main.py` on All-In-LoRA
```
.\venv\Scripts\activate
python main.py
```

6. Type the following command in your browser's address bar
```
http://127.0.0.1:8000
```

## Documentation

The documentation exists in the application and can be found here.
The content of the document changes depending on the page that is currently open.

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](/example/example02.png)

## Credits

- Stable Diffusion - https://github.com/Stability-AI/stablediffusion, https://github.com/CompVis/taming-transformers
- k-diffusion - https://github.com/crowsonkb/k-diffusion.git
- ESRGAN - https://github.com/xinntao/ESRGAN
- GFPGAN - https://github.com/TencentARC/GFPGAN.git
- sd-scripts - https://github.com/kohya-ss/sd-scripts
- ultralytics - https://github.com/ultralytics/ultralytics
- rembg - https://github.com/danielgatis/rembg
- LyCORIS - https://github.com/KohakuBlueleaf/LyCORIS
- lion-pytorch - https://github.com/lucidrains/lion-pytorch
- dadaptation - https://github.com/facebookresearch/dadaptation
- prodigy - https://github.com/konstmish/prodigy

## License

MIT - [vue.js](https://github.com/vuejs/core),[fastapi](https://github.com/tiangolo/fastapi),[Stable Diffusion](https://github.com/Stability-AI/stablediffusion),[k-diffusion](https://github.com/crowsonkb/k-diffusion.git),[k-diffusion](https://github.com/crowsonkb/k-diffusion.git),[rembg](https://github.com/danielgatis/rembg),[lion-pytorch](https://github.com/lucidrains/lion-pytorch),[dadaptation](https://github.com/facebookresearch/),[prodigy](https://github.com/konstmish/prodigy)

Apache-2.0 - [ESRGAN](https://github.com/xinntao/ESRGAN),[GFPGAN](https://github.com/TencentARC/GFPGAN.git),[sd-scripts](https://github.com/kohya-ss/sd-scripts),[LyCORIS](https://github.com/KohakuBlueleaf/LyCORIS)

AGPL-3.0 - [ultralytics](https://github.com/ultralytics/ultralytics)