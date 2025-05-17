# 🎬 UCClip

**UCClip** is a web app that generates highlight videos for UC Davis soccer matches. Users can upload footage and overlay professionally styled, AI-generated captions using custom templates. Built with a React + Tailwind frontend and a FastAPI backend.

---

## 🛠️ Tech Stack

- **Frontend:** React, Tailwind CSS  
- **Backend:** FastAPI, Python  
- **Video Processing:** OpenCV, MoviePy  
- **Other:** python-multipart for file handling

---

## 🚀 Getting Started

Follow the steps below to set up both the backend and frontend environments.

---

### 📦 Backend Setup

```bash
cd backend
pip install -r requirements.txt
pip install python-multipart
python3 -m venv venv
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
> ⚠️ **Important:**  
> In `backend/app/utils/video_service.py`, replace the placeholder in `Api_Key = "..."` with your actual [OpenAI API key](https://platform.openai.com/account/api-keys).

---
### 📦 **Frontend Setup**

```bash
npm install
npm run start
```
---

## 🎯 Features

- Upload full match footage
- Select visual templates
- Generate short highlight clips with styled captions
- Download or share outputs

---

## 📸 Templates

Current version supports 4 caption overlay templates (more to come).  
Choose a style during upload to personalize your video.

---

