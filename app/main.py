from fastapi import FastAPI
from app.core.config import load_dotenv
from app.api.routes.midi import router as midi_router

load_dotenv()

app = FastAPI(title="MIDI Analysis Service")

app.include_router(midi_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

from app.db.mongodb import db

@app.get("/db-test")
def db_test():
    return {"collections": db.list_collection_names()}