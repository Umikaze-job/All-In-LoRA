from typing import Any
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.datastructures import Headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from modules import *

from asyncio import ProactorEventLoop, set_event_loop, ProactorEventLoop, get_event_loop
from uvicorn import Config, Server

import platform

app = FastAPI()

# "assets"というディレクトリに静的ファイルが存在すると仮定
app.mount("/assets", app=StaticFiles(directory="assets"), name="assets")

# 静的コンテンツのエンドポイント
app.mount("/savefiles", app=StaticFiles(directory="savefiles"), name="savefiles")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
@app.get("/{wildcard}", response_class=HTMLResponse)
async def read_root(request: Request) -> Any:
    return templates.TemplateResponse("index.html", {"request": request})

# region topbar-setting
@app.post("/api/topbar/set-language")
async def Set_Language(request:Request) -> Any:
    return await TopbarManager.Set_Language(request=request)
# endregion

# region Welcome-Page
@app.post("/api/welcome-page/sd-models-folder")
async def Welcome_Page_Sd_Models_Folder(request:Request) -> Any:
    return await Welcome_Page.Sd_Models_Folder(request)

@app.post("/api/welcome-page/kohyass-folder")
async def Welcome_Page_Kohyass_Folder(request:Request) -> Any:
    return await Welcome_Page.Kohyass_Folder(request)

@app.post("/api/welcome-page/lora-folder")
async def Welcome_Page_Lora_Folder(request:Request) -> Any:
    return await Welcome_Page.Lora_Folder(request)

@app.post("/api/welcome-page/init-setting")
async def Welcome_Page_All_Folder_Path() -> Any:
    return await Welcome_Page.Init_Setting()

@app.post("/api/welcome-page/real-esrgan-install")
async def Welcome_Page_Real_ESRGAN_Install(request:Request) -> Any:
    return await Welcome_Page.RealESRGAN_Install(request)

@app.post("/api/welcome-page/setting-mixed-precision")
async def Welcome_Page_Setting_Mixed_Precision(request:Request) -> Any:
    return await Welcome_Page.Setting_Mixed_Precision(request)

@app.post("/api/welcome-page/check-cuda-cudnn")
async def Welcome_Page_Check_Cuda_Cudnn() -> Any:
    return await Welcome_Page.Check_Cuda_Cudnn()

#endregion
# region folder-select関係
@app.post("/api/folder-select/get-folders")
async def Folder_Select_Get_Folders(request: Request) -> Any:
    return await Folder_Select.Get_Folders(request)

@app.post("/api/folder-select/create")
async def Folder_Select_Create(request: Request) -> Any:
    return await Folder_Select.Create(request)

@app.post("/api/folder-select/rename")
async def Folder_Select_Rename(request: Request) -> Any:
    return await Folder_Select.Rename(request)

@app.post("/api/folder-select/thumbnail")
async def Folder_Select_Thumbnail(folderName: str = Form(), image: UploadFile = File()) -> Any:
    return await Folder_Select.Thumbnail(folderName,image)

@app.post("/api/folder-select/delete")
async def Folder_Select_Delete(request: Request) -> Any:
    return await Folder_Select.Delete(request)

@app.post("/api/folder-select/set-folder-name")
async def Set_Folder_Name(request: Request) -> Any:
    return await Folder_Select.Set_Folder_Name(request)


#endregion

# region processing-images
# processing-images
@app.post("/api/processing-images/input-images")
async def Processing_Images_Input_Images(request:Request) -> Any:
    return await Processing_Images.Input_Images(request)

@app.post("/api/processing-images/set-input-images")
async def Processing_Images_Set_Input_Images(file: UploadFile = File(...),folderName:str = Form(...)) -> Any:
    print(f"folder_name:{folderName}")
    return await Processing_Images.Set_Input_Images(file,folderName)

@app.post("/api/processing-images/delete-input-images")
async def Processing_Images_Delete_Input_Images(request:Request) -> Any:
    return await Processing_Images.Delete_Input_Images(request)

@app.post("/api/processing-images/output-input-images")
async def Processing_Images_Output_Input_Images(request:Request) -> Any:
    return await Processing_Images.Output_Input_Images(request)

