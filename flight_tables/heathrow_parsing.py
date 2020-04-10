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
        file_path = ""#./data/heathrow_data/"
        file_name = iso_date_str + 'Z'
        full_file_name = file_path + file_name + ".json"
        url_root = 'https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/' + direction + '/inactive/'
        url = url_root + file_name
        return url

    def fetch_html_soup(url_to_scrape):
        r = requests.get(url_to_scrape)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def soup_to_dict(soup, iso_date_str):
        return json.loads(str(soup))

    check_date_format(iso_date_str)
    url = make_url(iso_date_str, direction)
    soup = fetch_html_soup(url)
    heathrow_data = json.loads(str(soup))

    return heathrow_data

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

def extract_batch_heathrow(response):
    batch_info = [] # List with `flight_info` from multiple flights

    raw_flights = response['flightSummaryList']['flight']   

    for flight in raw_flights:
        flight_info = extract_flight_heathrow(flight)
        batch_info.append(flight_info) 

    return batch_info