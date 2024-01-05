from typing import Any
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.datastructures import Headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from modules.folder_select import Folder_Select
from modules.processing_images import Processing_Images
from modules.Make_TextFile import Make_TextFile
from modules.Make_Lora import Make_Lora

from asyncio import ProactorEventLoop, set_event_loop, ProactorEventLoop, get_event_loop
from uvicorn import Config, Server

import platform

app = FastAPI()

class MyStatics(StaticFiles):
    def is_not_modified(self) -> bool:
        # your own cache rules goes here...
        return False

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

# folder-select関係
@app.post("/api/folder-select/get-folders")
async def Folder_Select_Get_Folders(request: Request):
    return await Folder_Select.Get_Folders(request)

@app.post("/api/folder-select/create")
async def Folder_Select_Create(request: Request):
    return await Folder_Select.Create(request)

@app.post("/api/folder-select/rename")
async def Folder_Select_Rename(request: Request):
    return await Folder_Select.Rename(request)

@app.post("/api/folder-select/thumbnail")
async def Folder_Select_Thumbnail(folderName: str = Form(), image: UploadFile = File()):
    return await Folder_Select.Thumbnail(folderName,image)

@app.post("/api/folder-select/delete")
async def Folder_Select_Delete(request: Request):
    return await Folder_Select.Delete(request)

# processing-images
@app.post("/api/processing-images/input-images")
async def Processing_Images_Input_Images(request:Request):
    return await Processing_Images.Input_Images(request)

@app.post("/api/processing-images/set-input-images")
async def Processing_Images_Set_Input_Images(file: UploadFile = File(...),folderName:str = Form(...)):
    print(f"folder_name:{folderName}")
    return await Processing_Images.Set_Input_Images(file,folderName)

@app.post("/api/processing-images/delete-input-images")
async def Processing_Images_Delete_Input_Images(request:Request):
    return await Processing_Images.Delete_Input_Images(request)

@app.post("/api/processing-images/output-input-images")
async def Processing_Images_Output_Input_Images(request:Request):
    return await Processing_Images.Output_Input_Images(request)

@app.post("/api/processing-images/delete-output-images")
async def Processing_Images_Delete_Output_Images(request:Request):
    return await Processing_Images.Delete_Output_Images(request)

@app.post("/api/processing-images/get-backup-images")
async def Processing_Images_Get_Backup_Images(request:Request):
    return await Processing_Images.Get_Backup_Images(request)

#trimming-setting
@app.post("/api/processing-images/get-trimming-models")
async def Processing_Images_Get_Trimming_Models(request:Request):
    return await Processing_Images.Get_Trimming_Models(request)

@app.post("/api/processing-images/start-trimming")
async def Processing_Images_Start_Trimming(request:Request):
    return await Processing_Images.Start_Trimming(request)
# tagging
@app.post("/api/make-textfile/tagging/write")
async def Make_TextFile_Tagging(request:Request):
    return await Make_TextFile.Tagging02(request)

@app.post("/api/make-textfile/tagging/clear_tagging_model")
async def Make_TextFile_Clear_Tagging_Model(request:Request):
    return await Make_TextFile.Clear_Tagging_Model(request)

@app.post("/api/make-textfile/tagging/getdata")
async def Make_TextFile_Tagging_GetData(request:Request):
    return await Make_TextFile.Tagging_GetData(request)

@app.post("/api/make-textfile/tagging/alreadytag")
async def Make_TextFile_Tagging_Already_Tag(request:Request):
    return await Make_TextFile.Already_Tag(request)

@app.post("/api/make-textfile/edit_tag/getdata")
async def Make_TextFile_EditTag_GetData(request:Request):
    return await Make_TextFile.EditTag_GetData(request)

@app.post("/api/make-textfile/edit_tag/write")
async def Make_TextFile_EditTag_Write(request:Request):
    return await Make_TextFile.EditTag_Write(request)

@app.post("/api/make-textfile/captioning/start")
async def Make_TextFile_Captioning_Start(request:Request):
    return await Make_TextFile.Captioning_Start(request)

@app.post("/api/make-textfile/captioning/write")
async def Make_TextFile_Captioning_Write(request:Request):
    return await Make_TextFile.Captioning_Write(request)

@app.post("/api/make-textfile/captioning/captiontag")
async def Make_TextFile_Caption_Tag(request:Request):
    return await Make_TextFile.Caption_Tag(request)

@app.post("/api/make-textfile/captioning/start-caption")
async def Make_TextFile_Start_Caption(request:Request):
    return await Make_TextFile.Start_Caption(request)

#make_lora
@app.post("/api/make-lora/image-items")
async def Make_Lora_Image_Items(request:Request):
    return await Make_Lora.Image_Items(request)

@app.post("/api/make-lora/press-start-lora")
async def Make_Lora_Press_Start_Lora(request:Request):
    return await Make_Lora.Press_Make_Command(request)

@app.post("/api/make-lora/save-data")
async def Make_Lora_Save_Data(request:Request):
    return await Make_Lora.Save_Data(request)

@app.post("/api/make-lora/sd-model")
async def Make_Lora_Sd_Model(request:Request):
    return await Make_Lora.Sd_Model(request)

# Test用のパス
@app.post('/test/processing-images/delete-character_trimming_folder-images')
async def delete_character_trimming_folder_file_Test(request:Request):
    return await Processing_Images.delete_character_trimming_folder_file_Test(request)

@app.post("/test/make-lora/move-lora-file")
async def Make_Lora_Test_Move_Files(request:Request):
    return await Make_Lora.test_moveLoRa(request)

if __name__ == "__main__" and platform.uname().system == "Windows":
    #Windowsのみこのコマンドがないとsubprocessが使えない
    set_event_loop(ProactorEventLoop())
    server = Server(config=Config(app=app))
    get_event_loop().run_until_complete(server.serve())