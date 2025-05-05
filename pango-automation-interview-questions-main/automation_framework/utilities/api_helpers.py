import requests
import configparser
from pathlib import Path


class ApiHelper:

    def __init__(self):
        config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent / 'config' / 'config.ini'

        #error if file not in path
        if not config_path.is_file():
             raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        config.read(config_path)
        try:
            self.api_key = config['API']['API_KEY']
            self.base_url = config['API']['BASE_URL']
        except KeyError as err:
            raise KeyError(f"Missing key in config {err}")

        

    def get_current_weather(self, city_id):
        url = f"{self.base_url}?id={city_id}&units=metric&appid={self.api_key}"
        print(url)
        response = requests.get(url)
        print(response)
        return response
