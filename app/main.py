from fastapi import FastAPI
from app.core.config import load_dotenv

load_dotenv()

app = FastAPI(title="MIDI Analysis Service")


@app.get("/health")
def health_check():
    return {"status": "ok"}

from app.db.mongodb import db

@app.get("/db-test")
def db_test():
    return {"collections": db.list_collection_names()}