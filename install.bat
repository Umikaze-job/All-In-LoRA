call py -3.10 -m venv venv
call .\venv\Scripts\activate

call pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

call pip install -r requirements.txt
call deactivate

call cd tools
call git clone https://github.com/kohya-ss/sd-scripts.git
call cd sd-scripts

call py -3.10 -m venv venv
call .\venv\Scripts\activate

call pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118
call pip install --upgrade -r requirements.txt
call pip install xformers==0.0.20

call accelerate config default --mixed_precision fp16

call python -m pip install bitsandbytes==0.41.1 --prefer-binary --extra-index-url=https://jllllll.github.io/bitsandbytes-windows-webui

call cd ../../
call pip install -r requirements-kohyass.txt
call deactivate

pause