import logging, signal, time
from app.orchestrator.queue import dequeue
from app.orchestrator.engine import execute_campaign

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
running = True

def stop(*_):
    global running
    running = False

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)

if __name__ == "__main__":
    logging.info("AI Red Team campaign worker started")
    while running:
        try:
            job = dequeue(timeout=5)
            if job:
                cid = int(job["campaign_id"])
                logging.info("Executing campaign %s", cid)
                execute_campaign(cid)
        except Exception:
            logging.exception("Worker loop failure")
            time.sleep(2)
    logging.info("Worker stopped")
