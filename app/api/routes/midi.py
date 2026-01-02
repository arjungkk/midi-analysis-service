from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime

from app.db.mongodb import db
from app.services.storage_service import StorageService
from app.utils.hashing import compute_file_hash

router = APIRouter(prefix="/midi", tags=["midi"])

storage = StorageService()


@router.post("")
async def upload_midi(file: UploadFile = File(...)):
    if not file.filename.endswith(".mid"):
        raise HTTPException(status_code=400, detail="Only MIDI files are supported")

    content = await file.read()
    file_hash = compute_file_hash(content)

    file_path = storage.save_file(file.filename, content)

    midi_doc = {
        "filename": file.filename,
        "file_hash": file_hash,
        "storage_path": file_path,
        "created_at": datetime.utcnow(),
        "analysis": None
    }

    result = db.midi_files.insert_one(midi_doc)

    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "status": "uploaded"
    }
