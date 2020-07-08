from bs4 import BeautifulSoup
import datetime
import json
import requests
import sys

def saveJson(soup, fileName):
    json_data = json.loads(str(soup))
    with open(fileName, 'w') as f:
        json.dump(json_data, f)
        #f.write(myList)

def saveHtml(soup, fileName):
	with open(fileName, "w", encoding='utf-8') as file:
    		file.write(str(soup))

# String Mapping
## Used to get the required url string
direction_order_by = {'arrivals':'localArrivalTime', 'departures': 'localDepartureTime'}

# Request Headers 
## Copied from Chrome DevTools XHR request
## Optional Cookie is removed
request_headers = {
"accept": "application/json, text/plain, */*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7,ga;q=0.6",
"origin": "https://www.heathrow.com",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-site",
"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}

if __name__ == "__main__":
    """Ping heathrow endpoint and save arrivals/departures as json.
    
    Parameters:
        sys.argv[1] (str): Flight direction, either 'arrivals' or 'departures'.
    Returns:
        Success:
            .json (file): Json file with flight data. Saved to working directory.
        Fail:
            Prints message with error status code.
    """
    # Set Flight Direction
    try:
        direction = sys.argv[1]
    except:
        print("Direction parameter not specified. Assume `direction = arrivals`")
        direction = "arrivals"

    #Select Date Range
    last_date = datetime.date.today()-datetime.timedelta(days=1) #Or datetime(2020, 2,24).date()
    first_date =  last_date-datetime.timedelta(days=4) 

    delta = last_date - first_date
    number_of_days = delta.days + 1

    #Ask User to Confirm
    print("First date will be: ", first_date.isoformat())
    print("Last date will be: ", last_date.isoformat())
    print(f"Direction = {direction}")
    choice = input("Type y to continue:")
    if choice != "y":
        sys.exit("\nEXIT user did not want to continue.\n")

    # Loop: Request & Save for Each Date
    date = first_date
    for i in range(0, number_of_days):
        # Date string
        iso_date_str = date.isoformat()

        # Request
        ## Prepare Request URL
        url = f'https://api-dp-prod.dp.heathrow.com/pihub/flights/{direction}?date={iso_date_str}&orderBy={direction_order_by[direction]}'
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

        # Increment the date
        date += datetime.timedelta(days=1)