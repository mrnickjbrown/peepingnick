from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import zipfile, io, os
from PIL import Image
import torch
import torchvision.transforms as transforms
from transformers import CLIPProcessor, CLIPModel
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

results_cache = []

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/upload")
async def upload_files(refs: list[UploadFile] = File(...), zipfile_upload: UploadFile = File(...)):
    global results_cache
    references = []
    for ref in refs:
        image = Image.open(io.BytesIO(await ref.read())).convert("RGB")
        references.append(image)
    
    contents = await zipfile_upload.read()
    z = zipfile.ZipFile(io.BytesIO(contents))
    candidates = []
    filenames = []
    for fname in z.namelist():
        with z.open(fname) as f:
            try:
                img = Image.open(f).convert("RGB")
                candidates.append(img)
                filenames.append(fname)
            except:
                continue
    
    # Process embeddings
    ref_embeds = model.get_image_features(processor(images=references, return_tensors="pt")["pixel_values"])
    cand_embeds = model.get_image_features(processor(images=candidates, return_tensors="pt")["pixel_values"])
    
    ref_embeds /= ref_embeds.norm(dim=-1, keepdim=True)
    cand_embeds /= cand_embeds.norm(dim=-1, keepdim=True)
    
    sims = cand_embeds @ ref_embeds.T
    best_scores, _ = sims.max(dim=1)
    
    results = []
    for fname, score in zip(filenames, best_scores):
        status = "PASS" if score.item() > 0.3 else "FAIL"
        results.append({"filename": fname, "score": round(score.item(), 3), "status": status})
    
    results_cache = results
    return {"results": results}

@app.get("/api/results/csv")
def get_csv():
    global results_cache
    if not results_cache:
        return {"error": "No results yet"}
    df = pd.DataFrame(results_cache)
    return df.to_csv(index=False)
