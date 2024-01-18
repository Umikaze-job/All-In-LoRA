from typing import Any
from modules.class_definition.json_manager.interface.savefiles_setting_manager import SaveFilesSettingJsonManager

"""
SettingLearningMethodsManager:setting.jsonのLearningMehtodのデータを管理するマネージャー
"""
class SettingLearningMethodsManager(SaveFilesSettingJsonManager):
    def __init__(self, folder_name: str) -> None:
        super().__init__(folder_name)
        self.LearningMethodsData = self.get_learning_methods_data()

    # LearningMethodsのデータを取得する
    def get_learning_methods_data(self) -> list[dict[str,Any]]:
        json_data = super().get_setting_file_json()

        return json_data["LearningMethods"]
    
    def set_learning_methods_data(self,data:list[dict[str,Any]]) -> None:
        self.LearningMethodsData = data

        self.save_learning_methods_data()

    def save_learning_methods_data(self) -> None:
        json_data = super().get_setting_file_json()

        json_data["LearningMethods"] = self.LearningMethodsData

        super().write_setting_file_json(json_data=json_data)