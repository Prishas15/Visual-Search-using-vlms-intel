from fastapi import FastAPI, UploadFile, File, HTTPException
import torch
import clip
from PIL import Image, UnidentifiedImageError
import io
import faiss
import numpy as np
import os
import time

app = FastAPI()
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device)

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

database = []
faiss_index = faiss.IndexIDMap(faiss.IndexFlatL2(512))

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="Invalid image file format.")

        image_input = preprocess(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            image_features = model.encode_image(image_input)
        image_features = image_features.cpu().numpy().astype(np.float32).reshape(1, -1)
        
        timestamp = int(time.time())
        image_filename = f"{timestamp}_{file.filename}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as img_file:
            img_file.write(contents)
        
        index_id = len(database)
        database.append({"image": image_path, "embedding": image_features})
        faiss_index.add_with_ids(image_features, np.array([index_id], dtype=np.int64))
        
        return {"message": "Image uploaded successfully", "image_path": image_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/search/")
def search_image(query: str):
    if not database:
        raise HTTPException(status_code=404, detail="No images in database")
    if faiss_index.ntotal == 0:
        raise HTTPException(status_code=404, detail="FAISS index is empty. Upload images first.")
    
    try:
        text_input = clip.tokenize([query]).to(device)
        with torch.no_grad():
            text_features = model.encode_text(text_input)
        text_features = text_features.cpu().numpy().astype(np.float32)
        
        _, indices = faiss_index.search(text_features, k=min(5, len(database)))
        results = [database[i]["image"] for i in indices[0] if i >= 0]
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
