#~Ones displayed
#https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/inactive/2020-02-08Z
#~Ones not displayed
#https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/active/2020-02-08Z
with open('2020-02-08Zinactive.json') as json_file: data = json.load(json_file)
#data.keys()
flightsList = data['flightSummaryList']['flight'] #< the flightsList
firstFlightDict = data['flightSummaryList']['flight'][0]