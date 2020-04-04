from datetime import datetime

def extract_batch_heathrow(response):
    batch_info = [] # List with `flight_info` from multiple flights

    raw_flights = response['flightSummaryList']['flight']   

    for flight in raw_flights:
        flight_info = extract_flight_heathrow(flight)
        batch_info.append(flight_info) 

    return batch_info

def extract_flight_heathrow(raw_flight):
    #Input:
    #   raw_flight (dict): Dictionary for a single flight, pulled from the raw response.
    #Output:
    #   flight_info (dict): Dictionary with key information for the flight.

    assert type(raw_flight) == dict
    #Initialise empty dataframe
    flight_info = {'flight_id': None,
                   'origin': None,
                   'destination': None,
                   'status': None,
                   'scheduled_datetime': None,
                   'actual_datetime': None,
                   'code_share_type': None}

    flight_info["flight_id"] = raw_flight['flightIdentifier']

    # Get Origin and Destination
    flight_info["origin"] = raw_flight['origin']['airportIataRef']
    flight_info["destination"] = raw_flight['destination']['airportIataRef']

    # Get Status and Location
    try:
        status = raw_flight['origin']['status']['messages']['message'][0]['text']
        location = 'origin'
    except:
        status = raw_flight['destination']['status']['messages']['message'][0]['text']
        location = 'destination'

    # Get Scheduled Time
    scheduled_time_str = raw_flight[location]['scheduledDateTime']['local']
    flight_info["scheduled_datetime"] = datetime.strptime(scheduled_time_str[:-7], "%Y-%m-%dT%H:%M")

    # Assign Status
    flight_info["status"] = status

    # Assign Actual Time
    if status == "Cancelled":
        flight_info["status"] = "Cancelled"
    elif (status == "Departed") or (status=="Landed"):
        actual_date_str = raw_flight[location]['status']['statusTime'][0:11]
        actual_time_str = raw_flight[location]['status']['messages']['message'][0]['data']
        actual_datetime_str = actual_date_str + actual_time_str
        flight_info["actual_datetime"] = datetime.strptime(actual_datetime_str, "%Y-%m-%dT%H:%M")
    else:
        flight_info["status"] = f"Unexpected Status: {status}" # ToDo: Handle this better?

    # Assign code_share_type
    flight_info["code_share_type"] = raw_flight["codeShareType"]

    return flight_info