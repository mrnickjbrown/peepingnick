from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
import shutil
from pathlib import Path
import os

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.content_type and file.content_type.startswith("image/"):
        return {"message": f"✅ Image {file.filename} uploaded successfully!"}
    return JSONResponse(status_code=400, content={"error": "❌ File is not an image."})

# Serve built frontend
STATIC_DIR = "static"
if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

@app.get("/favicon.ico")
def favicon():
    ico_path = Path(STATIC_DIR) / "favicon.ico"
    if ico_path.exists():
        return FileResponse(str(ico_path))
    return Response(status_code=204)
