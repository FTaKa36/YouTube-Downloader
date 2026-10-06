# 🎥 YouTube Downloader (Local Web App)

A lightweight, locally-hosted web application that allows you to download videos and audio from YouTube directly to your computer. Since the app runs locally on your machine, no external web hosting is required—you just need an active internet connection to download media!

---

## 📂 Project Structure

Based on the local directory setup, the project consists of the following structure:

```text
├── downloads/             # Default directory for downloaded media files
├── static/                # Static assets for the web interface
├── YouTube Downloader/    # Core application folder
├── app.py                 # Main Python application entry point
├── requirements.txt       # Python dependency list
├── run.bat                # Batch file to start the local server
└── YouTube Downloader.url # Internet Shortcut to open the web interface
```

---

## 🚀 Getting Started

Follow these simple steps to run the application on your local machine:

### 1. Prerequisites

Make sure you have [Python](https://www.python.org/) installed on your Windows system.

### 2. Initial Setup (First Time Only)

Before launching for the first time, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

---

## 💻 How to Use

1. **Start the Local Server:**
   Double-click the **`run.bat`** file. This will initialize the backend server locally on your machine.
   
2. **Open the App:**
   Double-click the **`YouTube Downloader`** (Internet Shortcut) file. This will automatically open the local web interface in your default browser.

3. **Download Media:**
   - Ensure your **internet connection is active**.
   - Paste the YouTube URL into the web interface.
   - Choose whether to download as video or audio (MP3/MP4) and start downloading!

---

## 📥 Where are Downloads Saved?

The download destination depends on your web browser configuration:

- **Automatic Download Path (Default):** If automatic downloads are enabled in your browser settings, files will be saved directly to your default browser downloads folder (or the project's `./downloads/` directory depending on your configuration).
- **Manual Download Path:** If you have set your browser to prompt for a download location each time, a file manager window will pop up allowing you to manually choose where to save the downloaded video/audio file.

---

## ⚡ Prerequisites & Requirements

- **Operating System:** Windows (for executing `.bat` files directly).
- **Internet Connection:** Active connection required during downloads.
- **Python 3.x**

---

## 📜 License

This project is open-source and intended for personal educational use. Please observe YouTube's Terms of Service regarding media downloading.