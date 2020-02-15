import json
#Data Sources
#	Save these out manually for now.
#	~The Flights which are displayed
#https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/active/2020-02-08Z
#	~Flights which are not displayed
#https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/inactive/2020-02-08Z

#Load Data
def load_data():
	with open('2020-02-14Z.json') as json_file:
		raw_data = json.load(json_file)
	return raw_data

def extract_flight_list(raw_data):
	raw_flights = raw_data['flightSummaryList']['flight'] #< the flightsList
	return raw_flights


if __name__ == '__main__':
	raw_data = load_data()
	raw_flights = extract_flight_list(raw_data)

	#Print First Flight
	flight = raw_flights[0]
	print("Raw Payload of first Flight: \n", flight);

	#Extract & Print key info
	flightID = flight['flightIdentifier']
	departureTime = flight['origin']['status']['messages']['message'][0]['data']
	scheduledTime = flight['origin']['scheduledDateTime']['local']

	print("\n FlightID: " + flightID + "\n Departure Time:" + departureTime + "\n Scheduled Time: " + scheduledTime)
