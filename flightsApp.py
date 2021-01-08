from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "DFW"

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_code(city_names)
    data_manager.update_destination_codes()
    sheet_data = data_manager.get_destination_data()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    print(flight.price)
    if flight is None:
        continue

    # if flight.price < destinations[destination_code]["price"]:
    #     message = f"Low price alert! Only ${flight.price} to fly from " \
    #               f"{flight.origin_city}-{flight.origin_airport} to " \
    #               f"{flight.destination_city}-{flight.destination_airport}, " \
    #               f"from {flight.out_date} to {flight.return_date}."
    #     if flight.stop_overs > 0:
    #         message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}.\n"
    #         link = f"https://www.google.com/flights?hl=en#flt={flight.origin_airport}." \
    #                f"{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}." \
    #                f"{flight.origin_airport}.{flight.return_date}"
    #         message += link
    #         print(message)
    #     notification_manager.send_sms(message=message)
