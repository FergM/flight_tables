from bs4 import BeautifulSoup
import re
import requests

def getHtmlSoup(url_to_scrape):
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parseFlightElement(element):
    flightDict = {}
    
    flightDict['date'] = element['data-flight_date']
    flightDict['scheduledArrival'] = element.find("td", class_="css-sta").string
    flightDict['flightNumber'] = element.find("td", class_="css-flightNumber").contents[-1].split()[-1] 
    #regex = re.compile(r'(var jsonFlightList =)(\[.*\])')
    #firstMatch = regex.findall(html_str)[0]
    
    flightDict['airline'] = element.find("td", class_="css-company").contents[-1] # use regex
    flightDict['arrivalStatus'] = element.find("td", class_="css-status").contents[-1] # e.g. " Landed 05:02         " #use regex

    return flightDict

#-------------Get Flights as Soup
url = "https://www.euroairport.com/en/passengers-visitors/arrivals-departures/flights/arrivals.html"
soup = getHtmlSoup(url)

table = soup.find("table", class_="flights-table")
flightListSoup = table.find_all("tr", class_="flights-primary-info")

#-------------Count Flights
flightCount = len(flightListSoup)
print("\nThere are", flightCount, "flights listed. \n")

#--------------First Flight
print("------First Flight is:", parseFlightElement(flightListSoup[0])['flightNumber'])
flightInfo = parseFlightElement(flightListSoup[0])
print(flightInfo)

#--------------Find A Flight
flightID = "W64dd323"

for flightSoup in flightListSoup:
    if flightSoup.find("td", class_="css-flightNumber").contents[-1].split()[-1]  == flightID:
        flightInfo = parseFlightElement(flightSoup)

        print("------Found Flight:", flightID)
        print("Details are:")
        print(flightInfo, "\n")
        break
