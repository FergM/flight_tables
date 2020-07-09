import datetime
import json
import sys

from bs4 import BeautifulSoup
import pandas as pd
import requests

def saveJson(soup, fileName):
    json_data = json.loads(str(soup))
    with open(fileName, 'w') as f:
        json.dump(json_data, f)

def saveHtml(soup, fileName):
	with open(fileName, "w", encoding='utf-8') as file:
    		file.write(str(soup))

def manualConfirmDates(first_date, last_date):
    """Ask User to Confirm request Dates
    
    Break and exit if not confirmed.
    """
    print("First date will be: ", first_date.isoformat())
    print("Last date will be: ", last_date.isoformat())
    print(f"Direction = {direction}")
    choice = input("Type y to continue:")
    if choice != "y":
        sys.exit("\nEXIT user did not want to continue.\n")

# String Mapping
## Used to determine the pihub endpoint url
direction_order_by = {'arrivals':'localArrivalTime', 'departures': 'localDepartureTime'}

# Request Headers 
request_headers = {"origin": "https://www.heathrow.com",}

if __name__ == "__main__":
    """Ping heathrow endpoint and save arrivals/departures as json.
    
    Parameters:
        sys.argv[1] (str): Flight direction, either 'arrivals' or 'departures'.
        sys.argv[2] (str): API endpoint name, either 'infohub' or 'pihub'.
    Returns:
        Success:
            .json (file): Json file with flight data. Saved to working directory.
        Fail:
            Prints message with error status code.
    """
    # Set Flight Direction
    try:
        direction = sys.argv[1]
        assert (direction == "arrivals") or (direction == "departures"), f"Direction parameter {direction} is not valid."
    except:
        print("Direction parameter not specified. Assume `direction = arrivals`")
        direction = "arrivals"

    # Determine Endpoint
    try:
        endpoint = sys.argv[2]
        assert (endpoint == "infohub") or (endpoint == "pihub"), f"endpoint parameter {endpoint} is not valid."
    except:
        raise Exception("Error. API endpoint parameter not specified.\n")

    #Select Dates
    number_of_days = 4
    last_date = datetime.date.today()-datetime.timedelta(days=1) # Yesterday
    dates = pd.date_range(end=last_date, periods=number_of_days).date
    ## confirm dates
    manualConfirmDates(dates[0], dates[-1])

    # Save Response for Each Date
    for date in dates:

        # Date string
        iso_date_str = date.isoformat()

        # Send Request
        ## Prepare Request URL
        if endpoint == "infohub":
            url = f'https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/{direction}/inactive/{iso_date_str}Z'
        elif endpoint == "pihub":
            url = f'https://api-dp-prod.dp.heathrow.com/pihub/flights/{direction}?date={iso_date_str}&orderBy={direction_order_by[direction]}'
        else:
            print(f"Endpoing name {endpoint} with status code {r.status_code}.")
        ## Send Request
        r = requests.get(url, headers = request_headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Save Response
        if r.status_code == 200:
            ## Determine Output File Name
            output_file_name = f'heathrow_{direction}_{iso_date_str}.json'
            ## Save Output as JSON File
            saveJson(soup, output_file_name)
            print("File saved for", iso_date_str)
        else:
            print(f"Failed for {iso_date_str} with status code {r.status_code}.")