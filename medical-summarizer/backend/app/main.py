import os
import uuid
import shutil
import pathlib
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
from backend.worker.worker import RESULT_DIR

# load .env
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery client
celery = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

# Upload/result dirs
UPLOAD_DIR = pathlib.Path("/tmp/uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
from worker.worker import RESULT_DIR  # noqa: E402

app = FastAPI(title="Medical Report Summarizer")

# CORS (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/summarize")
async def summarize_pdf(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(415, "Only PDF uploads allowed")
    job_id = uuid.uuid4().hex
    dest = UPLOAD_DIR / f"{job_id}.pdf"
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    # enqueue
    from worker.worker import summarize_job
    summarize_job.delay(job_id, str(dest))
    return {"job_id": job_id}

@app.get("/api/status/{job_id}")
def get_status(job_id: str):
    res = celery.AsyncResult(job_id)
    return {"status": res.status.lower()}

@app.get("/api/result/{job_id}")
def get_result(job_id: str):
    res = celery.AsyncResult(job_id)
    if not res.ready():
        raise HTTPException(202, "Processing")
    payload = res.result or {}
    return payload.get("meta", {})

@app.get("/api/download/{job_id}")
def download(job_id: str):
    out = RESULT_DIR / f"{job_id}.pdf"
    if not out.exists():
        raise HTTPException(404, "Not ready")
    return FileResponse(out, media_type="application/pdf", filename=out.name)
