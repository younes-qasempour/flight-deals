import requests
from dotenv import dotenv_values
secrets = dotenv_values(".env")

SHEETY_ENDPOINT = "https://api.sheety.co/84f207f4e918992a5c3e9f2a0c374657/flightDeals/sheet1"

class DataManager:

    def __init__(self):
        self.sheety_headers = {'Authorization': secrets.get('SHEETY_API_KEY')}
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=self.sheety_headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["sheet1"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "sheet1": {
                    "iataCode": city["iataCode"]
                }
            }
            requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=self.sheety_headers
            )