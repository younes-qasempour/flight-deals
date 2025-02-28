from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from pprint import pprint
import requests
from dotenv import dotenv_values
secrets = dotenv_values(".env")

data_manager = DataManager()
sheet_data = data_manager.data

# pprint(sheet_data)

for dic in sheet_data:
    if dic['iataCode'] == "":
        flight_search = FlightSearch(dic['city'])
        dic['iataCode'] = flight_search.iatacode

pprint(sheet_data)



