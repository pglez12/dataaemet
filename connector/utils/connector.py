from datetime import datetime, timedelta
import logging
from google.cloud import bigquery

from utils.sink import BigQuerySink
from utils.source import AEMETSource

class Connector:
    def __init__(self, config):
        self.config = config
        self.source = AEMETSource(self.config["source"])
        self.sink = BigQuerySink(
            self.config["sink"]["project_id"],
            self.config["sink"]["dataset_name"],
            self.config["sink"]["table_name"]
        )
        self.logger = logging.getLogger(__name__)
        self.client = bigquery.Client(project=self.config["sink"]["project_id"])

    def incremental_load(self):
        try:
            end_date = datetime.utcnow() - timedelta(days=3)
            start_date = end_date - timedelta(days=1)
            self.extract_and_load_object(start_date, end_date)
        except Exception as e:
            self.logger.error(f"Error processing incremental load: {e}", exc_info=True)
            raise

    def backfill(self):
        try:
            end_date = datetime.utcnow()
            last_update_date = BigQuerySink.get_last_update_date(self)
            
            if last_update_date is None or not isinstance(last_update_date, datetime):
                start_date = end_date - timedelta(days=15)
            else:
                start_date = last_update_date
            self.extract_and_load_object(start_date, end_date)
        except Exception as e:
            self.logger.error(f"Error processing backfill: {e}", exc_info=True)
            
            raise

    def extract_and_load_object(self, start_date, end_date):
        try:
            data = self.source.fetch_data(start_date, end_date)
            if data:
                cleaned_data = self.clean_data(data, start_date, end_date)
                self.sink.load_data(cleaned_data)
            else:
                self.logger.info("No new data found to load.")
        except Exception as e:
            self.logger.error(f"Error extracting and loading data: {e}", exc_info=True)
            raise

    def clean_data(self, data, start_date, end_date):
        cleaned_data = []
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        query_template = """
            SELECT fecha, indicativo 
            FROM `aemet-data.aemet_db.staging`
            WHERE fecha >= @start_date AND fecha <= @end_date
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_date", "DATE", start_date_str),
                bigquery.ScalarQueryParameter("end_date", "DATE", end_date_str)
            ]
        )

        try:
            query_job = self.client.query(query_template, job_config=job_config)
            results = query_job.result()
            
            self.logger.info(f"Query returned {results.total_rows} rows.")
            
            existing_records = {(row.fecha, row.indicativo) for row in results}
            
            self.logger.info(f"Retrieved {len(existing_records)} unique records from BigQuery between {start_date_str} and {end_date_str}.")
            
        except Exception as e:
            self.logger.error(f"Error executing BigQuery query: {e}")
            raise

        for record in data:
            record_date = datetime.strptime(record['fecha'], '%Y-%m-%d').date()
            record_tuple = (record_date, record['indicativo'])
            if record_tuple in existing_records:
                self.logger.warning(f"Record {record_tuple} already exists in BigQuery, skipping insertion.")
            else:
                if 'prec' in record:
                    if record['prec'] == "Ip":
                        record['prec'] = 0.09
                    elif record['prec'] == "Acum":
                        record['prec'] = 0.0
                required_fields = ['fecha', 'indicativo', 'nombre', 'provincia', 'altitud']
                if all(record.get(field) is not None for field in required_fields):
                    processed_record = {
                        "fecha": record_date.isoformat(),
                        "indicativo": record["indicativo"],
                        "nombre": record["nombre"],
                        "provincia": record["provincia"],
                        "altitud": float(record["altitud"]),
                        "tmed": parse_float(record.get("tmed")),
                        "prec": parse_float(record.get("prec")),
                        "tmin": parse_float(record.get("tmin")),
                        "horatmin": record.get("horatmin"),
                        "tmax": parse_float(record.get("tmax")),
                        "horatmax": record.get("horatmax"),
                        "dir": parse_float(record.get("dir")),
                        "velmedia": parse_float(record.get("velmedia")),
                        "racha": parse_float(record.get("racha")),
                        "horaracha": record.get("horaracha"),
                        "sol": parse_float(record.get("sol")),
                        "presmax": parse_float(record.get("presMax")),
                        "horapresmax": record.get("horaPresMax"),
                        "presmin": parse_float(record.get("presMin")),
                        "horapresmin": record.get("horaPresMin"),
                        "hrmedia": parse_float(record.get("hrMedia")),
                        "hrmax": parse_float(record.get("hrMax")),
                        "horahrmax": record.get("horaHrMax"),
                        "hrmin": parse_float(record.get("hrMin")),
                        "horahrmin": record.get("horaHrMin"),
                    }
                    cleaned_data.append(processed_record)
                else:
                    self.logger.error(f"Record missing required fields: {record}")
        return cleaned_data

def parse_float(value):
    try:
        return float(value.replace(",", "."))
    except (ValueError, AttributeError):
        return None