# MIDI Analysis & Transformation Service

A production-oriented backend service for ingesting, analyzing, and transforming MIDI files. The system supports **asynchronous musical transformations** (e.g. transposition, tempo scaling), is fully containerized, and designed with clean separation between API, domain logic, and background execution.

---

## Key Features

- Upload and persist MIDI files
- Asynchronous background transformations (non-blocking API)
- Musical transformations:

  - Pitch transposition
  - Tempo scaling
- MongoDB-backed job & metadata tracking
- Deterministic, mathematical pytest validation
- Dockerized API + database (one-command startup)

---

## Architecture Overview

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

``` 
- **FastAPI** for the API layer  
- **Async background tasks** for compute isolation  
- **MongoDB** for job and metadata tracking  
- **Filesystem / Docker volume** for MIDI files  

---

## Supported Transformations

- **Transpose**: Shifts all note pitches by a fixed number of semitones  
- **Tempo Change**: Scales MIDI timing while preserving musical structure  

Transformations are deterministic and validated with automated tests.

---

## Async Processing Model

- API requests return immediately with a job reference
- Transformations run in the background
- Clients poll job status or fetch results when ready

This ensures predictable API latency regardless of processing time.

---

## Testing & CI

- Pytest-based tests validate pitch and tempo mathematically
- GitHub Actions CI runs tests on every push and pull request
- MongoDB is started as a service container during CI

---

## Docker & Deployment

The service is fully containerized and can be deployed locally or in cloud environments.

Designed to evolve toward:
- Dedicated worker processes
- Object storage (e.g. S3)
- Kubernetes-based scaling

---

## Performance & Scaling

- Lightweight, CPU-bound MIDI processing
- Async execution prevents API blocking
- Clear scaling path for throughput, compute, and storage
- MongoDB used only for metadata (no binary data)

---

## Future Work

- Symbolic music embeddings and similarity search
- ML-powered music analysis and transformations
- Hybrid symbolic + audio pipelines
- Research-to-production ML workflows

---

## Author

Arjun Gopalakrishnan
