import json
import os
from typing import Any
from modules.file_util import get_root_folder_path

__all__ = ["UserSettingManager"]

class UserSettingManager:
    
    def __init__(self) -> None:
        self.file_path = os.path.join(get_root_folder_path(),"user_setting.json")
        self.data = self.get_setting_file_json()

    @property
    def Lora_Folder(self) -> str:
        return self.data["lora-folder"]
    
    @property
    def Kohyass_Folder(self) -> str:
        return self.data["kohyass-folder"]

    # setting.jsonを読み込み
    def get_setting_file_json(self) -> Any:
        file_path = os.path.join(self.file_path)
        with open(file_path,"r") as f:
            return json.load(f)

    # setting.jsonに書き込み
    def write_setting_file_json(self,json_data:Any) -> None:
        file_path = os.path.join(self.file_path)
        with open(file_path,"w") as f:
            f.write(json.dumps(json_data, indent=2))