from app.queue.redis_client import dequeue_job
from app.worker.runner import process_job

def main() -> None: #main always runs (pulls from queue and processes using worker's process job)
    while True:
        job_id = dequeue_job()
        if job_id is None:
            continue
        process_job(job_id)
            
if __name__ == "__main__":
    main()