# Flight Tables: Arrivals and Departures Parsing Toolkit
## What is It?

**Flight Tables** lets you save public Arrivals and Departures infomation to a standardised csv file.  

Current version is for Heathrow Airport.

## Instructions
Install:
```
$ pip install flight_tables
```
Save CSV Files:
* Files are saved to your working directory. 

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

## Test Suite
Documentation [here](https://github.com/FergM/flight_tables/blob/master/docs/unit_tests.md)

## Background:
The initial motivation was to analyse flight punctuality. When you google for this most results are not detailed enough to compare one flight ID against another.