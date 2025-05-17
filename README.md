# 🎬 UCClip

**UCClip** is a web app that generates highlight videos for UC Davis soccer matches. Users can upload footage and overlay professionally styled captions using custom templates. Built with a React + Tailwind frontend and a FastAPI backend.

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

---
### 📦 **Frontend Setup**

```bash
cd backend
pip install -r requirements.txt
pip install python-multipart
python3 -m venv venv
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


