from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from modules.folder_select import Folder_Select

app = FastAPI()

# "assets"というディレクトリに静的ファイルが存在すると仮定
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

origins = [
    "http://localhost:5173",
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

@app.post("/api/folder-select/create")
async def Folder_Select_Create(request: Request):
    return await Folder_Select.Folder_Select_Create(request)