#---------------Flights to check
# FR 288
# 18:55 to stansted
#
# EI0184
# 20:10 to LHR

#-----------------------------
from datetime import date
import json

def loadJson(fileName):    
	with open(fileName) as f:
		payload = json.load(f)
	return payload


#------------------------------
#INPUTS

flight_str = "EK162"#"FR288" #"EI184"
date_str = date.isoformat(date.today()) #"2020-02-04"

payload = loadJson("DublinArrivals.json")

#-------------------------------Filter for One Flight at a time:

print("---------------First Flight")
flightOneData = []
todaysFlights = []

for flight in payload:
	if flight['FlightIdentity'] == flight_str:
		print("\n\nfound", flight_str)
		print("DateTime is: ", flight["ScheduledDateTime"])
		#print(flight['ScheduledDateTime'][:10])
		print("All Info: \n", flight, "\n\n")		
		flightOneData.append(flight)


#------------------------------Todays Flights
def getTodaysFlights(flight_data, date_str): 
	for flight in payload:
		if flight['ScheduledDateTime'][:10] == date_str:
			todaysFlights.append(flight)
	return todaysFlights

todaysFlights = getTodaysFlights(payload,date_str)

print("There are ", len(todaysFlights), " flights showing for today")



def getGate(flight_data, flight_str): 
	for flight in flight_data:
		if flight['FlightIdentity'] == flight_str:
			return flight['Gate']
			break
		else:
			None
			#print(flight['FlightIdentity'])
			#print(flight_str)
	return "Gate Not Found"


print("The gate for flight", flight_str, "on", date_str, "is:", getGate(todaysFlights, flight_str))