from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
import uvicorn

app = FastAPI()

# Enable CORS for your frontend
origins = [
    "https://vidfetch-frontend-hw19ahfgj-merazs-projects-afacd4c2.vercel.app/",  # replace with your frontend URL
                       # optional for local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],   # allow Content-Type
)

class VideoRequest(BaseModel):
    url: str

@app.post("/api/getvideo")
async def get_video(req: VideoRequest):
    if not req.url:
        return {"error": "No URL provided"}

    try:
        # Run yt-dlp to get video info in JSON
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-j", req.url],
            capture_output=True,
            text=True,
            check=True
        )
        info = json.loads(result.stdout)
        download_url = info.get("url")
        if not download_url:
            return {"error": "Could not retrieve video URL"}
        return {"downloadUrl": download_url}

    except subprocess.CalledProcessError as e:
        return {"error": e.stderr or str(e)}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "✅ VidFetch Python backend is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
