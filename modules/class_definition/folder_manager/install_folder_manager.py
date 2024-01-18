from modules.folder_path import get_root_folder_path
import os
import platform
import subprocess

def get_shell_command_folder_path() -> str:
    return os.path.join(get_root_folder_path(),"shell_command")

def is_windows() -> bool:
    return platform.system() == 'Windows'

def mac_venv_command() -> list[str]:
    return [
        f"cd {get_root_folder_path()} \n",
        f"source venv/bin/activate \n"
    ]
    return "source venv/bin/activate"

def win_venv_command() -> list[str]:
    return [
        f"call cd {get_root_folder_path()} \n",
        "call .\\venv\Scripts\\activate \n"
    ]

class ShellCommandManager:
    
    @staticmethod
    def get_real_esrgan_folder() -> str:
        return os.path.join(get_root_folder_path(),'tools',"Real-ESRGAN")
    
    @staticmethod
    async def RealESRGAN_Install() -> None:
        file_path:str
        # Windowsの場合batファイルを書く
        if is_windows():
            file_path = os.path.join(get_shell_command_folder_path(),"real_esrgan_install.bat")
            with open(file_path,"w", newline='\n') as f:
                f.writelines([f"call cd {os.path.join(get_root_folder_path(),'tools')}\n",
                              "call git clone https://github.com/xinntao/Real-ESRGAN\n",
                              "call cd Real-ESRGAN\n",
                              ""])
        # それ以外の場合shファイルを書く
        else:
            file_path = os.path.join(get_shell_command_folder_path(),"real_esrgan_install.sh")
            with open(file_path,"w", newline='\n') as f:
                f.writelines([f"cd {os.path.join(get_root_folder_path(),'tools')}\n",
                              "git clone https://github.com/xinntao/Real-ESRGAN"])

        result = subprocess.run(file_path, shell=True)
        print(result)

    @staticmethod
    async def Execute_Resize_Shell(temp_file_name:str,temp_path:str,rate:int) -> int:
        file_path:str
        # 外部ファイルのrembgで拡大する
        cmd = ["python","inference_realesrgan.py",
                    "-i",temp_file_name,
                    "-o",temp_path,
                    "-n","RealESRGAN_x4plus_anime_6B",
                    "-s",str(rate)]
        cmd_line = ' '.join(cmd)
        # Windowsの場合batファイルを書く
        if is_windows():
            file_path = os.path.join(get_shell_command_folder_path(),"real_esrgan_resize.bat")
            with open(file_path,"w", newline='\n') as f:
                command_list = win_venv_command()
                command_list.extend([f"call cd {os.path.join(get_root_folder_path(),'tools','Real-ESRGAN')}\n",f"call {cmd_line}"])
                f.writelines(command_list)
        # それ以外の場合shファイルを書く
        else:
            file_path = os.path.join(get_shell_command_folder_path(),"real_esrgan_resize.sh")
            with open(file_path,"w", newline='\n') as f:
                command_list = mac_venv_command()
                command_list.extend([f"cd {os.path.join(get_root_folder_path(),'tools','Real-ESRGAN')}\n",cmd_line])
                f.writelines(command_list)

        result = subprocess.Popen(file_path, shell=True,stdout=subprocess.PIPE)
        print(result.communicate()[0])

        code = result.wait()
        return code
