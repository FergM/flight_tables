date -> json

json -> dataframe

dataframe -> csv


Extra:
    solve for departures, arrivals, cancels
    + find "other"


-------------------------final Call
TabulateDepartures(iso_date_str)
TabulateArrivals(iso_date_str)
"""
Saves csv table of arrivals data on selected date to working directory.
    Inputs: iso_date_str, the yyyy-mm-dd date you want to get data for
    Output: file_path = path to file which was saved. Returns "No Data for this Date" if not found.
"""

HeathrowFlightTables.arrivals_csv(iso_date_str)
HeathrowFlightTables.departures_csv(iso_date_str)