from apscheduler.schedulers.blocking import BlockingScheduler
from redis_client import r
from worker import process_job


scheduler = BlockingScheduler()


@scheduler.scheduled_job("interval", seconds=20)
def run_worker():

    print("Checking queue...")

    job_id = r.rpop("queue")

    if not job_id:
        print("No jobs")
        return

    print("Processing:", job_id)

    process_job(job_id)


if __name__ == "__main__":
    scheduler.start()
