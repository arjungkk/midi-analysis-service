from fastapi import FastAPI

app = FastAPI(title="MIDI Analysis Service")


@app.get("/health")
def health_check():
    return {"status": "ok"}
