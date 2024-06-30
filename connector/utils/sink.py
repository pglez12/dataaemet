from google.cloud import bigquery
import logging

class BigQuerySink:
    def __init__(self, project_id, dataset_id, table_id):
        self.project_id = project_id
        self.dataset_id =  dataset_id
        self.table_id = table_id
        self.client = bigquery.Client(project=self.project_id)
        self.logger = logging.getLogger(__name__)

    def get_last_update_date(self):
        query = f"""
            SELECT MAX(fecha) AS last_update
            FROM `aemet_db.staging`
        """
        query_job = self.client.query(query)
        results = query_job.result()
        for row in results:
            return row.last_update

    def load_data(self, data):
        self.logger.info(f"Table name {self.table_id}")
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        job = self.client.load_table_from_json(data, table_ref, job_config=job_config)
        job.result()
        if job.errors:
            for error in job.errors:
                self.logger.error(f"Error loading data into BigQuery: {error}")
