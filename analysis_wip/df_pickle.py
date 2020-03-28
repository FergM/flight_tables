from os import listdir
import pandas as pd
import pickle

from heathrow_parsing import ParsedFlights

def load_json_file(full_file_name):
    with open(full_file_name) as json_file:
        py_obj = json.load(json_file)
    return py_obj

heathrow_df = pd.DataFrame()
print("\nempty df is:", heathrow_df)

#----------------------------------Append Everything

dir_path = "../data/heathrow_data/"
filenames = [item for item in listdir(dir_path) if item[-6:]=="Z.json"]
filenames.sort() # To avoid ambiguity.
print("Filenames are:\n\t", filenames)

for file in filenames:
    path = dir_path + file

    #Extract Raw Data
    raw_data = load_json_file(path)
   	raw_flights = raw_data['flightSummaryList']['flight']
    #Parse Flights
    parsed_flights = ParsedFlights(raw_flights)
    flights_df = parsed_flights.to_dataframe()
    #Append
    heathrow_df = heathrow_df.append(flights_df)
    print("Last line is:\n", heathrow_df.tail(1))

#----------------------------------Pickle
print("\nHead is:\n", heathrow_df.head())
print("Tail is:\n", heathrow_df.tail())

file_name = "heathrow_draft.p"

with open( file_name, "wb" ) as f:
    pickle.dump( heathrow_df, f)

with open(file_name, "rb") as f2:
    loaded_df = pickle.load(f2)

print("\nLoaded Head is:\n", loaded_df.head())
print("Loaded Tail is:\n", loaded_df.tail())
print("\n\n")