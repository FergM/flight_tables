from datetime import datetime
import numpy as np
import pandas as pd

class Flight(object):

    def __init__(self, raw_flight):
        self.flight_id = None
        self.scheduled_datetime = None
        self.actual_datetime = None
        self.delay_mins = None
        self.status = None
        self.code_share_type = None
        self.origin = None
        self.destination = None

        self.parse_heathrow_flight(raw_flight)
        self.delay_mins = self.calculate_delay_minutes(self.scheduled_datetime, self.actual_datetime)

    def parse_heathrow_flight(self, raw_flight):
        #Add more parsing to get times as datetime format & remove whitespace from flightId
        #Try accept is alternative to specifying arrival/departure in the input.
        #    Might make more sense to tell catch case where data is for departure but should be for arrival.
        assert type(raw_flight) == dict
        self.flight_id = raw_flight['flightIdentifier']

        # Get Origin and Destination
        self.origin = raw_flight['origin']['airportIataRef']
        self.destination = raw_flight['destination']['airportIataRef']

        # Get Status and Location
        try:
            status = raw_flight['origin']['status']['messages']['message'][0]['text']
            location = 'origin'
        except:
            status = raw_flight['destination']['status']['messages']['message'][0]['text']
            location = 'destination'

        # Get Scheduled Time
        scheduled_time_str = raw_flight[location]['scheduledDateTime']['local']
        self.scheduled_datetime = datetime.strptime(scheduled_time_str[:-7], "%Y-%m-%dT%H:%M")

        # Assign Status
        self.status = status

        # Assign Actual Time
        if status == "Cancelled":
            self.status = "Cancelled"
        elif (status == "Departed") or (status=="Landed"):
            actual_date_str = raw_flight[location]['status']['statusTime'][0:11]
            actual_time_str = raw_flight[location]['status']['messages']['message'][0]['data']
            actual_datetime_str = actual_date_str + actual_time_str
            self.actual_datetime = datetime.strptime(actual_datetime_str, "%Y-%m-%dT%H:%M")
        else:
            self.status = f"Unexpected Status: {status}" # ToDo: Handle this better?

        # Assign code_share_type
        self.code_share_type = raw_flight["codeShareType"]

        return None

    @staticmethod
    def calculate_delay_minutes(scheduled_datetime, actual_datetime):
        if None in (scheduled_datetime, actual_datetime):
            return None
        else:
            delay_mins = (actual_datetime - scheduled_datetime).total_seconds() / 60
            return delay_mins

    def to_list(self):
        flight_info = [self.flight_id, self.scheduled_datetime, self.actual_datetime, self.delay_mins, self.status, self.code_share_type, self.origin, self.destination]
        return flight_info

    @staticmethod
    def labels():
        return ["flight_id", "scheduled_datetime", "actual_datetime", "delay_mins", "status", "code_share", "origin", "destination"]

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
    def load_json_file(full_file_name):
        with open(full_file_name) as json_file:
            py_obj = json.load(json_file)
        return py_obj

    full_file_name = "../data/heathrow_data/2020-02-02Z.json"
    raw_data = load_json_file(full_file_name)
    raw_flights = raw_data['flightSummaryList']['flight']
    print("\nHere's the PAYLOAD from the first flight in `raw_data`: \n", raw_flights[0])

    print("\n--------------------Debugging for unittest of Departure/Scheduled Time")
    flight = Flight(raw_flights[0])
    print("Scheduled:", flight.scheduled_datetime, "\nDeparture:", flight.actual_datetime)
    print("Scheduled datatype:", type(flight.scheduled_datetime), "\nDeparture datatype:", type(flight.actual_datetime))

    print("\n--------------------Here's the LATEST, it's all coming together in a dataframe")
    parsed_flights = ParsedFlights(raw_flights)
    flights_df = parsed_flights.to_dataframe()
    print("There are", len(raw_flights), "flights in `raw_flights`")
    print("There are", len(flights_df), "flights in the dataframe (`flights_df`)")
    print("Head is:\n", flights_df.head())
    print("Tail is:\n", flights_df.tail())
