from google.cloud import bigquery
import os
import logging

DATASET_ID = "aemet_db"  # Corrected assignment
TABLE_ID = "data_stagging2"  # Corrected assignment

class BigQuerySink:
    def __init__(self, project_id, dataset_id, table_id):
        self.project_id = "aemet-data"
        self.dataset_id =  "aemet_db"
        self.table_id = "data_stagging2"
        self.client = bigquery.Client(project=self.project_id)
        self.logger = logging.getLogger(__name__)

    def get_last_update_date(self):
        query = f"""
            SELECT MAX(fecha) AS last_update
            FROM {self.dataset_id}.{self.table_id}
        """
        query_job = self.client.query(query)
        results = query_job.result()
        for row in results:
            return row.last_update

    def load_data(self, data):
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        job = self.client.load_table_from_json(data, table_ref, job_config=job_config)
        job.result()
        if job.errors:
            for error in job.errors:
                self.logger.error(f"Error loading data into BigQuery: {error}")

def main():
    project_id = os.getenv('PROJECT_ID')
    dataset_id = os.getenv('DATASET_ID')
    table_id = os.getenv('TABLE_ID')

    if not (project_id and dataset_id and table_id):
        raise ValueError("Missing PROJECT_ID, DATASET_ID, or TABLE_ID environment variable")

    try:
        sink = BigQuerySink(project_id, dataset_id, table_id)
        last_date = sink.get_last_update_date()
        # Assume data is loaded into 'data' variable
        data = []  # Dummy data, replace with actual data
        sink.load_data(data)
    except Exception as e:
        print(f"Error procesando la carga incremental: {e}")

if __name__ == "__main__":
    main()