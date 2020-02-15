from heathrow_extraction import load_data, extract_flight_list
import numpy as np
import pandas as pd

class Flight(object):

    def __init__(raw_flight):
        self.flight_id
        self.scheduled_datetime
        self.departure_datetime
        parse_heathrow_flights(self, raw_flights)

    def parse_heathrow_flights(raw_flights):
        return None

    def to_list(self):
        flight_info = [self.flight_id, self.scheduled_datetime, self.departure_datetime]
        return flight_info

    @staticmethod
    def labels():
        return ["flight_id", "scheduled_datetime", "departure_datetime"]

class ParsedFlights(object):

    def __init__(raw_flights):
        self.parsed_flights = []
        for flight in raw_flights:
            flight = Flight(raw_flight)
            parsed_flights.append(flight);

    def to_dataframe(self):
        data = []
        for flight in self.parsed_flights():
            row_data = flight.to_list()
            data.append(row_data)
        df = pd.DataFrame(np.array(data), columns = Flight().labels())
        return df

if __name__ == '__main__':
    raw_data = load_data()
    raw_flights = extract_flight_list(raw_data)
    print("Here's raw data from the first flight: \n\t", raw_flights[0])

    #parsed_flights = ParsedFlights(raw_flights)
    #flights_df = parsed_flights.to_dataframe()
    #print("Head is:\n" flights_df.head())
    #print("Tail is:\n" flights_df.tail())
