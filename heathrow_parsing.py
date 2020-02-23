from datetime import datetime
from heathrow_extraction import load_data, extract_flight_list
import numpy as np
import pandas as pd

class Flight(object):

    def __init__(self, raw_flight):
        self.flight_id = None
        self.scheduled_datetime = None
        self.departure_datetime = None
        self.delay_mins = None

        self.parse_heathrow_flight(raw_flight)
        self.delay_mins = self.calculate_delay_minutes(self.scheduled_datetime, self.departure_datetime)

    def parse_heathrow_flight(self, raw_flight):
        #Add more parsing to get times as datetime format & remove whitespace from flightId
        assert type(raw_flight) == dict
        self.flight_id = raw_flight['flightIdentifier']
        scheduled_time_str = raw_flight['origin']['scheduledDateTime']['local']
        self.scheduled_datetime = datetime.strptime(scheduled_time_str[:-7], "%Y-%m-%dT%H:%M")
        status = raw_flight['origin']['status']['messages']['message'][0]['text']
        if status == "Departed":
            departure_time_str = raw_flight['origin']['status']['messages']['message'][0]['data']
            departure_datetime_str = raw_flight['origin']['status']['statusTime']
            if departure_time_str == departure_datetime_str[11:-8]:
                self.departure_datetime = datetime.strptime(departure_datetime_str[:-8], "%Y-%m-%dT%H:%M")
        return None

    @staticmethod
    def calculate_delay_minutes(scheduled_datetime, departure_datetime):
        if None in (scheduled_datetime, departure_datetime):
            return None
        else:
            delay_mins = (departure_datetime - scheduled_datetime).total_seconds() / 60
            return delay_mins

    def to_list(self):
        flight_info = [self.flight_id, self.scheduled_datetime, self.departure_datetime]
        return flight_info

    @staticmethod
    def labels():
        return ["flight_id", "scheduled_datetime", "departure_datetime"]

class ParsedFlights(object):

    def __init__(self, raw_flights):
        self.parsed_flights = []
        assert type(raw_flights) == list
        for raw_flight in raw_flights:
            flight = Flight(raw_flight)
            self.parsed_flights.append(flight)

    def to_dataframe(self):
        data = []
        for flight in self.parsed_flights:
            row_data = flight.to_list()
            data.append(row_data)
        df = pd.DataFrame(np.array(data), columns = Flight.labels())
        return df

if __name__ == '__main__':
    raw_data = load_data()
    raw_flights = extract_flight_list(raw_data)
    print("\nHere's the PAYLOAD from the first flight in `raw_data`: \n", raw_flights[0])

    print("\n--------------------Debugging for unittest of Departure/Scheduled Time")
    flight = Flight(raw_flights[0])
    print("Scheduled:", flight.scheduled_datetime, "\nDeparture:", flight.departure_datetime)
    print("Scheduled datatype:", type(flight.scheduled_datetime), "\nDeparture datatype:", type(flight.departure_datetime))

    print("\n--------------------Here's the LATEST, it's all coming together in a dataframe")
    parsed_flights = ParsedFlights(raw_flights)
    flights_df = parsed_flights.to_dataframe()
    print("There are", len(raw_flights), "flights in `raw_flights`")
    print("There are", len(flights_df), "flights in the dataframe (`flights_df`)")
    print("Head is:\n", flights_df.head())
    print("Tail is:\n", flights_df.tail())
