import pandas as pd
from google.cloud import bigquery

class Staging:
    def __init__(self, project_id, dataset_name, table_name):
        self.client = bigquery.Client(project=project_id)
        self.dataset_name = dataset_name
        self.table_name = table_name

    def get_last_update_datetime(self):
        query = f"SELECT MAX(date) as last_update FROM `{self.dataset_name}.{self.table_name}`"
        query_job = self.client.query(query)
        result = query_job.result()
        return result[0].last_update if result.total_rows > 0 else None

    def load_data(self, data: pd.DataFrame):
        table_id = f"{self.dataset_name}.{self.table_name}"
        job = self.client.load_table_from_dataframe(data, table_id)
        job.result()
