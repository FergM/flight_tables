from datetime import datetime, timedelta
import pandas as pd
import sys

from heathrow_parsing import fetch_heathrow_data, extract_batch_heathrow
from flight_parsing import ParsedFlights

class HeathrowFlightTables(object):
    @classmethod
    def arrivals_csv(self, iso_date_str):
        self.date_to_csv(iso_date_str, "arrivals")

    @classmethod
    def departures_csv(self, iso_date_str):
        self.date_to_csv(iso_date_str, "departures")
    
    @staticmethod
    def date_to_csv(iso_date_str, direction):
        file_name = f"heathrow_{direction}_{iso_date_str}.csv"

        heathrow_raw_dict = fetch_heathrow_data(iso_date_str, direction)

        batch_info = extract_batch_heathrow(heathrow_raw_dict)

        parsed_flights = ParsedFlights(batch_info)

        heathrow_df = parsed_flights.to_dataframe()

        HeathrowFlightTables.df_to_csv(heathrow_df, file_name)

    @staticmethod
    def df_to_csv(df, file_name):
        with open( file_name, "x" ) as f:
            df.to_csv(file_name)

    @staticmethod
    def csv_to_df(file_name):
        with open( file_name, "r" ) as f:
            df = pd.read_csv(file_name)
        return df

if __name__=="__main__":
    date = datetime.today().date()-timedelta(days=1)
    date_str = date.isoformat()

    # Save Arrivals CSV
    HeathrowFlightTables.arrivals_csv(date_str)

    # Save Departures csv
    HeathrowFlightTables.departures_csv(date_str)