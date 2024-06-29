import requests
import logging
import os
from google.cloud import bigquery

AEMET_API_KEY = os.getenv("AEMET_API_KEY")
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

        logging.info(f"Realizando solicitud a {url} con headers {headers}")
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
                logging.info("No hay nuevos datos para insertar en estaciones.")

            return {"message": "Datos de estaciones obtenidos y guardados en BigQuery exitosamente"}
        else:
            error_detail = {
                "status_code": response.status_code,
                "message": "Error al obtener datos de la API de AEMET",
                "detail": response.content.decode('utf-8')
            }
            raise Exception(f"Error: {error_detail}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error de conexión con la API de AEMET: {str(e)}")
        raise Exception(f"Error de conexión con la API de AEMET: {str(e)}")

    except Exception as e:
        logging.error(f"Error inesperado en la aplicación: {str(e)}")
        raise Exception(f"Error inesperado en la aplicación: {str(e)}")

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
            logging.error(f"Error procesando entrada de estación: {entry}. Error: {str(e)}")

    return processed_data

import logging

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
        logging.error(f"Error al convertir el valor: {value}. Error: {str(e)}")
        return value

def save_estaciones_to_bigquery(data):
    try:
        dataset_ref = client.dataset(DATASET_ID)
        table_ref = dataset_ref.table(ESTACIONES_TABLE_ID)

        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")

        job = client.load_table_from_json(data, table_ref, job_config=job_config)
        job.result()

        logging.info("Datos de estaciones insertados correctamente en BigQuery")
    except Exception as e:
        logging.error(f"Error al guardar datos de estaciones en BigQuery: {str(e)}")
        raise e
