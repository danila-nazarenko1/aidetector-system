import json
import time

from redis_client import r
from ai_detector import detect_from_code


PROCESSING = "processing"
DONE = "done"
ERROR = "error"


def process_job(job_id: str):

    key = f"job:{job_id}"

    data = r.get(key)

    if not data:
        return

    job = json.loads(data)

    job["status"] = PROCESSING
    r.set(key, json.dumps(job))

    results = {}

    try:

        for file in job["files"]:

            name = file["name"]
            code = file["code"]

            verdict = detect_from_code(code)

            results[name] = verdict

        job["status"] = DONE
        job["verdict"] = results

    except Exception as e:

        job["status"] = ERROR
        job["error"] = str(e)

    r.set(key, json.dumps(job))
