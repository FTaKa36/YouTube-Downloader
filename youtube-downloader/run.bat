@echo off
setlocal
set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WinGet\Links"
set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"
cd /d "%~dp0"
echo Starting YouTube Downloader at http://127.0.0.1:8000
"%PY%" -m uvicorn app:app --host 127.0.0.1 --port 8000
endlocal
