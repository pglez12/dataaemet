from fastapi import FastAPI
from cloudops.logging.google import get_logger

from aemet_utils.config import get_config
from orchestrator import Orchestrator

logger = get_logger(__name__)
app = FastAPI()

@app.get("/run")
def run_etl():
    config = get_config("./config.yaml")
    orchestrator = Orchestrator(config)
    orchestrator.run()
    return {"status": "ETL process completed"}
