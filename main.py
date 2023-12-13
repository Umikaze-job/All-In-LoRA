from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.datastructures import Headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from modules.folder_select import Folder_Select
from modules.processing_images import Processing_Images
from modules.Make_TextFile import Make_TextFile

app = FastAPI()

class MyStatics(StaticFiles):
    def is_not_modified(self, response_headers: Header, request_headers: Headers) -> bool:
        # your own cache rules goes here...
        return False

# "assets"というディレクトリに静的ファイルが存在すると仮定
app.mount("/assets", app=StaticFiles(directory="assets"), name="assets")

# 静的コンテンツのエンドポイント
app.mount("/savefiles", app=MyStatics(directory="savefiles"), name="savefiles")

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
async def read_root(request: Request):
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
async def Folder_Select_Thumbnail(folderName: str = Form(), image: UploadFile = Form()):
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

# tagging
@app.post("/api/make-textfile/tagging/write")
async def Make_TextFile_Tagging(request:Request):
    return await Make_TextFile.Tagging(request)

@app.post("/api/make-textfile/tagging/getdata")
async def Make_TextFile_Tagging_GetData(request:Request):
    return await Make_TextFile.Tagging_GetData(request)

@app.post("/api/make-textfile/edit_tag/getdata")
async def Make_TextFile_EditTag_GetData(request:Request):
    return await Make_TextFile.EditTag_GetData(request)

@app.post("/api/make-textfile/edit_tag/write")
async def Make_TextFile_EditTag_Write(request:Request):
    return await Make_TextFile.EditTag_Write(request)

@app.post("/api/make-textfile/captioning/start")
async def Make_TextFile_Captioning_Start(request:Request):
    return await Make_TextFile.Captioning_Start(request)