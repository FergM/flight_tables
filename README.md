# FlightTimes

Fetch Heathrow Arrivals/Departures Data and save to CSV. 
* One day at a time.
* One Direction at a time (arrivals or departures)

Data is saved to your working directory. You will be asked to confirm before saving.

It will only work for recent dates because data is fetched from Heathrow's website.  

## Instructions

#### Basic Example
Run the following in command line:
```
python src/heathrow_flight_tables.py
```
This will output `heathrow_arrivals_yyyy-mm-dd.csv`, a file which contains all arrivals for yesterday.

#### Command line Execution
* First argument is date you want
* Second argument is `departures` or `arrivals`
```
python src/heathrow_flight_tables.py yyyy-mm-dd departures
```  
   
#### Python Execution
* From `src/heathrow_fligh_tables.py` import `HeathrowFlightTables`:  
```         
# Save Arrivals CSV
HeathrowFlightTables.arrivals_csv("yyyy-mm-dd")

# Save Departures csv
HeathrowFlightTables.departures_csv("yyyy-mm-dd")
```

## Output Format
The output is a csv these column names; in addition to the index column:
* flight_id
* scheduled_datetime
* departure_datetime
* delay_mins
* status

## Motivation:
The initial motivation was around analysing flight punctuality. When you google for this most results are not detailed enough to compare one flight IDs against another. One use case for this tool is to find airlines/flight times which are less delayed.
