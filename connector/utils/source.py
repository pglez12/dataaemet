import requests
import logging

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
            self.logger.info(f"Making request to {url} with headers {headers}")
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
                    self.logger.error("Data URL not found in AEMET response.")
                    return None
            else:
                error_detail = {
                    "status_code": response.status_code,
                    "message": "Error obtaining data from AEMET API",
                    "detail": response.content.decode('utf-8')
                }
                self.logger.error(f"Error obtaining data from AEMET API: {error_detail}")
                return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Connection error with AEMET API: {str(e)}")
            raise

        except Exception as e:
            self.logger.error(f"Unexpected error processing request to AEMET: {str(e)}", exc_info=True)
            raise
