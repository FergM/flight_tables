# WIP Notes
Notes about work in progress and possible improvements.

# Future Development Ideas
* Resolve known bugs
* Parsing option to choose API or json source
* Table Columns: check if there's a neater way to add new ones.

# Manual Validation of CSV Table
## Part 1: finding Duplicates
* filter by actual time
    * If actual time & scheduled time & origin/destination are the same, flag this.
* add origin and destination airport to help find if there's any true duplicates.

## Part 2
* Basically, split into Marketing, Operating and Normal
    * Cross check using vlookup on origin, from and to time
* check1: check cancelled don't duplicate (order by scheduled)
* check2: check landed don't duplicate (order by landed time)
* check3: check codeshares marketing all have a match vlookup from marketing flights to non marketing flights.
* check4: Reverse check that flights in today's Normal aren't elsewhere and Operating is mapped once to Codeshare at least.

# Known Bugs
*  Day Overlap Bug: 
    * **Summary**: Date could be wrong if data overlaps two days.
    * Heathrow
    * Status time is past midnight but flight landed on day intended
    * Landing date will be wrong

* Returning Departures:
    * **Summary**: Some departures return to airport in exceptional circumstances. I haven't tested handling of this.
    * A Heathrow departure that returned to Heathrow instead of Nairobi. Shows up in heathrow arrivals payload.
    * Origin Equals Destination
    * 2020-03-27 flight MH004 showing status time instead of landed time
    * Found 2020-03-28@17:15
    * Should have a test that feeds a flight and validates each field in table is right.
    * make test against commit c74b7d1 to ensure it fails.
   
   ```
   {
      "flightIdentifier":"BA065",
      "icaoCallsign":"BAW65R",
      "flightNumber":"65",
      "airlineIataRef":"BA",
      "origin":{
         "airportIataRef":"LHR",
         "terminalCode":"3",
         "status":{
            "interpretedStatus":" Landed 12:15  ",
            "category":"INFO",
            "messages":{
               "message":[
                  {
                     "text":"Landed",
                     "data":"12:15"
                  },
                  {
                     "text":" "
                  }
               ]
            },
            "code":"LD",
            "statusTime":"2020-03-27T12:15:24.000Z"
         },
         "scheduledDateTime":{
            "utc":"2020-03-27T12:35:00.000",
            "local":"2020-03-27T12:35:00.000",
            "utcOffset":0
         }
      },
      "destination":{
         "airportIataRef":"LHR"
      },
      "stops":{
         "stop":[

         ],
         "count":0
      },
      "codeShareType":"CODESHARE_OPERATING_FLIGHT",
      "isHadacabCancelled":false
   }
   ```
# Toolkit Ideas
```
def load_json_file(full_file_name):
   with open(full_file_name) as json_file:
      py_obj = json.load(json_file)
   return py_obj
```
```
def df_to_csv: #IFF filename doesn't exist
   test whether this is really needed or happens anyways...
```