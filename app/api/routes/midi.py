from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime

from app.db.mongodb import db
from app.services.storage_service import StorageService
from app.services.analysis_service import MidiAnalysisService
from app.utils.hashing import compute_file_hash

router = APIRouter(prefix="/midi", tags=["midi"])

storage = StorageService()
analysis_service = MidiAnalysisService()


@router.post("")
async def upload_midi(file: UploadFile = File(...)):
    if not file.filename.endswith(".mid"):
        raise HTTPException(status_code=400, detail="Only MIDI files are supported")

    content = await file.read()
    file_hash = compute_file_hash(content)
    file_path = storage.save_file(file.filename, content)

    analysis = analysis_service.analyze(file_path)

    midi_doc = {
        "filename": file.filename,
        "file_hash": file_hash,
        "storage_path": file_path,
        "analysis": analysis,
        "created_at": datetime.utcnow(),
        "analyzed_at": datetime.utcnow()
    }

    result = db.midi_files.insert_one(midi_doc)

    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "analysis_summary": {
            "tempo_bpm": analysis["tempo_bpm"],
            "estimated_key": analysis["estimated_key"]
        }
    }

from bson import ObjectId

@router.get("/{midi_id}")
def get_midi_analysis(midi_id: str):    
    midi = db.midi_files.find_one({"_id": ObjectId(midi_id)})

    if not midi:
        raise HTTPException(status_code=404, detail="MIDI not found")

    midi["_id"] = str(midi["_id"])
    return midi
