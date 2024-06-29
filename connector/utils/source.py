
import requests
import logging

AEMET_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcHR5bGxhbmFAZ21haWwuY29tIiwianRpIjoiMjJjNGNkZGQtZmQyNy00YTM3LWFlYmMtYjY3NjNiMjA4MmMzIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3MTgwOTMxNTksInVzZXJJZCI6IjIyYzRjZGRkLWZkMjctNGEzNy1hZWJjLWI2NzYzYjIwODJjMyIsInJvbGUiOiIifQ.dsLyBdXEMU2JoAYTjZTRyxtMje5t3iAT__9Moy7tl5g"

class AEMETSource:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def fetch_data(self, start_date, end_date):
        url = self.config["base_url"].format(
            start_date=start_date.strftime("%Y-%m-%dT00:00:00UTC"),
            end_date=end_date.strftime("%Y-%m-%dT01:00:00UTC")
        )
        headers = {
            'accept': 'application/json',
            'api_key': self.config["api_key"]
        }

        try:
            self.logger.info(f"Realizando solicitud a {url} con headers {headers}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()
                data_url = data.get('datos')
                if data_url:
                    response_data = requests.get(data_url, headers=headers)
                    response_data.raise_for_status()
                    return response_data.json()
                else:
                    self.logger.error("No se encontró la URL de datos en la respuesta de AEMET.")
                    return None
            else:
                error_detail = {
                    "status_code": response.status_code,
                    "message": "Error al obtener datos de la API de AEMET",
                    "detail": response.content.decode('utf-8')
                }
                self.logger.error(f"Error al obtener datos de la API de AEMET: {error_detail}")
                return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de conexión con la API de AEMET: {str(e)}")
            raise

        except Exception as e:
            self.logger.error(f"Error inesperado al procesar solicitud a AEMET: {str(e)}", exc_info=True)
            raise