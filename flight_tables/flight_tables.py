from datetime import datetime, timedelta
import pandas as pd
import sys

from flight_tables.heathrow_parsing import fetch_heathrow_data, extract_batch_heathrow
from flight_tables.flight_parsing import ParsedFlights

class FlightTables(object):
    """Class for saving Arrivals and Departures to csv"""
    @classmethod
    def arrivals_csv(self, iso_date_str):
        self.date_to_csv(iso_date_str, "arrivals")

    @classmethod
    def departures_csv(self, iso_date_str):
        self.date_to_csv(iso_date_str, "departures")
    
    @staticmethod
    def date_to_csv(iso_date_str, direction):
        """
        Saves csv table of data on selected date to working directory.
            Inputs:
                iso_date_str (str): The yyyy-mm-dd date you want to get data for
                direction (str): "arrivals" or "departures"
            Output:
                CSV table saved to working directory.
        """
        file_name = f"heathrow_{direction}_{iso_date_str}.csv"

        heathrow_raw_dict = fetch_heathrow_data(iso_date_str, direction)

        batch_info = extract_batch_heathrow(heathrow_raw_dict)

        parsed_flights = ParsedFlights(batch_info)

        heathrow_df = parsed_flights.to_dataframe()

        FlightTables.df_to_csv(heathrow_df, file_name)

    @staticmethod
    def df_to_csv(df, file_name):
        with open( file_name, "x" ) as f:
            df.to_csv(file_name)

    @staticmethod
    def csv_to_df(file_name):
        with open( file_name, "r" ) as f:
            df = pd.read_csv(file_name)
        return df