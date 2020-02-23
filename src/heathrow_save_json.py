from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import requests
import sys

def getHtmlSoup(url_to_scrape):
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def saveJson(soup, fileName):
    json_data = json.loads(str(soup))
    with open(fileName, 'w') as f:
        json.dump(json_data, f)
        #f.write(myList)

def saveHtml(soup, fileName):
	with open(fileName, "w", encoding='utf-8') as file:
    		file.write(str(soup))


if __name__ == "__main__":

    #Select Date Range
    last_date = datetime.today().date()-timedelta(days=1) #Or datetime(2020, 2,24)
    first_date =  last_date-timedelta(days=7) 
    delta = last_date - (first_date - timedelta(days=1))
    number_of_days = delta.days

    #Ask User to Confirm
    print("First date will be: ", first_date.isoformat())
    print("Last date will be: ", last_date.isoformat())
    choice = input("Type ACCEPT to continue:")
    if choice != "ACCEPT":
        sys.exit("\nEXIT user did not want to continue.\n")

    date = first_date
    for i in range(0, number_of_days):
        file_name = date.strftime('%Y-%m-%d') + 'Z'
        file_path = ""#./data/heathrow_data/"
        full_file_name = file_path + file_name + ".json"

        url_root = 'https://api-dp-prod.dp.heathrow.com/infohub/api/v1/flights/departures/inactive/'
        url = url_root + file_name
        soup = getHtmlSoup(url)
        saveJson(soup, full_file_name)
        print("File saved for", date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)
