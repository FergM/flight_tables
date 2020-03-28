# Validating this approach
* Is it ok to keep adding columns like this?
    * Consider clearer labelling / replace labels in codeshare column with simpler. 
    * e.g. AltID, MainID, OnlyID

# finding Duplicates
* filter by actual time
    * If actual time & scheduled time & origin/destination are the same, flag this.
* add origin and destination airport to help find if there's any true duplicates.

# Changes for Other Branches
* Change accept to Y/y like "rm -i" does

# CSV Table Validation
* Basically, split into Marketing, Operating and Normal
    * Cross check using vlookup on origin, from and to time
* check1: check cancelled don't duplicate (order by scheduled)
* check2: check landed don't duplicate (order by landed time)
* check3: check codeshares marketing all have a match vlookup from marketing flights to non marketing flights.
* check4: Reverse check that flights in today's Normal aren't elsewhere and Operating is mapped once to Codeshare at least.

# Corner Case
* Potential bug if status time is 1past midnight but flight landed on day intended.

# Errors
* Basic Validation Fail:
    * 2020-03-27 flight MH004 showing status time instead of landed time
    * Found 2020-03-28@17:15
    * Should have a test that feeds a flight and validates each field in table is right.
    * make test against commit c74b7d1 to ensure it fails.
   
# Corner Case Code:
# Origin Equals Destination
A Heathrow departure that returned to Heathrow instead of Nairobi. Shows up in heathrow arrivals payload.

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