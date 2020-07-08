from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests
import sys

def fetch_heathrow_data(iso_date_str, direction):
    """
    Returns python object with data from Heathrow API.
    Inputs: 
        `iso_date_str` (str): YYYY-MM-DD format of the date for which you want data.
        `direction` (str): Specify whether you want "departures" or "arrivals"
    Outputs: 
        `heathrow_data` (dict);
            Successful = 
                * Python Dictionary with keys: ['header', 'flightSummaryList', 'references']
                * Payload is the list output['flightSummaryList']['flight']
                * Where each dictionary in the list represents a different flightID.
            Failure = 
                * Wrong Date will sys.exit("message")
    """
    def check_date_format(iso_date_str):
        """Exit if date is not an iso date string"""
        try:
            datetime.strptime(iso_date_str, '%Y-%m-%d')
        except ValueError as err:
            sys.exit(f"Invalid Date: {iso_date_str}. Required Format is YYYY-MM-DD")
        return iso_date_str

    def make_url(iso_date_str, direction):

        # String Mapping
        ## Used to get the required url string
        direction_order_by = {'arrivals':'localArrivalTime', 'departures': 'localDepartureTime'}

        # Flight Data Request pattern
        url = f'https://api-dp-prod.dp.heathrow.com/pihub/flights/{direction}?date={iso_date_str}&orderBy={direction_order_by[direction]}'

        return url

    def fetch_html_soup(url_to_scrape):
        headers={"origin": "https://www.heathrow.com"}
        r = requests.get(url_to_scrape, headers = headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def soup_to_dict(soup, iso_date_str):
        return json.loads(str(soup))

    check_date_format(iso_date_str)
    url = make_url(iso_date_str, direction)
    soup = fetch_html_soup(url)
    heathrow_data = json.loads(str(soup))

    return heathrow_data

def extract_flight_heathrow_pihub(raw_flight):
    """Parse a raw flight sourced from the pihub/ endpoint

    Input:
       raw_flight (dict): Dictionary for a single flight, pulled from the raw response.
    Output:
       flight_info (dict): Dictionary with key information for the flight.
    """
    assert type(raw_flight) == dict
    #Initialise empty dataframe
    flight_info = {'flight_id': None,
                   'origin': None,
                   'destination': None,
                   'status': None,
                   'scheduled_datetime': None,
                   'actual_datetime': None,
                   'code_share_type': None}

    flight_info["flight_id"] = raw_flight['flightService']['iataFlightIdentifier']

    # Get Origin and Destination
    flight_info["origin"] = raw_flight['flightService']['aircraftMovement']['route']['portsOfCall'][0]['airportFacility']['iataIdentifier']
    flight_info["destination"] = raw_flight['flightService']['aircraftMovement']['route']['portsOfCall'][1]['airportFacility']['iataIdentifier']

    # Get Status
    flight_info["status"] = raw_flight['flightService']['aircraftMovement']['aircraftMovementStatus'][0]['statusData'][0]['localisationKey']
    
    # Get Scheduled Time
    ## Get Direction (Arrival or Departure)
    direction_char = raw_flight['flightService']['arrivalOrDeparture']
    direction_char_dict = {'A':'Arrival','D':'Departure'}
    direction = direction_char_dict[direction_char]    
    ## Get Scheduled Time (Local BST Timezone)
    ### Assuming ORIGIN portsOfCall always comes first. 
    ##### For departures we need to look at the time associated with the origin.
    ##### For arrivals we need to look at the time associated with the destination.
    direction_bool_dict = {'Arrival':1,'Departure':0}
    direction_bool = direction_bool_dict[direction]    
    scheduled_time_str = raw_flight['flightService']['aircraftMovement']['route']['portsOfCall'][direction_bool]['operatingTimes']['scheduled']['local']
    flight_info["scheduled_datetime"] = datetime.strptime(scheduled_time_str, "%Y-%m-%dT%H:%M:%S")

    # Assign Actual Time
    status = flight_info['status']
    if status == "Cancelled":
        pass
    elif (status == "Departed") or (status=="Landed"):
        actual_time_str = raw_flight['flightService']['aircraftMovement']['aircraftMovementStatus'][0]['statusData'][0]['data']        
        actual_date_str = scheduled_time_str[0:11]
        actual_datetime_str = actual_date_str + actual_time_str
        flight_info["actual_datetime"] = datetime.strptime(actual_datetime_str, "%Y-%m-%dT%H:%M")
    else:
        flight_info["status"] = f"Unexpected Status: {status}" # ToDo: Handle this better?

    # Assign code_share_type
    def standardise_codeshare_name(old_name):
        raw_names = ["CODESHARE_MARKETING_FLIGHT", "CODESHARE_OPERATING_FLIGHT", "NORMAL_FLIGHT"]
        standardised_names = ["alt_code", "main_code", "no_codeshare"]
        name_mapping = dict(zip(raw_names, standardised_names))

        new_name = name_mapping[old_name]

        return new_name

    raw_codeshare_name = raw_flight['flightService']['codeShareStatus']
    flight_info["code_share_type"] = standardise_codeshare_name(raw_codeshare_name)

    return flight_info

def extract_batch_heathrow(response):
    batch_info = [] # List with `flight_info` from multiple flights

    raw_flights = response

    for flight in raw_flights:
        flight_info = extract_flight_heathrow_pihub(flight)
        batch_info.append(flight_info) 

    return batch_info