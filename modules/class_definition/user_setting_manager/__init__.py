import json
import os
from typing import Any
from modules.file_util import get_root_folder_path

__all__ = ["UserSettingManager"]

class UserSettingManager:
    
    def __init__(self) -> None:
        self.file_path = os.path.join(get_root_folder_path(),"user_setting.json")

    @property
    def Sd_Model_Folder(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["sd-model-folder"]
    
    @Sd_Model_Folder.setter
    def Sd_Model_Folder(self,value) -> None:
        json_data = self.get_setting_file_json()
        json_data["sd-model-folder"] = value
        self.write_setting_file_json(json_data=json_data)

    @property
    def Lora_Folder(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["lora-folder"]
    
    @Lora_Folder.setter
    def Lora_Folder(self,value) -> None:
        json_data = self.get_setting_file_json()
        json_data["lora-folder"] = value
        self.write_setting_file_json(json_data=json_data)

    @property
    def Kohyass_Folder(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["kohyass-folder"]
    
    @Kohyass_Folder.setter
    def Kohyass_Folder(self,value) -> str:
        json_data = self.get_setting_file_json()
        json_data["kohyass-folder"] = value
        self.write_setting_file_json(json_data=json_data)

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