import requests
from datetime import datetime

class AemetAPI:
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    def get_data(self, start_date: datetime, end_date: datetime, station_id: str):
        url = f"{self.endpoint}/fechaini/{start_date.strftime('%Y-%m-%dT%H:%M:%S')}/fechafin/{end_date.strftime('%Y-%m-%dT%H:%M:%S')}/estacion/{station_id}"
        headers = {'api_key': self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
