import json
import os
from typing import Any
from modules.file_util import get_root_folder_path

__all__ = ["UserSettingManager"]

def merge_dicts_recursive(dict_a:Any, dict_b:Any) -> Any:
    for key, value_b in dict_b.items():
        if key not in dict_a:
            # キーが存在しない場合、そのまま追加
            dict_a[key] = value_b
        else:
            # キーが存在する場合、辞書なら再帰的に処理、それ以外は上書きしない
            if isinstance(value_b, dict) and isinstance(dict_a[key], dict):
                merge_dicts_recursive(dict_a[key], value_b)
            elif dict_a[key] != value_b:
                # 辞書でない場合は上書きしない
                print(f"Key: {key} already exists with a different value. Skipped.")

class UserSettingManager:
    
    def __init__(self) -> None:
        self.file_path = os.path.join(get_root_folder_path(),"user_setting.json")

    @property
    def Sd_Model_Folder(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["sd-model-folder"]
    
    @Sd_Model_Folder.setter
    def Sd_Model_Folder(self,value:str) -> None:
        json_data = self.get_setting_file_json()
        json_data["sd-model-folder"] = value
        self.write_setting_file_json(json_data=json_data)

    @property
    def Lora_Folder(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["lora-folder"]
    
    @Lora_Folder.setter
    def Lora_Folder(self,value:str) -> None:
        json_data = self.get_setting_file_json()
        json_data["lora-folder"] = value
        self.write_setting_file_json(json_data=json_data)

    @property
    def Kohyass_Folder(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["kohyass-folder"]
    
    @Kohyass_Folder.setter
    def Kohyass_Folder(self,value:str) -> None:
        json_data = self.get_setting_file_json()
        json_data["kohyass-folder"] = value
        self.write_setting_file_json(json_data=json_data)

    @property
    def Select_Folder_Name(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["select-folder-name"]
    
    @Select_Folder_Name.setter
    def Select_Folder_Name(self,value:str) -> None:
        json_data = self.get_setting_file_json()
        json_data["select-folder-name"] = value
        self.write_setting_file_json(json_data=json_data)

    @property
    def User_Language(self) -> str:
        json_data = self.get_setting_file_json()
        return json_data["language"]
    
    @User_Language.setter
    def User_Language(self,value:str) -> None:
        json_data = self.get_setting_file_json()
        json_data["language"] = value
        self.write_setting_file_json(json_data=json_data)

    @property
    def Init_LoraData(self) -> dict[str,Any]:
        json_data = self.get_setting_file_json()
        return json_data["loraData"]
    
    @Init_LoraData.setter
    def Init_LoraData(self,value:dict[str,Any]) -> None:
        json_data = self.get_setting_file_json()
        json_data["loraData"] = value
        self.write_setting_file_json(json_data=json_data)

    # jsonファイルのリフレッシュをする
    # ファイルがなかった時は作成して、項目が足りない時は追加する
    def setting_file_refresh(self) -> None:
        json_data:dict[str,Any]
        # jsonファイルが存在しないとき
        if os.path.exists(self.file_path) == False:
            json_data = self.init_data()
            with open(self.file_path,"w") as file:
                file.write(json.dumps(json_data, indent=2))
        else:
            with open(self.file_path,"r") as file:
                json_data = json.loads(file.read())
            # 不足しているデータは不足分だけ追加する。
            # 連想配列Aに不足しているデータを連想配列Bから追加
            merge_dicts_recursive(json_data,self.init_data())

            with open(self.file_path,"w") as file:
                file.write(json.dumps(json_data, indent=2))


    # 初期のデータ
    def init_data(self) -> dict[str,Any]:
        return {
            "sd-model-folder": os.path.join(get_root_folder_path(),"models","sd_models"),
            "kohyass-folder": os.path.join(get_root_folder_path(),"tools","sd-scripts"),
            "lora-folder": os.path.join(get_root_folder_path(),"outputs"),
            "select-folder-name": "",
            "language": "en",
            "loraData": {
                "MainSetting": {
                    "outputFileName": "",
                    "commentLine": "",
                    "epochs": 4,
                    "sdType": "sd1.5",
                    "useModel": "",
                    "loraType": "LoCon",
                    "optimizer": "DAdaptAdam",
                    "mixed_precision": ""
                },
                "learningSetting": {
                    "networkDim": 64,
                    "networkAlpha": 1,
                    "learningRate": 1,
                    "textEncoderLr": 1,
                    "unetLr": 1,
                    "schduler": "cosine",
                    "schedulerOption": 1,
                    "lrWarmupSteps": 10
                },
                "netArgs": {
                    "convDim": 64,
                    "convAlpha": 1,
                    "dropout": 0.1
                },
                "performance": {
                    "cupThread": 8,
                    "workers": 12
                },
                "sampleImage": {
                    "triggerWord": "",
                    "positivePrompt": "masterpiece, best quality, 1girl, looking at viewer, white background",
                    "negativePrompt": "low quality, worst quality, bad anatomy,bad composition, poor, low effort",
                    "width": 600,
                    "height": 900,
                    "steps": 20
                }
            }
        }

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