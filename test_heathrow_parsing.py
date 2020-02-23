from datetime import datetime
from heathrow_parsing import Flight, ParsedFlights
import json
import unittest

class SampleData(object):
    
    def __init__(self):
        self.test_flight_departed_1 = json.loads(r'''{"flightIdentifier":"OS8237","flightNumber":"8237","airlineIataRef":"OS","origin":{"airportIataRef":"LHR","terminalCode":"2","status":{"interpretedStatus":" Departed 15:15  ","category":"INFO","messages":{"message":[{"text":"Departed","data":"15:15"},{"text":" "}]},"code":"AB","statusTime":"2020-01-30T15:15:00.000Z"},"scheduledDateTime":{"utc":"2020-01-30T14:30:00.000","local":"2020-01-30T14:30:00.000","utcOffset":0}},"destination":{"airportIataRef":"YYC"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_MARKETING_FLIGHT","isHadacabCancelled":false}''')
        self.test_flight_departed_2 = json.loads(r'''{"flightIdentifier":"AC6186","flightNumber":"6186","airlineIataRef":"AC","origin":{"airportIataRef":"LHR","terminalCode":"2","status":{"interpretedStatus":" Departed 06:26  ","category":"INFO","messages":{"message":[{"text":"Departed","data":"06:26"},{"text":" "}]},"code":"AB","statusTime":"2020-02-14T06:26:00.000Z"},"scheduledDateTime":{"utc":"2020-02-14T06:00:00.000","local":"2020-02-14T06:00:00.000","utcOffset":0}},"destination":{"airportIataRef":"VIE"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_MARKETING_FLIGHT","isHadacabCancelled":false}''')
        self.test_flight_cancelled_1 = json.loads(r'''{"flightIdentifier":"BA7008","flightNumber":"7008","airlineIataRef":"BA","origin":{"airportIataRef":"LHR","terminalCode":"4","status":{"interpretedStatus":" Cancelled Contact airline","category":"INFO","messages":{"message":[{"text":"Cancelled"},{"text":"Contact airline"}]},"code":"CX","statusTime":"2020-01-30T15:05:00.000Z"},"scheduledDateTime":{"utc":"2020-01-30T15:05:00.000","local":"2020-01-30T15:05:00.000","utcOffset":0}},"destination":{"airportIataRef":"DOH"},"stops":{"stop":[],"count":0},"codeShareType":"CODESHARE_MARKETING_FLIGHT","isHadacabCancelled":false}''')

    def three_flights_one_cancelled(self):
        return [self.test_flight_departed_1, self.test_flight_departed_2, self.test_flight_cancelled_1]

class TestFlight(unittest.TestCase):
    """Test the class called Flight"""

    def setUp(self):
        self.raw_flight = SampleData().test_flight_departed_1

    def test_the_init(self):
        flight = Flight(self.raw_flight)
        self.assertIsInstance(flight.flight_id, str) #ToDO: assert regex string length >=0 with no whitespace.
        self.assertIsInstance(flight.scheduled_datetime, datetime)
        self.assertIsInstance(flight.departure_datetime, datetime)#Note: will return None and fail in some cases. 

    def test_to_list(self):
        flight = Flight(self.raw_flight)
        self.assertIsInstance(flight.to_list(), list)
        self.assertEqual(len(flight.to_list()), len(flight.labels()))

class TestParsedFlights(unittest.TestCase):
    def setUp(self):
        self.raw_flights = SampleData().three_flights_one_cancelled()
        
    def test_the_init(self):
        parsed_flights = ParsedFlights(self.raw_flights)
        self.assertEqual(len(parsed_flights.parsed_flights), len(self.raw_flights))
        #Check parsed_flights have the right class (the user defined Flight class)
        #   For brevity, just check the first parsed_flight .
        self.assertEqual(str(type(parsed_flights.parsed_flights[0])), "<class 'heathrow_parsing.Flight'>")

    def test_to_dataframe(self):
        parsed_flights = ParsedFlights(self.raw_flights)
        flight_df = parsed_flights.to_dataframe()
        self.assertEqual(len(flight_df), len(self.raw_flights))
        self.assertEqual(list(flight_df.columns), Flight.labels())
        #print(flight_df.head())

if __name__ == '__main__':
   unittest.main()