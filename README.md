## Broken Datasource Alert:
The default datasource no longer works.

The heathrow website has changed and `heathrow_parsing.py` is out of date.

The generic flight parsing could be useful for another airport. You would need to write something similar to `heathrow_parsing.py` for it.

# Flight Tables: Arrivals and Departures Parsing Toolkit
## What is It?

**Flight Tables** lets you save public Arrivals and Departures infomation to a standardised CSV file.  

Current version is for Heathrow Airport.

## Installation
```
$ pip install flight_tables
```

## Command Line Execution
Save yesterday's Arrivals and Departures to CSV:
```
python -m flight_tables.main
```
If you want to specify a date, add "yyyy-mm-dd" to the command. It will only work for the past few days, where data is still available from the airport API.

## Script Execution
Run the script below, but replace "yyyy-mm-dd" with the date you want. It will only work for the past few days, where data is still available from the airport API.
```         
from flight_tables.flight_tables import FlightTables

# Save Arrivals CSV
FlightTables.arrivals_csv("yyyy-mm-dd")

# Save Departures CSV
FlightTables.departures_csv("yyyy-mm-dd")
```

## CSV Output Format
The output is a csv with these columns:

| flight_id | origin | destination |   status  | scheduled_datetime |  actual_datetime | delay_mins | code_share |
|:---------:|:------:|:-----------:|:---------:|:------------------:|:----------------:|:----------:|:----------:|
|   BA028   |   HKG  |     LHR     |   Landed  |  03/04/2020 05:30  | 03/04/2020 05:39 |      9     |     No     |
|   VA5341  |   HKG  |     LHR     |   Landed  |  03/04/2020 05:30  | 03/04/2020 05:29 |     -1     |  Alt-Code  |
|   BA064   |   NBO  |     LHR     | Cancelled |  03/04/2020 06:20  |                  |            |  Main-Code |
|    ...    |        |             |           |                    |                  |            |            |

Output is saved to your working directory.

## Test Suite
Documentation [here](https://github.com/FergM/flight_tables/blob/master/docs/unit_tests.md)

## Background:
The initial motivation was to analyse flight punctuality. When you google for this most results are not detailed enough to compare one flight ID against another.
