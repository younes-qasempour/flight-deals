import requests
from dotenv import dotenv_values
secrets = dotenv_values(".env")

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/84f207f4e918992a5c3e9f2a0c374657/flightDeals/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/84f207f4e918992a5c3e9f2a0c374657/flightDeals/users"


class DataManager:

    def __init__(self):
        self.sheety_headers = {'Authorization': secrets.get('SHEETY_API_KEY')}
        self.prices_endpoint = SHEETY_PRICES_ENDPOINT
        self.users_endpoint = SHEETY_USERS_ENDPOINT
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.prices_endpoint, headers=self.sheety_headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["price"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            requests.put(
                url=f"{self.prices_endpoint}/{city['id']}",
                json=new_data,
                headers=self.sheety_headers
            )

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, headers=self.sheety_headers)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data