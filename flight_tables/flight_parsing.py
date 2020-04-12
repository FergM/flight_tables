from datetime import datetime
import numpy as np
import pandas as pd

class Flight(object):

    def __init__(self, flight_info):
        """
        Input:
            flight_info (dict)
        Attributes:
            The keys in `flight_info`:
                flight_id,
                origin,
                destination,
                status,
                scheduled_datetime,
                actual_datetime,
                code_share_type,
            Derived Attributes:
                delay_mins
        """
        expected_keys = {'flight_id',
                         'origin',
                         'destination',
                         'status',
                         'scheduled_datetime',
                         'actual_datetime',
                         'code_share_type'}

        assert flight_info.keys() == expected_keys, f"The input `flight_info` is missing these keys: {expected_keys-set(flight_info.keys())}"

        for k, v in flight_info.items():
            setattr(self, k, v)

        self.delay_mins = self.calculate_delay_minutes(self.scheduled_datetime, self.actual_datetime)

    @staticmethod
    def calculate_delay_minutes(scheduled_datetime, actual_datetime):
        if None in (scheduled_datetime, actual_datetime):
            return None
        else:
            delay_mins = (actual_datetime - scheduled_datetime).total_seconds() / 60
            return delay_mins

    def to_list(self):
        flight_info = [self.flight_id, self.origin, self.destination, self.status, self.scheduled_datetime, self.actual_datetime, self.delay_mins, self.code_share_type]
        return flight_info

    @staticmethod
    def labels():
        return ["flight_id", "origin", "destination", "status", "scheduled_datetime", "actual_datetime", "delay_mins", "code_share"]

class ParsedFlights(object):

    def __init__(self, batch_info):
        self.parsed_flights = []
        assert type(batch_info) == list
        for flight_info in batch_info:
            flight = Flight(flight_info)
            self.parsed_flights.append(flight)

    def to_dataframe(self):
        data = []
        for flight in self.parsed_flights:
            row_data = flight.to_list()
            data.append(row_data)
        df = pd.DataFrame(np.array(data), columns = Flight.labels())
        return df