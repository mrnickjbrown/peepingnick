from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path

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

    # Simple image validation
    if file.content_type.startswith("image/"):
        return {"message": f"✅ Image {file.filename} uploaded successfully!"}
    else:
        return JSONResponse(
            status_code=400,
            content={"error": "❌ File is not an image."}
        )
