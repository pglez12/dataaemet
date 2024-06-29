import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException
import uvicorn
from config import get_config
from connector import Connector
from locations import fetch_and_save_estaciones

# Basic logging configuration
logging.basicConfig(level=logging.INFO)

# Rotating file handler for more detailed logs
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Create a logger instance
logger = logging.getLogger(__name__)
logger.addHandler(handler)  # Add the rotating file handler to the logger

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
