import pandas as pd
import sys

from dataframe_to_csv import df_to_csv
from date_to_dict import fetch_heathrow_data
from dict_to_dataframe import dict_to_dataframe

class HeathrowFlightTables(object):
    @classmethod
    def arrivals_csv(cls, iso_date_str):
        cls.date_to_csv(iso_date_str, "arrivals")

    @classmethod
    def departures_csv(cls, iso_date_str):
        cls.date_to_csv(iso_date_str, "departures")
    
    @staticmethod
    def date_to_csv(iso_date_str, direction):
        file_name = f"heathrow_{direction}_{iso_date_str}.csv"
        heathrow_raw_dict = fetch_heathrow_data(iso_date_str, direction)
        #heathrow_payload_dict = heathrow_raw_dict['flightSummaryList']['flight']
        heathrow_df = dict_to_dataframe(heathrow_raw_dict)
        df_to_csv(heathrow_df, file_name)

    @staticmethod
    def csv_to_df(file_name):
        with open( file_name, "r" ) as f:
            df = pd.read_csv(file_name)
        return df

if __name__=="__main__":
    print("start")

    direction = "arrivals" #Assume arrivals unless specified later as an argument.

    print(sys.argv)
    if len(sys.argv) == 1:
        date_str = "2020-03-26"
        print(f"Direction not specified. Assume: {direction}")
    elif len(sys.argv) == 2:
        date_str = sys.argv[1]
    elif len(sys.argv) == 3:
        date_str = sys.argv[1]
        direction = sys.argv[2]
    else:
        Print("Too Many Arguments. You can include 'yyyy-mm-dd' and 'arrivals' or 'departures' as second and third arguments.")
        sys.exit(f"Too Many Arguments. Expected 2 or less, received {len(sys.argv)}.")

    if direction=="arrivals":
        HeathrowFlightTables.arrivals_csv(date_str)
    if direction=="departures":
        HeathrowFlightTables.departures_csv(date_str)

    print("End")