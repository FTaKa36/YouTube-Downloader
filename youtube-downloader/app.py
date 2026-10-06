import re
import shutil
import uuid
from pathlib import Path

import yt_dlp
from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
STATIC_DIR = BASE_DIR / "static"
DOWNLOAD_DIR.mkdir(exist_ok=True)

QUALITY_FORMATS = {
    "best": "bestvideo+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "audio": "bestaudio/best",
}

app = FastAPI(title="YouTube Downloader")


def ffmpeg_dir() -> str | None:
    exe = shutil.which("ffmpeg")
    if exe:
        return str(Path(exe).parent)

    roots = [
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages",
        Path("C:/ProgramData/chocolatey/bin"),
        Path("C:/ffmpeg/bin"),
    ]
    for root in roots:
        if not root.exists():
            continue
        for found in root.rglob("ffmpeg.exe"):
            return str(found.parent)
    return None


class InfoRequest(BaseModel):
    url: str


@app.post("/api/info")
def info(req: InfoRequest):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="Paste a YouTube URL first.")
    if not re.match(r"^https?://", url):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    opts = {"quiet": True, "no_warnings": True, "skip_download": True, "noplaylist": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=False)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read that video: {exc}")

    return {
        "title": data.get("title"),
        "uploader": data.get("uploader"),
        "duration": data.get("duration"),
        "thumbnail": data.get("thumbnail"),
        "view_count": data.get("view_count"),
    }


def cleanup(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


@app.get("/api/download")
def download(
    background: BackgroundTasks,
    url: str = Query(...),
    quality: str = Query("best"),
):
    url = url.strip()
    if not re.match(r"^https?://", url):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    if quality not in QUALITY_FORMATS:
        raise HTTPException(status_code=400, detail="Unknown quality option.")

    job_dir = DOWNLOAD_DIR / uuid.uuid4().hex[:8]
    job_dir.mkdir(parents=True, exist_ok=True)

    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "format": QUALITY_FORMATS[quality],
        "outtmpl": str(job_dir / "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "windowsfilenames": True,
    }
    if quality == "audio":
        opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ]
    ff = ffmpeg_dir()
    if ff:
        opts["ffmpeg_location"] = ff

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as exc:
        cleanup(job_dir)
        raise HTTPException(status_code=400, detail=f"Download failed: {exc}")

    files = [f for f in job_dir.iterdir() if f.is_file()]
    if not files:
        cleanup(job_dir)
        raise HTTPException(status_code=500, detail="Download produced no file.")

    result = max(files, key=lambda f: f.stat().st_size)
    background.add_task(cleanup, job_dir)
    return FileResponse(
        path=result,
        filename=result.name,
        media_type="application/octet-stream",
    )


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
