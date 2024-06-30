import requests
import logging
import os
from google.cloud import bigquery

AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcHR5bGxhbmFAZ21haWwuY29tIiwianRpIjoiMjJjNGNkZGQtZmQyNy00YTM3LWFlYmMtYjY3NjNiMjA4MmMzIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3MTgwOTMxNTksInVzZXJJZCI6IjIyYzRjZGRkLWZkMjctNGEzNy1hZWJjLWI2NzYzYjIwODJjMyIsInJvbGUiOiIifQ.dsLyBdXEMU2JoAYTjZTRyxtMje5t3iAT__9Moy7tl5g"
PROJECT_ID = "aemet-data"
DATASET_ID = "aemet_db"
ESTACIONES_TABLE_ID = "estaciones"

client = bigquery.Client(project=PROJECT_ID)

def fetch_and_save_estaciones():
    try:
        url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
        headers = {
            'accept': 'application/json',
            'api_key': AEMET_API_KEY
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            data_url = data['datos']
            response = requests.get(data_url, headers=headers)
            response.raise_for_status()
            estaciones_data = response.json()

            processed_estaciones_data = process_estaciones_data(estaciones_data)
            if processed_estaciones_data:
                save_estaciones_to_bigquery(processed_estaciones_data)
            else:
                logging.info("No new data to insert in estaciones.")

            return {"message": "Estaciones data successfully retrieved and saved to BigQuery"}
        else:
            error_detail = {
                "status_code": response.status_code,
                "message": "Error retrieving data from AEMET API",
                "detail": response.content.decode('utf-8')
            }
            raise Exception(f"Error: {error_detail}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error with AEMET API: {str(e)}")
        raise Exception(f"Connection error with AEMET API: {str(e)}")

    except Exception as e:
        logging.error(f"Unexpected application error: {str(e)}")
        raise Exception(f"Unexpected application error: {str(e)}")

def process_estaciones_data(data):
    processed_data = []

    for entry in data:
        try:
            processed_entry = {
                "latitud": edit_form(entry["latitud"]),
                "provincia": entry["provincia"],
                "indicativo": entry["indicativo"],
                "altitud": float(entry["altitud"]),
                "nombre": entry["nombre"],
                "indsinop": entry["indsinop"],
                "longitud": edit_form(entry["longitud"])
            }
            processed_data.append(processed_entry)
        except Exception as e:
            logging.error(f"Error processing station entry: {entry}. Error: {str(e)}")
    return processed_data

def edit_form(value):
    try:
        degrees = int(value[:2])
        minutes = int(value[2:4])
        seconds = int(value[4:6])
        direction = value[-1]
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if direction in ['S', 'W']:
            decimal = -decimal
        decimal = round(decimal, 6)
        return decimal
    except Exception as e:
        logging.error(f"Error converting value: {value}. Error: {str(e)}")
        return value

def save_estaciones_to_bigquery(data):
    try:
        table_ref = client.dataset(DATASET_ID).table(ESTACIONES_TABLE_ID)

        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")

        job = client.load_table_from_json(data, table_ref, job_config=job_config)
        job.result()

        logging.info("Estaciones data successfully inserted into BigQuery")
    except Exception as e:
        logging.error(f"Error saving estaciones data to BigQuery: {str(e)}")
        raise e
