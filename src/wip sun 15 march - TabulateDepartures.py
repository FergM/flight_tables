date -> json

json -> dataframe

dataframe -> csv


Extra:
    solve for departures, arrivals, cancels
    + find "other"


--------------------------Code:
save_json.py


from heathrow_extraction import load_data, extract_flight_list
from heathrow_parsing import ParsedFlights

dataframe_pickle


--------------------------Part 1) json
    #Get Date from User
        #Assert ISO Date STR
    date = ...
    choice = input("Type ACCEPT to continue:")
    if choice != "ACCEPT":
        sys.exit("\nEXIT user did not want to continue.\n")
    
    file_name = date.strftime('%Y-%m-%d') + 'Z'
    file_path = ""#./data/heathrow_data/"
    full_file_name = file_path + file_name + ".json"

    url_root = 'https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/inactive/'
    url = url_root + file_name
    soup = getHtmlSoup(url)
    #saveJson(soup, full_file_name)
    #print("File saved for", date.strftime('%Y-%m-%d'))

--------------------------Part 2) Parse the Json to Dataframe...

#Setup
from os import listdir
import pandas as pd
import pickle

from heathrow_extraction import load_data, extract_flight_list
from heathrow_parsing import ParsedFlights

heathrow_df = pd.DataFrame()
#----------------------------------Append Everything
dir_path = "../data/heathrow_data/"
    
path = dir_path + file

#Extract Raw Data
raw_flights = extract_flight_list(soup)
#Parse Flights
parsed_flights = ParsedFlights(raw_flights)
flights_df = parsed_flights.to_dataframe()
#Append
heathrow_df.append(flights_df)
print("Last line is:\n", heathrow_df.tail(1))

#----------------------------------Pickle
print("\nHead is:\n", heathrow_df.head())
print("Tail is:\n", heathrow_df.tail())

file_name = "heathrow_draft" + date + ".csv" #add date to filename

with open( file_name, "wb" ) as f:
    heathrow_df.to_csv(f)

with open(file_name, "rb") as f2:
    loaded_df = pd.read_csv.load(f2)

print("\nLoaded Head is:\n", loaded_df.head())
print("Loaded Tail is:\n", loaded_df.tail())
print("\n\n")


-------------------------final Call
TabulateDepartures(iso_date_str)
TabulateArrivals(iso_date_str)
"""
Saves csv table of arrivals data on selected date to working directory.
    Inputs: iso_date_str, the yyyy-mm-dd date you want to get data for
    Output: file_path = path to file which was saved. Returns "No Data for this Date" if not found.
"""