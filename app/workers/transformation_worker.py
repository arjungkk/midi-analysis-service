from datetime import datetime
from app.db.mongodb import db
from app.services.transformation_service import MidiTransformationService


service = MidiTransformationService()


def run_transformation(job_id, midi_path, transform_type, params):
    try:
        if transform_type == "transpose":
            result = service.transpose(midi_path, params["semitones"])

        elif transform_type == "tempo_change":
            result = service.change_tempo(midi_path, params["factor"])

        else:
            raise ValueError("Unknown transformation type")

        db.transformations.update_one(
            {"_id": job_id},
            {"$set": {
                "status": "completed",
                "output_path": result["output_path"],
                "processing_time_ms": result["processing_time_ms"],
                "completed_at": datetime.utcnow()
            }}
        )

    except Exception as e:
        db.transformations.update_one(
            {"_id": job_id},
            {"$set": {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.utcnow()
            }}
        )
