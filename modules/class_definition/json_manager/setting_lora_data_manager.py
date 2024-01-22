from typing import Any
from modules.class_definition.json_manager.interface.savefiles_setting_manager import SaveFilesSettingJsonManager

"""
SettingLoraDataManager:setting.jsonのLoraDataのデータを管理するマネージャー
"""
class SettingLoraDataManager(SaveFilesSettingJsonManager):
    def __init__(self, folder_name: str) -> None:
        super().__init__(folder_name)
        self.LoraData = self.get_lora_data()

    # LearningMethodsのデータを取得する
    def get_lora_data(self) -> dict[str,Any]:
        json_data = super().get_setting_file_json()

        # v1.0.0のデータを使用している人用
        if json_data["loraData"]["performance"].get("cupThread") != None:
            json_data["loraData"]["performance"]["cpuThreads"] = json_data["loraData"]["performance"]["cupThread"]

        return json_data["loraData"]
    
    @property
    def triggerWord(self) -> str:
        return self.LoraData["sampleImage"]["triggerWord"]
    
    @triggerWord.setter
    def triggerWord(self,word:str) -> None:
        self.LoraData["sampleImage"]["triggerWord"] = word
        self.save_lora_data()
    
    def set_lora_data(self,data:dict[str,Any]) -> None:
        self.LoraData = data

        self.save_lora_data()

    def save_lora_data(self) -> None:
        json_data = super().get_setting_file_json()

        # v1.0.0のデータを使用している人用
        if json_data["loraData"]["performance"].get("cupThread") != None:
            json_data["loraData"]["performance"]["cpuThreads"] = json_data["loraData"]["performance"]["cupThread"]

        json_data["loraData"] = self.LoraData

        super().write_setting_file_json(json_data=json_data)