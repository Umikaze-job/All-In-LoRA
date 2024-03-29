from modules.folder_path import get_savefiles
import os
import json
from typing import Any
"""
SaveFilesSettingJsonManager:savefilesの中にあるフォルダごとに存在するsetting.jsonの管理をする
"""

#region setting.jsonの中身
"""
setting.jsonの中身
"date":{
    "Folder creation date": <フォルダを初めて作成した日>
},
"folderData":{
    "id":"<フォルダID>",
    "name":"<フォルダ名>"
}
"Image_Data":{"base":[
    {"file_name":"<ファイル名>","tags":"<タグ>","caption":"<キャプション>","method":"<メソッド名>"}
],"after":[
    {"file_name":"","tags":"","caption":"","method":""}
]},
"LearningMethods":[
    {
        name:string,
        setting:{
            batchSize: number,
            bucketNoUpscale: boolean,
            bucketResoSteps: number,
            enableBucket: boolean,
            maxBucketReso:number,
            minBucketReso:number,
            resolution:number,
            colorAug: boolean,
            flipAug: boolean,
            keepTokens:number,
            numRepeats:number,
            shuffleCaption: boolean,
        }
    },
    {
        name:string,
        ...
    },...
],
"loraData":{
    MainSetting:{
        outputFileName:string, 
        commentLine:string,
        epochs:number, 
        sdType:string, 
        useModel:string,
        loraType:string,
        optimizer:string,
        mixed_precision:string,
    },
    learningSetting:{
        networkDim:number,
        networkAlpha:number,
        learningRate:number,
        textEncoderLr:number,
        unetLr:number,
        schduler:string,
        schedulerOption:number,
        lrWarmupSteps:number
    },
    netArgs:{
        convDim:number,
        convAlpha:number,
        dropout:number,
    },
    performance:{
        cpuThreads:number,
        workers:number,
    },
    sampleImage:{
        positivePrompt:string,
        negativePrompt:string,
        width:number,
        height:number,
        steps:number
    }
}

"""
#endregion

class SaveFilesSettingJsonManager:
    def __init__(self,folder_id:str) -> None:
        self.folder_id = folder_id

    @property
    def now_save_file(self):
        return os.path.join(get_savefiles(),self.folder_id)

    # setting.jsonを読み込み
    def get_setting_file_json(self) -> Any:
        file_path = os.path.join(self.now_save_file,"setting.json")
        with open(file_path,"r") as f:
            return json.load(f)

    # setting.jsonに書き込み
    def write_setting_file_json(self,json_data:Any) -> None:
        file_path = os.path.join(self.now_save_file,"setting.json")
        with open(file_path,"w") as f:
            f.write(json.dumps(json_data, indent=2))

    # こっちを使いたい
    @property
    def setting_file_json(self) -> dict[str,Any]:
        file_path = os.path.join(self.now_save_file,"setting.json")
        with open(file_path,"r") as f:
            return json.load(f)
        
    @setting_file_json.setter
    def setting_file_json(self,json_data:Any) -> None:
        file_path = os.path.join(self.now_save_file,"setting.json")
        with open(file_path,"w") as f:
            f.write(json.dumps(json_data, indent=2))

        

