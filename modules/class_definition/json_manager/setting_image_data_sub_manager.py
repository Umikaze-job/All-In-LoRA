from .interface.setting_image_data_manager import SaveFilesSettingImageDataManager

"""
SaveFilesSettingImageFolderManager:setting.jsonのデータの中にあるImage_Dataのbaseの中にあるデータの管理をする
"""
class SaveFilesSettingImageFolderManager(SaveFilesSettingImageDataManager):
    def __init__(self, folder_name: str) -> None:
        subfoldername = "base"
        super().__init__(folder_name, subfoldername)

"""
SaveFilesSettingTrimmingFolderManager:setting.jsonのデータの中にあるImage_Dataのafterの中にあるデータの管理をする
"""
class SaveFilesSettingTrimmingFolderManager(SaveFilesSettingImageDataManager):
    def __init__(self, folder_name: str) -> None:
        subfoldername = "after"
        super().__init__(folder_name,subfoldername)