@app.post("/api/processing-images/delete-output-images")
async def Processing_Images_Delete_Output_Images(request:Request) -> Any:
    return await Processing_Images.Delete_Output_Images(request)

@app.post("/api/processing-images/get-backup-images")
async def Processing_Images_Get_Backup_Images(request:Request) -> Any:
    return await Processing_Images.Get_Backup_Images(request)

#trimming-setting
@app.post("/api/processing-images/get-trimming-models")
async def Processing_Images_Get_Trimming_Models(request:Request) -> Any:
    return await Processing_Images.Get_Trimming_Models(request)

@app.post("/api/processing-images/start-trimming")
async def Processing_Images_Start_Trimming(request:Request) -> Any:
    return await Processing_Images.Start_Trimming(request)
# endregion
# region Make-Textfile
# tagging
@app.post("/api/make-textfile/tagging/write")
async def Make_TextFile_Tagging(request:Request) -> Any:
    return await Make_TextFile.Tagging02(request)

@app.post("/api/make-textfile/tagging/clear_tagging_model")
async def Make_TextFile_Clear_Tagging_Model(request:Request) -> Any:
    return await Make_TextFile.Clear_Tagging_Model(request)

@app.post("/api/make-textfile/tagging/getdata")
async def Make_TextFile_Tagging_GetData(request:Request) -> Any:
    return await Make_TextFile.Tagging_GetData(request)

@app.post("/api/make-textfile/tagging/alreadytag")
async def Make_TextFile_Tagging_Already_Tag(request:Request) -> Any:
    return await Make_TextFile.Already_Tag(request)

@app.post("/api/make-textfile/tagging/set-trigger-word")
async def Make_TextFile_Tagging_Set_Trigger_Word(request:Request) -> Any:
    return await Make_TextFile.Set_Trigger_Word(request)

@app.post("/api/make-textfile/edit_tag/getdata")
async def Make_TextFile_EditTag_GetData(request:Request) -> Any:
    return await Make_TextFile.EditTag_GetData(request)

@app.post("/api/make-textfile/edit_tag/write")
async def Make_TextFile_EditTag_Write(request:Request) -> Any:
    return await Make_TextFile.EditTag_Write(request)

@app.post("/api/make-textfile/captioning/start")
async def Make_TextFile_Captioning_Start(request:Request) -> Any:
    return await Make_TextFile.Captioning_Start(request)

@app.post("/api/make-textfile/captioning/write")
async def Make_TextFile_Captioning_Write(request:Request) -> Any:
    return await Make_TextFile.Captioning_Write(request)

@app.post("/api/make-textfile/captioning/captiontag")
async def Make_TextFile_Caption_Tag(request:Request) -> Any:
    return await Make_TextFile.Caption_Tag(request)

@app.post("/api/make-textfile/captioning/start-caption")
async def Make_TextFile_Start_Caption(request:Request) -> Any:
    return await Make_TextFile.Start_Caption(request)
#endregion
# region make_lora
@app.post("/api/make-lora/image-items")
async def Make_Lora_Image_Items(request:Request) -> Any:
    return await Make_Lora.Image_Items(request)

@app.post("/api/make-lora/press-start-lora")
async def Make_Lora_Press_Start_Lora(request:Request) -> Any:
    return await Make_Lora.Press_Make_Command(request)

@app.post("/api/make-lora/save-data")
async def Make_Lora_Save_Data(request:Request) -> Any:
    return await Make_Lora.Save_Data(request)

@app.post("/api/make-lora/sd-model")
async def Make_Lora_Sd_Model(request:Request) -> Any:
    return await Make_Lora.Sd_Model(request)
#endregion

# region Test用のパス
@app.post('/test/processing-images/delete-character_trimming_folder-images')
async def delete_character_trimming_folder_file_Test(request:Request) -> Any:
    return await Processing_Images.delete_character_trimming_folder_file_Test(request)

@app.post("/test/make-lora/move-lora-file")
async def Make_Lora_Test_Move_Files(request:Request) -> Any:
    return await Make_Lora.test_moveLoRa(request)

if __name__ == "__main__" and platform.uname().system == "Windows":
    #Windowsのみこのコマンドがないとsubprocessが使えない
    set_event_loop(ProactorEventLoop())
    server = Server(config=Config(app=app))
    get_event_loop().run_until_complete(server.serve())

# endregion