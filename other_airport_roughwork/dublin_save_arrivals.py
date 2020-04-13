import ast
from bs4 import BeautifulSoup
import json
import re
import requests

#----------------------------------About:
#Takes arrivals data from dublin airport website and Saves
#it in json format to my working directory.

def getHtmlSoup(url_to_scrape):
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def extractPayload(html_str):
    #Regular Expression reminder:
    #"." matches any character except a newline.
    #"*" to match 0 or more repetitions of the preceding RE
    regex = re.compile(r'(var jsonFlightList =)(\[.*\])')
    firstMatch = regex.findall(html_str)[0]
    payloadStr = firstMatch[1]
    payloadList = json.loads(payloadStr)
    return payloadList

def getFlightList(url_to_scrape):
    soup = getHtmlSoup(url_to_scrape)
    html_str = str(soup)
    payload = extractPayload(html_str)
    return(payload)

def saveListAsJson(myList, fileName):
    with open(fileName, 'w') as f:
        json.dump(myList, f)
        #f.write(myList)

if __name__ == "__main__":
    url_to_scrape = 'https://www.dublinairport.com/flight-information/live-departures'

    flightList = getFlightList(url_to_scrape)

    saveListAsJson(flightList, 'DublinArrivals.json')

#-------------------------------WIP
#Conform to Naming Conventions for variables, functions...
#Make this test driven development
#Use Below functions for ideas
def filterFlightID(flightList, flightId):
    """Filters for a given flightID""" 

def selectDateRange(flightList, startDate, endDate):
    """Selects trades between start (inclusive of) and end date (exclusive of)."""
    #Can make endDate an optional argument. If not provided startDate = endDate.
    return None

def printOrigins(table_data):
    for flight in table_data[:10]:
        Origin = flight['Origin']
        print(Origin)

def printAirlines(table_data):
    for flight in table_data[:10]:
        Origin = flight['Airline']
        print(Origin)