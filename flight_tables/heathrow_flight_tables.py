from datetime import datetime, timedelta
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
    print("\nStart")

    direction = "arrivals" #Assume arrivals unless specified later as an argument.

    if len(sys.argv) == 1:
        yesterday = datetime.today().date()-timedelta(days=1)
        date_str = yesterday.isoformat()
        print(f"\nDirection not specified. \n\tAssume: Yesterday's {direction}")
    elif len(sys.argv) == 2:
        date_str = sys.argv[1]
    elif len(sys.argv) == 3:
        date_str = sys.argv[1]
        direction = sys.argv[2]
    else:
        sys.exit(f"\n Failed because Too many Arguments. Expected 2 or less, received {len(sys.argv)}.")

    #Ask User to Confirm
    print("\nUSER CONFIRMATION REQUIRED:")
    print("Computer will fetch data from Heathrow's website and save it to your working directory as CSV.")
    print("* Date: ", date_str)
    print("* Direction: ", direction)
    choice = input("Type ACCEPT to continue: ")
    if choice != "ACCEPT":
        sys.exit("\nEXIT. User did not want to continue.\n")

    print("\n")
    if direction=="arrivals":
        HeathrowFlightTables.arrivals_csv(date_str)
    if direction=="departures":
        HeathrowFlightTables.departures_csv(date_str)

    print("\nEnd")