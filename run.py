# import os
# import tempfile
import uvicorn

if __name__ == "__main__":
    # LOCK_PATH = os.environ["dramatiq_prom_lock"] = "tmp/dramatiq-prometheus.lock"
    # DB_PATH = os.environ["dramatiq_prom_db"] = "tmp/dramatiq-prometheus"
    # os.makedirs(DB_PATH, exist_ok=True)
    uvicorn.run("src.application:app", host="0.0.0.0", reload=True, workers=3)
