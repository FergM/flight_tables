"""
1) initialise dataframe

2) Create Append everything
for day in dataFiles:
    makeDayDataframe
    dataframe.append() it

3) save dataframe as pickle
"""
#----------------------------------initialise
import pandas as pd

mydf = pd.DataFrame()
print("\nempty df is:", mydf)
#----------------------------------Append Everything
#2.2) need to add a for loop
from os import listdir

filenames = [item for item in listdir("../data/heathrow_data/") if item[-6:]=="Z.json"]
print("Filenames are:\n\t", filenames)

#2.1) simplify heathrow parsing and use it to create dataframe
    #Select File
from heathrow_extraction import load_data, extract_flight_list
from heathrow_parsing import ParsedFlights

full_file_name = "../data/heathrow_data/2020-02-02Z.json"

#Extract Raw Data
raw_data = load_data(full_file_name)
raw_flights = extract_flight_list(raw_data)

#Parse Flights
parsed_flights = ParsedFlights(raw_flights)
flights_df = parsed_flights.to_dataframe()

print("\nempty df is:", mydf)
mydf = mydf.append(flights_df)
print("\nempty df.head() is NOW:\n", mydf.head(), "\n\n")

#----------------------------------Pickle
import pickle

var1 = ["This is a hello world string."]
var2 = ["empty"]
file_name = "myPickle.p"

print("Var1:", var1)
print("Var2:", var2)

with open( file_name, "wb" ) as f:
    pickle.dump( var1, f)

with open(file_name, "rb") as f2:
    var2 = pickle.load(f2)

print("Var1:", var1)
print("Var2:", var2)