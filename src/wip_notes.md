# CSV Pipeline
* date -> json
* json -> dataframe
* dataframe -> csv

## Implementation
fetch_heathrow_data
* date=>dict  

dict_to_dataframe
* dict=>df   

df_to_csv
* df=>csv

# CSV Callables
* TabulateDepartures(iso_date_str)
* TabulateArrivals(iso_date_str)
* OR
* HeathrowFlightTables.arrivals_csv(iso_date_str)
* HeathrowFlightTables.departures_csv(iso_date_str)
"""
Saves csv table of arrivals data on selected date to working directory.
    Inputs: iso_date_str, the yyyy-mm-dd date you want to get data for
    Output: file_path = path to file which was saved. Returns "No Data for this Date" if not found.
"""

## Cases to Solve
* Cancelled departures (TDD)
* Validate Departures CSV
* Arrivals  (TDD)
* Validate Arrivals CSV
* Extra
    * Handle mock "other" not departed/arrived and not cancelled.
* Create Package
    * Deploy sample Package
    * Tidy code
    * Deploy package

# Dependencies
* from heathrow_parsing import `ParsedFlights`
* from heathrow_extraction import extract_flight_list # load_data
    * Can be removed it's a oneliner

# Test Scripts
test_*.py
dataframe_to_csv.py

# Example Flights
## Cancelled Departures
{
   "flightIdentifier":"DL4339",
   "flightNumber":"4339",
   "airlineIataRef":"DL",
   "origin":{
      "airportIataRef":"LHR",
      "terminalCode":"3",
      "status":{
         "interpretedStatus":" Cancelled Contact airline",
         "category":"INFO",
         "messages":{
            "message":[
               {
                  "text":"Cancelled"
               },
               {
                  "text":"Contact airline"
               }
            ]
         },
         "code":"CX",
         "statusTime":"2020-03-25T07:00:00.000Z"
      },
      "scheduledDateTime":{
         "utc":"2020-03-25T07:00:00.000",
         "local":"2020-03-25T07:00:00.000",
         "utcOffset":0
      }
   },
   "destination":{
      "airportIataRef":"LOS"
   },
   "stops":{
      "stop":[

      ],
      "count":0
   },
   "codeShareType":"CODESHARE_MARKETING_FLIGHT",
   "isHadacabCancelled":true
}
## Arrival
{
   "flightIdentifier":"BA058",
   "icaoCallsign":"BAW58",
   "flightNumber":"58",
   "airlineIataRef":"BA",
   "origin":{
      "airportIataRef":"CPT"
   },
   "destination":{
      "airportIataRef":"LHR",
      "terminalCode":"3",
      "status":{
         "interpretedStatus":" Landed 04:31 Bags delivered on belt 08",
         "category":"INFO",
         "messages":{
            "message":[
               {
                  "text":"Landed",
                  "data":"04:31"
               },
               {
                  "text":"Bags delivered on belt",
                  "data":"08"
               }
            ]
         },
         "code":"LB",
         "statusTime":"2020-03-25T05:24:25.000Z"
      },
      "scheduledDateTime":{
         "utc":"2020-03-25T04:45:00.000",
         "local":"2020-03-25T04:45:00.000",
         "utcOffset":0
      }
   },
   "stops":{
      "stop":[

      ],
      "count":0
   },
   "codeShareType":"CODESHARE_OPERATING_FLIGHT",
   "isHadacabCancelled":false
}
## Cancelled Arrival
{
   "flightIdentifier":"BA078",
   "icaoCallsign":"BAW78",
   "flightNumber":"78",
   "airlineIataRef":"BA",
   "origin":{
      "airportIataRef":"ACC"
   },
   "destination":{
      "airportIataRef":"LHR",
      "terminalCode":"3",
      "status":{
         "interpretedStatus":" Cancelled Contact airline",
         "category":"INFO",
         "messages":{
            "message":[
               {
                  "text":"Cancelled"
               },
               {
                  "text":"Contact airline"
               }
            ]
         },
         "code":"CX",
         "statusTime":"2020-03-25T05:30:00.000Z"
      },
      "scheduledDateTime":{
         "utc":"2020-03-25T05:30:00.000",
         "local":"2020-03-25T05:30:00.000",
         "utcOffset":0
      }
   },
   "stops":{
      "stop":[

      ],
      "count":0
   },
   "codeShareType":"CODESHARE_OPERATING_FLIGHT",
   "isHadacabCancelled":false
}