import os, sys
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, '../yt-downloader'))
from downloader import downloadVideo 

video_hash = {}

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 配置靜態文件路由
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# download in the backend
@app.get("/download")
async def download(url: str, type: str): 
    # data = await request.json()
    # url = data.get("url")
    # type = data.get("type")
  
    # 以固定的path去實作 

    try:
        name, path, originalTitle = downloadVideo(url, type, "./videos/")
        video_hash[name] = originalTitle
    except Exception as error :
        print(error)
        return {"message": "Video download failed"}
    
    return {"message": "Video downloaded successfully",
            "name":{name}
            }

@app.get("/video/{video_id}/name")
async def get_video_name(video_id: str):
    if video_id not in video_hash:
        return {"message": "Video not found"}
    return {"name": video_hash.get(video_id),"message":"Success"}

# 上傳給使用者 
@app.get("/video/{video_id}")
async def read_item(video_id: str):
    video_path = f"./videos/{video_id}"
    if not os.path.exists(video_path):
        print(video_path)
        return {"message": "Video not found"}
    
    content_type = get_content_type(video_id)
    headers = {
        "Content-Type": content_type,
        "Content-Disposition": f"attachment; filename={video_id}"
    }
    return StreamingResponse(file_iterator(video_path), headers=headers) # 以streaming的方式去實作

# 取得檔案的類型
def get_content_type(video_id: str) -> str:
    if video_id.endswith(".mp4"):
        return "video/mp4"
    elif video_id.endswith(".wmv"):
        return "video/x-ms-wmv"
    elif video_id.endswith(".mp3"):
        return "audio/mpeg"
    else:
        return "application/octet-stream"

# 以streaming的方式去實作
def file_iterator(file_path: str, chunk_size: int = 8192):
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk: 
                break
            yield chunk