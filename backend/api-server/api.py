import os, sys, socket
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, '../yt-downloader'))
from downloader import downloadVideo

video_hash = {}

app = FastAPI()
env_port = os.getenv("PORT", 3000)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://youtubedownload-8c304a4e20ec.herokuapp.com:{env_port}"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# test
@app.get("/")
def hello_world():
    return {"message": "Hello World"}

# download in the backend
@app.get("/download")
async def download(url: str, type: str, id: str): 
    # data = await request.json()
    # url = data.get("url")
    # type = data.get("type")
  
    # 以固定的path去實作 
     
    try:
        name, path, originalTitle = downloadVideo(url, type, id, "./videos/")
        video_hash[name] = originalTitle
    except Exception as e : 
        print(e)
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