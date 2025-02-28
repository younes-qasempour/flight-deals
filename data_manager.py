from pprint import pprint
from flight_search import FlightSearch
import requests
from dotenv import dotenv_values
secrets = dotenv_values(".env")

class DataManager:

    def __init__(self):
        self.sheety_headers = {'Authorization': secrets.get('SHEETY_API_KEY')}
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=secrets['SHEETY_ENDPOINT'], headers=self.sheety_headers)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{secrets['SHEETY_ENDPOINT']}/{city['id']}",
                json=new_data,
                headers=self.sheety_headers
            )
            print(response.text)