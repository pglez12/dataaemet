from datetime import datetime, timedelta
import pandas as pd
from aemet_api import AemetAPI
from staging import Staging
from transformer import Transformer
from cloudops.logging.google import get_logger

logger = get_logger(__name__)

class Orchestrator:
    def __init__(self, config):
        self.config = config
        self.api = AemetAPI(config.source.endpoint, config.source.api_key)
        self.staging = Staging(config.sink.project_id, config.sink.dataset_name, config.sink.table_name)
        self.transformer = Transformer(config.dataform.project_id, config.dataform.location, config.dataform.dataset)

    def run(self):
        last_update = self.staging.get_last_update_datetime()
        if not last_update:
            last_update = datetime.utcnow() - timedelta(days=2)
        end_date = datetime.utcnow()
        
        data = self.api.get_data(last_update, end_date, "all")
        if data:
            df = pd.DataFrame(data)
            self.staging.load_data(df)
            self.transformer.run()
        else:
            logger.error("No data fetched from AEMET API")
