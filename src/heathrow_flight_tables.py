from date_to_dict import fetch_heathrow_data
from dict_to_dataframe import dict_to_dataframe
from dataframe_to_csv import df_to_csv
import pandas as pd

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
    #from heathrow_flight_tables import HeathrowFlightTables
    print("start")
    HeathrowFlightTables.arrivals_csv("2020-03-26")
    print("end")