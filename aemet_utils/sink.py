from datetime import datetime

import pandas as pd
import pydantic
from google.cloud import bigquery

class DummySinkConfig(pydantic.BaseModel):
    project_id: str
    dataset_name: str
    table_name: str

class DummySink:
    def __init__(self, config: DummySinkConfig):
        self.config = config
        self.client = bigquery.Client()

    def get_last_update_datetime(self, object_id: str) -> datetime:
        # Implementa la lógica para obtener la última fecha de actualización
        return datetime(2021, 1, 1, 0, 0, 0)

    def load_object(self, object_id: str, df: pd.DataFrame) -> None:
        table_id = f"{self.config.project_id}.{self.config.dataset_name}.{self.config.table_name}"
        job = self.client.load_table_from_dataframe(df, table_id)
        job.result()
