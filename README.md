# MIDI Analysis & Transformation Service

A production-oriented backend service for ingesting, analyzing, and transforming MIDI files. The system supports **asynchronous musical transformations** (e.g. transposition, tempo scaling), is fully containerized, and designed with clean separation between API, domain logic, and background execution.

---

## 🚀 Key Features

* Upload and persist MIDI files
* Asynchronous background transformations (non-blocking API)
* Musical transformations:

  * Pitch transposition
  * Tempo scaling
* MongoDB-backed job & metadata tracking
* Deterministic, mathematical pytest validation
* Dockerized API + database (one-command startup)

---

## 🧠 Architecture Overview

```
                ┌──────────────┐
                │   Client     │
                │ (curl / UI)  │
                └──────┬───────┘
                       │ HTTP
                       ▼
               ┌─────────────────┐
               │   FastAPI API   │
               │  (Stateless)   │
               └──────┬─────────┘
          create job  │
          enqueue     │
                       ▼
        ┌─────────────────────────┐
        │ Background Task Executor │
        │ (FastAPI BackgroundTasks)│
        └──────┬──────────────────┘
               │ calls
               ▼
     ┌──────────────────────────────┐
     │ MidiTransformationService    │
     │  - transpose                 │
     │  - change_tempo              │
     │  (pure domain logic)         │
     └──────┬──────────────────────┘
            │ writes output
            ▼
        ┌──────────────┐
        │ File Storage │
        │ (Docker vol) │
        └──────────────┘

 MongoDB is used throughout to persist:
 - MIDI metadata
 - Transformation jobs
 - Status, timing, output paths
```

**Design principles:**

* Stateless API layer
* Asynchronous execution boundary
* Pure, testable domain logic
* Explicit job state tracking

---

## 🧩 Tech Stack

* **Language:** Python 3.11
* **API:** FastAPI
* **Async execution:** FastAPI BackgroundTasks
* **MIDI processing:** pretty_midi
* **Database:** MongoDB
* **Testing:** pytest
* **Containerization:** Docker, docker-compose

---

## 📁 Project Structure

```
app/
├── api/
│   └── routes/
│       └── midi.py        # HTTP endpoints
├── services/
│   └── midi_transformation_service.py
├── workers/
│   └── transformation_tasks.py
├── db/
│   └── mongodb.py
├── main.py

tests/
├── conftest.py
├── test_transpose.py
├── test_tempo_change.py

Dockerfile
docker-compose.yml
requirements.txt
```

---

## 🔄 Async Transformation Flow

1. Client uploads a MIDI file
2. Client requests a transformation (transpose / tempo)
3. API immediately returns `job_id`
4. Transformation runs asynchronously in background
5. Job status + output path persisted in MongoDB
6. Client polls job endpoint for completion

This pattern mirrors real-world **data pipeline and ML inference systems**.

---

## 🧪 Testing Strategy

Transformations are validated **mathematically**:

* **Transpose:**

  * Assert `output_pitch == input_pitch + semitones`
* **Tempo change:**

  * Assert `output_duration == input_duration / factor`

Tests use:

* Deterministic MIDI fixtures
* `tmp_path` isolation
* Black-box testing of domain logic

Run tests:

```bash
pytest -v
```

---

## 🐳 Running with Docker

```bash
docker compose build
docker compose up
```

API available at:

```
http://localhost:8000
```

MongoDB available at:

```
localhost:27017
```

---

## 🔮 Future Extensions

* Replace BackgroundTasks with Celery / Redis
* Chain transformations (pipeline DAG)
* Audio rendering / preview generation
* Model-based MIDI analysis (ML features)
* Web frontend for browsing transformations

---

## 👤 Author

Built by a Lead/Senior Software Engineer with experience in:

* Distributed systems
* Data-intensive pipelines
* AI-driven platforms
* Music technology

This project is intentionally scoped to demonstrate **production engineering quality**, not just musical features.
