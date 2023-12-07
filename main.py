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
    "http://localhost:64383",
    "http://localhost:5173",
    "http://localhost",
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
async def Processing_Images_Delete_Input_Images(request:Request):
    return await Processing_Images.Delete_Input_Images(request)
