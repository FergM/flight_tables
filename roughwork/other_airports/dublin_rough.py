#---------------Flights to check
# FR 288
# 18:55 to stansted
#
# EI0184
# 20:10 to LHR
#------------------------------


from datetime import datetime
import json


def loadJson(fileName):    
	with open(fileName) as f:
		payload = json.load(f)
	return payload

payload = loadJson("DublinArrivals.json")

#-------------------------------Filter for One Flight at a time:

print("---------------First Flight")
flightOneData = []
flightTwoData = []

for item in payload:
	if item['FlightIdentity'] == "EI184":
		print("found EI0184")
		print("DateTime is: ", item["ScheduledDateTime"])		
		flightOneData.append(item)

flightOneData = flightOneData[1:] #hack to match both flights

print("---------------Second Flight")
for item in payload:
	if item['FlightIdentity'] == "FR288":
		print("Found FR288")
		print("DateTime is: ", item["ScheduledDateTime"])		
		flightTwoData.append(item)

#-----------------Now we have two flight payloads separately
#But they're only showing 2 & 3 datapoints, & for the future so can't calc the delay...

def getDelayList(flightObjectList):
	delayList = []

	for flight in flightObjectList:
		print(flight)
		print(flight['ActualOffBlocksDateTime'])
		actual = datetime.strptime(flight['ActualOffBlocksDateTime'], "%Y-%m-%dT%H:%M:%S")
		planned = datetime.strptime(flight['ScheduledDateTime'], "%Y-%m-%dT%H:%M:%S")
		delay = actual - planned
		delayList.append(delay)
	
	return delayList

#print(getDelayList(flightOneData))

#Next steps:
#	would need to ..., just do simple plot comparing two flights just departed
#		https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
#		https://stackoverflow.com/questions/14270391/python-matplotlib-multiple-bars
#	THEN:
#		Do out the existing delays by airline, and how do they bunch around 15 min mark.
#	Later: schedule to gather data into a database every night (AWS?)
#	Revisit after 1 week's data collected (can verify vs punctuality websites)
#
#---------------------Get Departing flights with Actual Departure value:
departedFlights = []

for flight in payload:
	if flight['ActualOffBlocksDateTime'] != None:
		departedFlights.append(flight)

delayList = []
for flight in departedFlights:
	actual = datetime.strptime(flight['ActualOffBlocksDateTime'], "%Y-%m-%dT%H:%M:%S")
	planned = datetime.strptime(flight['ScheduledDateTime'], "%Y-%m-%dT%H:%M:%S")
	if actual > planned: 
		delay = actual - planned
		delay = delay.seconds/60
		print("Delay in Minutes: ", delay)

	else:
		delay = planned - actual
		delay = delay.seconds/60
		delay = delay*-1
		print("Delay in Minutes:", delay)
	delayList.append(delay)
	
#-------------------------#
print("list length = ", len(delayList))

delayList = sorted(delayList)

for delay in delayList:
	print(delay)
