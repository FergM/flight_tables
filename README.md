# FlightTimes

Code to analyse flight arrivals and departures data.  

Current version is for Heathrow Airport only.  

## Instructions
Instructions for saving data from one day's departures to csv. This will only work for recent dates because data is fetched from heathrow's website.

#### CSV Format
The csv output currently has these column names, in addition to the index column:
* flight_id	
* scheduled_datetime	
* departure_datetime	
* delay_mins

### Save Departures as CSV

#### Basic Example
Run the following in command line:
```
python src/heathrow_flight_tables.py
```
This will output `heathrow_departures_2020-03-25.csv`, a file which contains all departures for March 25th.

#### Request your own Date
* From `heathrow_flight_tables.py` import `HeathrowFlightTables`.
* You can then execute ```HeathrowFlightTables.departures_csv("2020-03-25")``` to save a csv for the specified date.

## Motivation:
The initial motivation was around analysing flight punctuality. When you google for this most results are not detailed enough to compare one flight IDs against another. One use case for this tool is to find airlines/flight times which are less delayed.
