import os
import glob
from PIL import Image
from ...folder_path import get_savefiles
import json
from ...gpu_modules.tagging import do_tagging

"""
FolderManagerParent:画像フォルダの処理をするクラスの親クラス
"""
class FolderManagerParent:
    def __init__(self,folder_name,folder_path,url_path):
        self.folder_path = folder_path
        self.url_path = url_path
        self.folder_name = folder_name
        self.Image_Data = None

        self.image_extentions = ['jpg', 'jpeg', 'png', 'gif',"webp"]

    # フォルダ内に存在するすべての画像ファイルを取得する
    def get_all_url_paths(self):
        all_files_path = []
        list(map(lambda ext:all_files_path.extend(glob.glob(os.path.join(self.folder_path,f'*.{ext}'))),self.image_extentions))
        all_files_name = list(map(lambda path:os.path.basename(path),all_files_path))

        return list(map(lambda name:os.path.join(self.url_path,name),all_files_name))
    
    # 画像をフォルダに追加する
    async def Input_Image(self):
        pass

    # 画像ファイルを消去する
    def delete_file(self,file_name):
        os.remove(os.path.join(self.folder_path,file_name))

    # setting.jsonのデータを取得
    def get_setting_json(self):
        with open(os.path.join(get_savefiles(),self.folder_name,"setting.json"),"r") as f:
            return json.load(f)
        
    def write_setting_json(self,json_data):
        file_path = os.path.join(get_savefiles(),self.folder_name,"setting.json")
        with open(file_path,"w") as f:
            f.write(json.dumps(json_data, indent=2))
        
    # 指定した名前の画像フォルダのデータの初期データを作成する(すでに指定した名前のデータが存在する場合は何もしない)
    def image_data_init(self,file_name):
        if any(file_name == item.get('file_name') for item in self.Image_Data) == False:
            self.Image_Data.append({"file_name":file_name})
        
    # タグを生成して変更する
    async def tags_generate(self,file_name:str,Tagging_Model):
        if self.Image_Data == None:
            return
        
        file_path = os.path.join(self.folder_path,file_name)
        image = Image.open(file_path)
        # json_data["taggingData"]["---"]["file_name"]の値がfile_nameと同じ名前の連想配列があるとき
        self.image_data_init(file_name)
        rensou = list(filter(lambda item:item.get('file_name') == file_name,self.Image_Data))
        rensou[0]["tags"] = await do_tagging(image,Tagging_Model) #タグを指定

    # タグを消去する
    def tags_delete(self,file_name:str):
        if self.Image_Data == None:
            return
        
        self.image_data_init(file_name)
        rensou = [item for item in self.Image_Data if item.get('file_name') == file_name and item.get('tags') != None]
        if len(rensou) == 0:
            return
        rensou[0]["tags"] = [""]
        
    
