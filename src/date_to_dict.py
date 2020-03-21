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

if __name__=="__main__":
    iso_date_str = "2020-03-20"
    direction = "arrivals"

    json_data_raw = fetch_heathrow_data(iso_date_str, direction)
    print("\nOutput Length:", len(json_data_raw['flightSummaryList']['flight']), "characters")
    print("Sample content: \n\t", (str(json_data_raw['flightSummaryList']['flight']))[0:800])
