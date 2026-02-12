import json
import time

from redis_client import r
from ai_detector import detect_from_code


PROCESSING = "PROCESSING"
DONE = "DONE"
ERROR = "ERROR"


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

        if "files" in job:
            del job["files"]

        job["status"] = DONE
        job["verdict"] = results

    except Exception as e:

        if "files" in job:
            del job["files"]

        job["status"] = ERROR
        job["error"] = str(e)

    r.set(key, json.dumps(job))