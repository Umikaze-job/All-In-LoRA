py -3.10 -m venv venv
.\venv\Scripts\activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

pip install -r requirements.txt
deactivate

cd tools
git clone https://github.com/kohya-ss/sd-scripts.git
cd sd-scripts

py -3.10 -m venv venv
.\venv\Scripts\activate

pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118
pip install --upgrade -r requirements.txt
pip install xformers==0.0.20

accelerate config default --mixed_precision fp16

python -m pip install bitsandbytes==0.41.1 --prefer-binary --extra-index-url=https://jllllll.github.io/bitsandbytes-windows-webui

cd ../../
pip install -r requirements-kohyass.txt
deactivate

pause