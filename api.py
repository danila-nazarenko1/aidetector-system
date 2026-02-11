import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from redis_client import r


load_dotenv()

app = FastAPI()


# ===== Models =====

class CodeFile(BaseModel):
    name: str
    code: str


class AnalyzeRequest(BaseModel):
    id: str
    files: List[CodeFile]


# ===== Status consts =====

RECEIVED = "received"


# ===== API =====

@app.post("/analyze")
def analyze(req: AnalyzeRequest):

    key = f"job:{req.id}"

    if r.exists(key):
        raise HTTPException(400, "Request already exists")

    job = {
        "id": req.id,
        "files": req.dict()["files"],
        "status": RECEIVED,
        "verdict": None
    }

    r.set(key, json.dumps(job))

    r.lpush("queue", req.id)

    return {
        "id": req.id,
        "status": RECEIVED,
        "message": "Request accepted"
    }

@app.get("/result/{job_id}")
def get_result(job_id: str):
    key = f"job:{job_id}"
    data = r.get(key)
    if not data:
        raise HTTPException(404, "Not found")
    job = json.loads(data)

    return job

