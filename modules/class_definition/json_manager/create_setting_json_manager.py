import datetime
from modules.class_definition.json_manager.interface.savefiles_setting_manager import SaveFilesSettingJsonManager

class SaveFilesSettingCreateManager(SaveFilesSettingJsonManager):
    def create_setting_file(self) -> None:
        now = datetime.datetime.now()
        # [年]_[月]_[日]_[時間] 形式の文字列を生成
        date = now.strftime("%Y_%m_%d_%H%M%S")
        # データ内容
        settings_data = {
            "date":{
                "Folder creation date": date
            },
            # "base","after"の各要素の中身:{"file_name":"","tags":"","caption":"","method":""}
            "Image_Data":{"base":[],"after":[]},
            "LearningMethods":[],
            "loraData":{}
        }

        self.write_setting_file_json(settings_data)