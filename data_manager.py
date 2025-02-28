from pprint import pprint
import requests
from dotenv import dotenv_values
secrets = dotenv_values(".env")

class DataManager:

    def __init__(self):
        self.sheety_headers = {'Authorization': secrets.get('SHEETY_API_KEY')}
        self.sheety_get_response = requests.get(url=secrets['SHEETY_GET_ENDPOINT'], headers=self.sheety_headers)
        self.sheety_get_response.raise_for_status()
        self.data = self.sheety_get_response.json()['prices']


    def put_request(self):
