from datetime import datetime

import pandas as pd
import pydantic

class DummySourceConfig(pydantic.BaseModel):
    endpoint: str
    api_key: str

class DummySource:
    def __init__(self, config: DummySourceConfig):
        self.config = config

    def extract_object(
        self, object_id: str, start_datetime: datetime, end_datetime: datetime
    ) -> pd.DataFrame:
        # Implementa la lógica para extraer datos desde la API de AEMET
        return pd.DataFrame()
