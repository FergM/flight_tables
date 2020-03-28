from os import listdir
import pandas as pd
import pickle

from heathrow_parsing import ParsedFlights
from date_to_dict import fetch_heathrow_data

def dict_to_dataframe(heathrow_data):

    heathrow_df = pd.DataFrame()

	raw_flights = heathrow_data['flightSummaryList']['flight']

    #Parse Flights
    parsed_flights = ParsedFlights(raw_flights)
    heathrow_df = parsed_flights.to_dataframe()

    return heathrow_df

if __name__=="__main__":
    iso_date_str = "2020-03-20"
    direction = "departures"
    heathrow_data = fetch_heathrow_data(iso_date_str, direction)

    heathrow_df = dict_to_dataframe(heathrow_data)

    print("Last lines:\n", heathrow_df.tail(5))
