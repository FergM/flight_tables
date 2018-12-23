#GRABDUBLINARRIVALS.py takes arrivals data from dublin airport website and Saves
#it in json format to my working directory.

#----------------------------------Setup
import requests
from bs4 import BeautifulSoup
import json

url_to_scrape = 'https://www.dublinairport.com/flight-information/live-departures'

#----------------------------------Prepare Data
r = requests.get(url_to_scrape)

soup = BeautifulSoup(r.text, 'html.parser')
##print(soup.prettify())

#----------------------------------
table_data = [] #This is a list

table_body = soup.tbody.find_all('tr') #<tbody> is a selector/tag
#<tr> is also a selector/tag

for table_row in table_body: #For each thing in the table_body
    flight_data = {} #This is a dictionary

    flight_data['Origin'] = table_row.find_all('td')[1].text.strip() #The 1 here picks out Origin as the 1+1th data element in the row
    flight_data['Airline'] = table_row.find_all('td')[2].text.strip() #The 1 here picks out Origin as the 1+1th data element in the row

    table_data.append(flight_data)

#print(table_data[:10])#Print the things with <td> tag
    #The things we print here are ~ the data values from each row.

for flight in table_data[:10]:
    Origin = flight['Origin']
    print(Origin)

for flight in table_data[:10]:
    Origin = flight['Airline']
    print(Origin)

#Recap of the above
#   Each row from the website's table is a dictionary entry
#   table_data is a list of all the dictionary entries

#Save out as Json
with open('DublinArrivals_2018-12-23.json', 'w') as fout:
    json.dump(table_data,fout)
