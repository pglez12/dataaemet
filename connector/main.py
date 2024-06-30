import logging
from fastapi import FastAPI, HTTPException
import uvicorn
from config import get_config
from utils.connector import Connector
from utils.locations import fetch_and_save_estaciones

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def get_connector() -> Connector:
    config = get_config("./config.yaml")
    connector = Connector(config)
    return connector

@app.get("/incremental_load")
def process_incremental_load():
    try:
        connector = get_connector()
        connector.incremental_load()
        return {"message": "Incremental load processed successfully"}
    except Exception as e:
        logger.error(f"Error processing incremental load: {e}")
        raise HTTPException(status_code=500, detail="Error processing incremental load")

@app.get("/backfill")
def backfill():
    try:
        connector = get_connector()
        connector.backfill()
        return {"message": "Backfill processed successfully"}
    except Exception as e:
        logger.error(f"Error processing backfill: {e}")
        raise HTTPException(status_code=500, detail="Error processing backfill")

@app.get("/locations")
def update_locations():
    try:
        fetch_and_save_estaciones()
        return {"message": "Locations updated successfully"}
    except Exception as e:
        logger.error(f"Error updating locations: {e}")
        raise HTTPException(status_code=500, detail="Error updating locations")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
