from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from datetime import datetime

from app.db.mongodb import db
from app.services.storage_service import StorageService
from app.services.analysis_service import MidiAnalysisService
from app.utils.hashing import compute_file_hash

from app.services.transformation_service import MidiTransformationService
import time

from bson import ObjectId
from app.workers.transformation_worker import run_transformation


router = APIRouter(prefix="/midi", tags=["midi"])

storage = StorageService()
analysis_service = MidiAnalysisService()
transform_service = MidiTransformationService()


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


@router.get("/{midi_id}")
def get_midi_analysis(midi_id: str):    
    midi = db.midi_files.find_one({"_id": ObjectId(midi_id)})

    if not midi:
        raise HTTPException(status_code=404, detail="MIDI not found")

    midi["_id"] = str(midi["_id"])
    return midi


@router.post("/{midi_id}/transpose")
def transpose_midi(
    midi_id: str,
    semitones: int,
    background_tasks: BackgroundTasks
):
    midi = db.midi_files.find_one({"_id": ObjectId(midi_id)})
    if not midi:
        raise HTTPException(status_code=404, detail="MIDI not found")

    job = {
        "midi_id": midi["_id"],
        "type": "transpose",
        "parameters": {"semitones": semitones},
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    result = db.transformations.insert_one(job)

    background_tasks.add_task(
        run_transformation,
        result.inserted_id,
        midi["storage_path"],
        "transpose",
        {"semitones": semitones}
    )

    return {
        "job_id": str(result.inserted_id),
        "status": "accepted"
    }


@router.post("/{midi_id}/tempo")
def change_tempo(
    midi_id: str,
    factor: float,
    background_tasks: BackgroundTasks
):
    if factor <= 0:
        raise HTTPException(status_code=400, detail="Factor must be > 0")

    midi = db.midi_files.find_one({"_id": ObjectId(midi_id)})
    if not midi:
        raise HTTPException(status_code=404, detail="MIDI not found")

    job = {
        "midi_id": midi["_id"],
        "type": "tempo_change",
        "parameters": {"factor": factor},
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    result = db.transformations.insert_one(job)

    background_tasks.add_task(
        run_transformation,
        result.inserted_id,
        midi["storage_path"],
        "tempo_change",
        {"factor": factor}
    )

    return {
        "job_id": str(result.inserted_id),
        "status": "accepted"
    }


@router.get("/transformations/{job_id}")
def get_transformation_status(job_id: str):
    job = db.transformations.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job["_id"] = str(job["_id"])
    job["midi_id"] = str(job["midi_id"])
    return job


