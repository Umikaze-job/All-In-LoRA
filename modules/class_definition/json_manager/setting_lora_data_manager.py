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

        return json_data["loraData"]
    
    def set_lora_data(self,data:list[dict[str,Any]]) -> None:
        self.LoraData = data

        self.save_lora_data()

    def save_lora_data(self):
        json_data = super().get_setting_file_json()

        json_data["loraData"] = self.LoraData

        super().write_setting_file_json(json_data=json_data)