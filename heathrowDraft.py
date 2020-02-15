import json
#Data Sources
#	Save these out manually for now.
#	~The Flights which are displayed
#https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/inactive/2020-02-08Z
#	~Flights which are not displayed
#https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/active/2020-02-08Z

#Load Data
with open('2020-02-14Z.json') as json_file: 
	data = json.load(json_file)

flightsList = data['flightSummaryList']['flight'] #< the flightsList

#Print First Flight
flight = data['flightSummaryList']['flight'][0]
print("Raw Payload of first Flight: \n", flight);

#Extract & Print key info 
flightID = flight['flightIdentifier']
departureTime = flight['origin']['status']['messages']['message'][0]['data']
scheduledTime = flight['origin']['scheduledDateTime']['local']

print("\n FlightID: " + flightID + "\n Departure Time:" + departureTime + "\n Scheduled Time: " + scheduledTime)
