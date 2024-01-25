import datetime
from modules.class_definition.json_manager.interface.savefiles_setting_manager import SaveFilesSettingJsonManager
from modules.class_definition.user_setting_manager import UserSettingManager
"""
SaveFilesSettingCreateManager:setting.jsonを作るためだけのマネージャー
"""
class SaveFilesSettingCreateManager(SaveFilesSettingJsonManager):
    def __init__(self, folder_id: str,folder_name:str) -> None:
        self.folder_name = folder_name
        super().__init__(folder_id)
    def create_setting_file(self) -> None:
        now = datetime.datetime.now()
        # [年]_[月]_[日]_[時間] 形式の文字列を生成
        date = now.strftime("%Y_%m_%d_%H%M%S")
        user_manager = UserSettingManager()
        # データ内容
        settings_data = {
            "date":{
                "Folder creation date": date
            },
            "folderData":{
                "id":self.folder_id,
                "name":self.folder_name
            },
            # "base","after"の各要素の中身:{"file_name":"","tags":"","caption":"","method":""}
            "Image_Data":{"base":[],"after":[]},
            "LearningMethods":[],
            "loraData":user_manager.Init_LoraData,
            "version":"1.0.3"
        }

        self.write_setting_file_json(settings_data)
        
