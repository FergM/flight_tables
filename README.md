# FlightTimes

Fetch Heathrow Arrivals/Departures Data and save to CSV.

## Instructions
Data is saved to your working directory. You will be asked to confirm before saving.

It will only work for recent dates because data is fetched from Heathrow's website.  

### CSV Format
The csv output currently has these column names, in addition to the index column:
* flight_id	
* scheduled_datetime	
* departure_datetime	
* delay_mins
* status

#### Basic Example
Run the following in command line:
```
python src/heathrow_flight_tables.py
```
This will output `heathrow_arrivals_yyyy-mm-dd.csv`, a file which contains all arrivals for yesterday.

#### Command line Execution
        * `python src/heathrow_flight_tables.py yyyy-mm-dd direction`
        * where `direction` is one of:
            * arrivals
            * departures
   
#### Python Execution
* From `src/heathrow_fligh_tables.py` import `HeathrowFlightTables`:
        ```         
           # Save Arrivals CSV
           HeathrowFlightTables.arrivals_csv("yyyy-mm-dd")
           
           # Save Departures csv
           HeathrowFlightTables.departures_csv("yyyy-mm-dd")
        ```

## Motivation:
The initial motivation was around analysing flight punctuality. When you google for this most results are not detailed enough to compare one flight IDs against another. One use case for this tool is to find airlines/flight times which are less delayed.
