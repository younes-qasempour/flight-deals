# import time
# from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
import json
# ==================== Set up the Flight Search ====================

# data_manager = DataManager()
# sheet_data = data_manager.get_destination_data()

# with open('data.json', 'w') as file:
#     json.dump(sheet_data, file)

with open('data.json', 'r') as file:
    sheet_data = json.load(file)


flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================
# for row in sheet_data:
#     if row["iataCode"] == "":
#         row["iataCode"] = flight_search.get_destination_code(row["city"])
#         # slowing down requests to avoid rate limit
#         time.sleep(2)
#
# data_manager.destination_data = sheet_data
# data_manager.update_destination_codes()

# ==================== Search for Flights and Send Notifications ====================
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}")
    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = find_cheapest_flight(flights)
    if cheapest_flight.price != "N/A":
        if float(cheapest_flight.price) < float(destination["lowestPrice"]):
            print(f"\n\n\nLower price flight found to {destination['city']}!\n\n\n")
            notification_manager.send_sms(
                message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                             f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                             f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
            )
            # SMS not working? Try whatsapp instead.
            # notification_manager.send_whatsapp(
            #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
            #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
            #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
            # )