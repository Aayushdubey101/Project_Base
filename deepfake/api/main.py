from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.predict import predict_image
from app.preprocess import load_image
from app.utils import build_upload_path, ensure_directory, is_allowed_file

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = ensure_directory(BASE_DIR / "uploads")

app = FastAPI(title="Deepfake Detection API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict:
    return {"message": "Deepfake Detection API is running"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict:
    if not file.filename or not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    image_bytes = await file.read()
    upload_path = build_upload_path(UPLOADS_DIR, file.filename)
    upload_path.write_bytes(image_bytes)

    image = load_image(image_bytes)
    result = predict_image(image)

    return {"filename": upload_path.name, **result}
